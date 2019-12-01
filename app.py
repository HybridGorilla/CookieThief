from flask import request
from flask import Flask
from flask import render_template
from flask import jsonify
import sqlite3
import time
import calendar

app = Flask(__name__)
global_headers = ""


@app.before_request
def before_request():
    if "IgnoreMe" in request.headers['Cookie']:
        pass
    else:
        global_headers = str(request.headers['Cookie'])
        conn = sqlite3.connect("requests.db")
        if global_headers != None:
            sql = 'INSERT INTO requests (request_data) VALUES ("'+global_headers+'")'
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            conn.close()
        else: 
            pass


@app.after_request
def after_request(response):
    return response


@app.route("/")
@app.route("/index")
def index():
    return render_template("main.html")


@app.route("/poll")
def poll():
    arr = []
    sql = "SELECT request_data FROM requests ORDER BY id DESC LIMIT 10;"
    conn = sqlite3.connect("requests.db")
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    values = c.fetchall()
    return jsonify(values)


# Dynamic Domain for Filtering with Jquery(?) 
@app.route('/capture/<variable>', methods=['GET'])
def pokemon(variable):
    cookie = request.headers['cookie']
    return str(cookie)


if __name__ == '__main__':
    app.run(debug=True)


