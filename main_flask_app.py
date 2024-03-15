import csv

import backend
import util
from flask import Flask, send_file, render_template, request, redirect, session
from os import environ
import time
import io
import socket

app = Flask(__name__)
app.secret_key = "My secret"


@app.route('/')
def main_page():
    return render_template('main_equipment_page.html')


@app.route('/search/<condition>/')
def display_search_page(condition=None):
    if condition != "new" and condition != "used":
        return "Invalid address"
    return render_template('search_page.html', condition=condition)


@app.route('/results/<condition>/')
def run_search(condition=None):
    search_words = request.args.get('search')
    # web_index is the  index of the website to begin or continue searching
    web_index = 0 if request.args.get('web_index') is None else int(request.args.get('web_index'))
    start_time = time.time()
    continue_searching = True
    message = ""
    results = []
    # time the result to make sure it makes heroku's 30 second timeout
    # stop searching if we have 10 or more results, run out of time, or finish searching relevant websites
    # check if web_index is less than 20 to ensure the while loop ends
    while continue_searching and web_index < 10 and time.time() - start_time < 20 and len(results) < 10:
        continue_searching, new_message, new_results = backend.search_a_website(search_words, condition, web_index)
        results.extend(new_results)
        message = message + new_message
        web_index += 1
    # if we ran out of time and got few results, continue the search where we left off in a redirect
    if continue_searching and len(results) < 4 and web_index < 20:
        return redirect("/results/%s/?web_index=%s&search=%s" % (condition, web_index, search_words))
    results = util.sort_by_price(results)
    median = util.price_prettify(util.median_price(results))
    for item in results:
        item.price = util.price_prettify(util.str_to_float(item.price))

    # Saving results for download
    session["results"] = [['Title', 'Price', 'Image', 'URL']]
    for r in results:
        session["results"].append([r.title, r.price, r.image_src, r.url])
    return render_template('result_page.html', search_words=search_words, result=results,
                           median=median, message=message, condition=condition)


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
