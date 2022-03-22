import os
import atexit
from pprint import pprint
from flask import Flask, \
    send_from_directory, \
    render_template
from flask import jsonify
from flask_restful import Api
from garbe_scraper import garbe_scraper
from time import sleep
from driver_setup import set_driver
from rosa_alscher_scrapper import rosa_scraper
from brandberger_scraper import brandberger_scraper
from garbe_scraper import database as garbe_db
from rosa_alscher_scrapper import database as rosa_db
from brandberger_scraper import database as branden_db
from flask_apscheduler import APScheduler

app = Flask(__name__)
api = Api(app)
garbe_link = "https://www.garbe-immobilien-projekte.de/projekte/"
rosa_link = "https://rosa-alscher.com/en/projects.html"
brand_berger_link = "https://www.brandberger.com/en/#references"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/garbe_new', methods=['GET'])
def get_garbe_new():
    browser = set_driver(garbe_link)
    result = garbe_scraper(class_name='@class="col-md-4"', browser=browser)
    browser.quit()
    return jsonify(result)


@app.route('/garbe_old', methods=['GET'])
def get_garbe_old():
    browser = set_driver(garbe_link)
    result = garbe_scraper(class_name='@data-category', browser=browser)
    browser.quit()
    return jsonify(result)


@app.route('/rosa_all', methods=['GET'])
def rosa_all():
    browser = set_driver(rosa_link)
    result = rosa_scraper(browser=browser)
    browser.quit()
    return jsonify(result)


@app.route('/brandberger', methods=['GET'])
def brandberger():
    browser = set_driver(brand_berger_link)
    result = brandberger_scraper(browser=browser)
    browser.quit()
    return jsonify(result)


@app.route('/garbe_database', methods=['GET'])
def garbe_database():
    result = garbe_db(action_bool=True, project_dictionary={})
    return jsonify(result)


@app.route('/rosa_database', methods=['GET'])
def rosa_database():
    result = rosa_db(action_bool=True, project_dictionary={})
    return jsonify(result)


@app.route('/brandenberg_database', methods=['GET'])
def brandenberg_database():
    result = branden_db(action_bool=True, return_list=[])
    return jsonify(result)


# call scheduler functions
def scheduler_job():
    browser = set_driver(garbe_link)
    garbe_scraper(class_name='@class="col-md-4"', browser=browser)
    browser.quit()
    sleep(30)
    browser = set_driver(garbe_link)
    garbe_scraper(class_name='@data-category', browser=browser)
    browser.quit()
    sleep(30)
    browser = set_driver(rosa_link)
    rosa_scraper(browser=browser)
    browser.quit()
    sleep(30)
    browser = set_driver(brand_berger_link)
    brandberger_scraper(browser=browser)
    browser.quit()
    sleep(30)


# run Server
if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.add_job(func=scheduler_job, trigger='interval', id='job', days=7)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.run(host="0.0.0.0", port=5001, debug=True)
