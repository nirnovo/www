from flask import Flask, render_template, redirect, url_for, request
import random
import string
import redis
import time

app = Flask(__name__)
conn = redis.StrictRedis(host="localhost", port=6379, db=2)

def getfromdb(username):
    content = conn.hget(username, "content")
    if content is None:
        content = b""
    else:
        content = conn.hget(username, "content")
   # last_time = conn.hget(time, "time")
    if conn.hexists(username, "time"):
        times = conn.hget(username, "time")
    else:
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return content, times


def random_user(ulength):
    chars = string.ascii_letters + string.digits
    tmp_name = ''.join([random.choice(chars) for i in range(ulength)])
#    getfromdb(tmp_name.upper())
    return tmp_name.upper()


@app.route('/')
def index():
    return redirect(url_for('users', user=random_user(8)))


@app.route('/<user>')
def users(user):
    info,times = getfromdb(user)
    print(info)
    return render_template("main.html", username=user, t=info.decode("utf-8"), times=times.decode("utf-8"))
    # return render_template("main.html", username=user, t=info.decode("utf-8"))


@app.route('/ajax_save', methods=["GET", "POST"])
def ajax_save():
    if request.method == "POST":
        user = request.json['_user']
        print(user)
        content = request.json['_content']
        print(content)
        conn.hset(user, "content", content)
        times = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        conn.hset(user, "time", times)
    return "OK"


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
