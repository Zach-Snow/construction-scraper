from flask import Flask, request, jsonify
from flask_restful import Api
import os
from garbe_scraper import garbe_scraper
from time import sleep

app = Flask(__name__)
api = Api(app)


@app.route('/garbe_new', methods=['GET'])
def get_garbe_new():
    result = garbe_scraper(class_name='@class="col-md-4"')
    return jsonify(result)


@app.route('/garbe_old', methods=['GET'])
def get_garbe_old():
    result = garbe_scraper(class_name='@data-category')
    return jsonify(result)


@app.route('/cleanup', methods=['GET'])
def cleanup():
    result = garbe_scraper(class_name="cleanup")
    return jsonify(result)


# run Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
