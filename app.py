import os
import atexit
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_restful import Api
from garbe_scraper import garbe_scraper
from time import sleep
from driver_setup import set_driver
from rosa_alscher_scrapper import rosa_scraper
from brandberger_scraper import brandberger_scraper
from apscheduler.schedulers.background import BackgroundScheduler
from garbe_scraper import database

app = Flask(__name__)
api = Api(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/garbe_new', methods=['GET'])
def get_garbe_new():
    browser = set_driver("https://www.garbe-immobilien-projekte.de/projekte/")
    result = garbe_scraper(class_name='@class="col-md-4"', browser=browser)
    browser.quit()
    return jsonify(result)


@app.route('/garbe_old', methods=['GET'])
def get_garbe_old():
    browser = set_driver("https://www.garbe-immobilien-projekte.de/projekte/")
    result = garbe_scraper(class_name='@data-category', browser=browser)
    browser.quit()
    return jsonify(result)


@app.route('/rosa_all', methods=['GET'])
def rosa_all():
    browser = set_driver("https://rosa-alscher.com/en/projects.html")
    result = rosa_scraper(browser=browser)
    browser.quit()
    return jsonify(result)


@app.route('/brandberger', methods=['GET'])
def brandberger():
    browser = set_driver("https://www.brandberger.com/en/#references")
    result = brandberger_scraper(browser=browser)
    browser.quit()
    return jsonify(result)


@app.route('/garbe_database', methods=['GET'])
def garbe_database():
    result = database(action_bool=True, project_dictionary={})
    return jsonify(result)


# handling the automatic data fetch for a period, I have used 1 week here
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_garbe_old, trigger="interval", days=7)
scheduler.add_job(func=get_garbe_new, trigger="interval", days=7)
scheduler.add_job(func=rosa_all, trigger="interval", days=7)
scheduler.add_job(func=brandberger, trigger="interval", days=7)
scheduler.start()

# Shutting down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# run Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
