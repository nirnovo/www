from flask import Flask, render_template, redirect, url_for, request
import random
import string
import redis

app = Flask(__name__)

conn = redis.StrictRedis(host="localhost", port=6379, db=1)
def getfromdb(username):
    conn = conndb()
    content = conn.get(username)
    if content is None:
        content = b""
    else:
        content = conn.get(username)
    return content


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
    info = getfromdb(user).decode("utf-8")
    print(info)
    return render_template("main.html", username=user, t=info)
    # return render_template("main.html", username=user, t=info.decode("utf-8"))


@app.route('/ajax_save', methods=["GET", "POST"])
def ajax_save():
    if request.method == "POST":
        conn = conndb()
        user = request.json['_user']
        print(user)
        content = request.json['_content']
        print(content)
        conn.set(user, content)
    return "OK"


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
