from __future__ import division, print_function
# coding=utf-8
import os
import pandas as pd
import random
from google.cloud import storage
from flask import Flask, redirect, url_for, request, render_template
from gevent.pywsgi import WSGIServer
import re
from flask_caching import Cache
import bmemcached
import codecs
import time

# Define a flask app
app = Flask(__name__)
app.secret_key = b'\xc9%\xd1\xf1\xf7=\xfaM$\xf6\x9c\xc7\t\xc2h\x00'

servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
user = os.environ.get('MEMCACHIER_USERNAME', '')
passw = os.environ.get('MEMCACHIER_PASSWORD', '')

cache = bmemcached.Client(servers, username=user, password=passw)

cache.enable_retry_delay(True)
# def set_up_cache():
#     cache = Cache()
#     cache_servers = os.environ.get('MEMCACHIER_SERVERS')
#     if cache_servers == None:
#         cache.init_app(app, config={'CACHE_TYPE': 'simple'})
#     else:
#         cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
#         cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
#         cache.init_app(app,
#             config={'CACHE_TYPE': 'saslmemcached',
#                     'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
#                     'CACHE_MEMCACHED_USERNAME': cache_user,
#                     'CACHE_MEMCACHED_PASSWORD': cache_pass,
#                     'CACHE_OPTIONS': { 'behaviors': {
#                         # Faster IO
#                         'tcp_nodelay': True,
#                         # Keep connection alive
#                         'tcp_keepalive': True,
#                         # Timeout for set/get requests
#                         'connect_timeout': 2000, # ms
#                         'send_timeout': 750 * 1000, # us
#                         'receive_timeout': 750 * 1000, # us
#                         '_poll_timeout': 2000, # ms
#                         # Better failover
#                         'ketama': True,
#                         'remove_failed': 1,
#                         'retry_timeout': 2,
#                         'dead_timeout': 30}}})
#
#     return cache
#
# cache = set_up_cache()

# memcachier-round-62159
classes = {}
all_results = {}
location = ""

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="image-location-finder-43db266d7800.json"
storage_client = storage.Client()
bucket = storage_client.bucket("image-finder-datafiles")

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    cache.set('selected_pic',request.form['javascript_data'].split("/")[-1])
    print(cache.get('selected_pic'))
    return "Check"

@app.route('/', methods=['GET'])
def index():
    # Main page
    matches = []
    with codecs.open(r"utils/app_iceland_results.txt", 'r', encoding="utf-8-sig") as f:
        for line in f:
            m = re.match(r"(.*?)[|](.*?)[|](.*?)[|](.*?)[|](.*?)\n",line)
            matches.append([m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)])
    matches_sample = random.sample(matches,20)
    for i,rec in enumerate(matches_sample):
        location = rec[0]
        class_ = rec[1]
        # all_results["pic_"+str(i)+".png"] = rec[2:]
        # classes["pic_"+str(i)+".png"] = class_
        cache.set("pic_"+str(i)+".png", class_)
        cache.set("result_pic_" + str(i) + ".png","|".join(rec[2:]))
        blob = bucket.blob("app_iceland/" + location)
        blob.download_to_filename(r"static/images/pic_" + str(i) + ".png")
        # copyfile(r"./utils/app_iceland/" + location, r"./static/images/pic_" + str(i) + ".png")
    return render_template('index.html')

print('Running on http://localhost:5000')

@app.route('/displayClassText', methods=['GET', 'POST'])
def displayClassText():
    if request.method == 'POST':
        selected_pic = cache.get('selected_pic')
        class_ = cache.get(selected_pic)
    return class_

@app.route('/findLocation', methods=['GET', 'POST'])
def findLocation():
    if request.method == 'POST':
        selected_pic = cache.get('selected_pic')
        results = cache.get("result_"+selected_pic).split("|")
        print(results)
        for i, city in enumerate(pd.Series(results)):
            try:
                os.remove(r"static/images/result_" + str(i) + ".png")
            except:
                pass
            image_path = city.split(",")[0]
            blob = bucket.blob("Dataset" + image_path.replace("\\", "/"))
            blob.download_to_filename(r"static/images/result_" + str(i) + ".png")
        return "|".join(results)
    return None

if __name__ == '__main__':
    # Serve the app with gevent
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
