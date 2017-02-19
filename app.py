import logging
import os
from logging.config import fileConfig

import tensorflow as tf
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

fileConfig('logging_config.ini')
logger = logging.getLogger('app')
DEFAULT_PORT = '8080'

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception(e)
    return "Error [{}] occurred when processing request [{}]".format(e, request.base_url), 500


@app.errorhandler(404)
def handle_404(e):
    return "[{}] is not found.".format(request.base_url), 404


@app.route('/tensorflow')
def tensorflow():
    logger.info('processing tensorflow request.')
    hello = tf.constant('Hello, TensorFlow!')
    sess = tf.Session()
    message = sess.run(hello).decode('utf-8')
    logger.info(message)

    a = tf.constant(10)
    b = tf.constant(32)
    number = sess.run(a + b).item()
    logger.info(number)
    return jsonify(message=message, number=number)


if __name__ == '__main__':
    port = os.getenv('PORT', DEFAULT_PORT)
    logger.info("starting app at port {}".format(port))
    app.run(host='0.0.0.0', port=int(port))
