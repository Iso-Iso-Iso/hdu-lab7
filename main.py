from flask import Flask, render_template, request, session, redirect

from flask_session import Session
from services.user import UserServices

app = Flask(__name__, static_folder='static')
app.config['SESSION_TYPE'] = 'filesystem'
app.config.update(SECRET_KEY='super_secret_key:)')
Session(app)


@app.route('/')
def index():
    if session.get("access_token"):
        return redirect("/marks", 302)
    return render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    if session.get("access_token"):
        return redirect("/marks", 302)

    login = request.form['login']
    password = request.form['password']
    try:
        access_token = UserServices.login(login, password)['refresh']
        session['access_token'] = access_token
        return redirect("/marks", 302)
    except Exception as e:
        print(e)
        return redirect('/', 400)


@app.route("/marks", methods=["GET"])
def marks():
    if not session.get("access_token"):
        return redirect("/", 302)
    token = session.get("access_token")
    user_profile = UserServices.get_profile(token)
    id = user_profile['id']

    record = UserServices.get_recordbooks_record(id, token)
    return render_template('marks.html', records=record['results'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


app.run()
