import csv

import backend
import util
from flask import Flask, send_file, render_template, request, redirect, session
from os import environ
import time
import io
import socket
import threading

app = Flask(__name__, static_url_path='/static')
app.secret_key = "My secret"


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/search/<condition>/')
def display_search_page(condition=None):
    if condition != "new" and condition != "used":
        return "Invalid address"
    return render_template('search_page.html', condition=condition)


@app.route('/results/<condition>/')
def run_search(condition=None):
    search_words = request.args.get('q')
    results = []
    threads = []
    lock = threading.Lock()
    stop_event = threading.Event()
    websites = backend.USED_WEBSITES if condition == 'used' else backend.NEW_WEBSITES
    for site in websites:
        thread = threading.Thread(target=backend.search_a_website,
                                  args=(site, search_words, results, lock, stop_event, condition))
        thread.start()
        threads.append(thread)

    # Set a timer to stop threads after 25s, Heroku timeout is 30s
    timer = threading.Timer(20, stop_event.set)
    timer.start()

    # Wait for all threads to complete or until stop condition is met or until timer expires
    for t in threads:
        t.join()  # Wait for this thread to terminate
        if len(results) >= 10:
            break
    # Cancel timer if it has not expired
    timer.cancel()

    # Sort results by price
    results = util.sort_by_price(results)
    median = util.price_prettify(util.median_price(results))

    # Format prices and save results for download
    session["results"] = [['Title', 'Price', 'Image', 'URL']]
    for r in results:
        r.price = util.price_prettify(util.str_to_float(r.price))
        session["results"].append([r.title, r.price, r.image_src, r.url])
    return render_template('result_page.html', search_words=search_words, result=results,
                           median=median, condition=condition)


@app.route('/download/<condition>/<search_words>/', methods=['GET'])
def download_file(condition, search_words):
    # Create a StringIO obj to write CSV data
    csv_data = io.StringIO()
    # Create a CSV writer obj
    csv_writer = csv.writer(csv_data)
    data = session.get("results", [])
    csv_writer.writerows(data)
    csv_data.seek(0)
    return send_file(io.BytesIO(csv_data.getvalue().encode()), mimetype='text/csv', as_attachment=True,
                     download_name=f"{condition}_{search_words}.csv")


def finish(self):
    if not self.wfile.closed:
        self.wfile.flush()
        try:
            self.wfile.flush()
        except socket.error:
            # A final socket error may have occurred here, such as
            # the local error ECONNABORTED.
            pass
    self.wfile.close()
    self.rfile.close()


if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
