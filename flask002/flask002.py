# coding: utf8
import os
import sqlite3
from functools import wraps

from flask import Flask, redirect, request, url_for, render_template, g, flash
from flask import session, make_response

from forms import RegistForm, LoginForm, PwdForm, InfoForm
from model import User

os.chdir("E:\\FlaskProject2\\flask002")
print(os.getcwd())

app = Flask(__name__)

app.config["DATABASE"] = 'database.db'
app.config["SECRET_KEY"] = 'who i am ? do you know?'


def connect_db():
    """Connects to the specific database."""
    db = sqlite3.connect(app.config['DATABASE'])
    return db


def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    # print('before_request()')
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        # print('teardown_request()')
        g.db.close()


def insert_user_to_db(user):
    # sql_insert = "INSERT INTO users (name,pwd,email,age,birthday,face) VALUES (?, ?, ?, ?, ?, ?)"
    user_attrs = user.getAttrs()
    values = " VALUES ("
    last_attr = user_attrs[-1]
    for attr in user_attrs:
        if attr != last_attr:
            values += " ?,"
        else:
            values += " ?"
    values += " )"
    sql_insert = "INSERT INTO users" + str(user_attrs) + values
    args = user.toList()
    g.db.execute(sql_insert, args)
    g.db.commit()


def query_users_from_db():
    users = []
    sql_select = "SELECT * FROM users"
    args = []
    cur = g.db.execute(sql_select, args)
    for item in cur.fetchall():
        user = User()
        user.fromList(item[1:])
        users.append(user)
    return users


def query_user_by_name(user_name):
    sql_select = "SELECT * FROM users where name=?"
    args = [user_name]
    cur = g.db.execute(sql_select, args)
    items = cur.fetchall()
    if len(items) < 1:
        return None
    first_item = items[0]
    user = User()
    user.fromList(first_item[1:])
    return user


def delete_user_by_name(user_name):
    delete_sql = "DELETE FROM users WHERE name=?"
    args = [user_name]
    g.db.execute(delete_sql, args)
    g.db.commit()


def update_user_by_name(old_name, user):
    update_str = ""
    user_attrs = user.getAttrs()
    last_attr = user_attrs[-1]
    for attr in user_attrs:
        if attr != last_attr:
            update_str += attr + " = ?,"
        else:
            update_str += attr + " = ?"
    sql_update = "UPDATE users SET " + update_str + " WHERE name = ?"
    args = user.toList()
    args.append(old_name)
    g.db.execute(sql_update, args)
    g.db.commit()


# 登陆装饰器检查登录状态
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_name" not in session:
            return redirect(url_for("user_login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    users = query_users_from_db()
    for user in users:
        print(user.toList())
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form["user_name"]
        userpwd = request.form["user_pwd"]
        # 查看用户名是否存在
        user_x = query_user_by_name(username)
        if not user_x:
            flash("用户名不存在！", category='err')
            return render_template('user_login.html', form=form)
        else:
            if str(userpwd) != str(user_x.pwd):
                flash("用户密码输入错误！", category='err')
                return render_template('user_login.html', form=form)
            else:
                # flash("登陆成功！", category='ok')
                session["user_name"] = user_x.name
                return redirect(url_for("index"))
    return render_template('user_login.html', form=form)


@app.route('/logout')
@user_login_req
def logout():
    # remove the username from the session if it's there
    session.pop('user_name', None)
    return redirect(url_for('index'))


@app.route('/regist/', methods=['GET', 'POST'])
def user_regist():
    form = RegistForm()
    if form.validate_on_submit():
        user = User()
        user.name = form.user_name.data
        user.pwd = form.user_pwd.data
        user.email = form.data['user_email']
        user.age = form.user_edge.data
        user.birthday = form.data["user_birthday"]
        # filestorage = form.user_face.data
        filestorage = request.files["user_face"]
        print(filestorage)
        user.face = filestorage.filename
        print(user.face)
        # 查看用户名是否已经存在
        user_x = query_user_by_name(user.name)
        if user_x:
            flash("用户名已经存在！", category='err')
            return render_template('user_regist.html', form=form)
        # 如果用户不存在，执行插入操作
        insert_user_to_db(user)
        # 保存用户头像文件
        filestorage.save(filestorage.filename)
        flash("用户注册成功！", category='ok')
        return redirect(url_for("user_login", username=user.name))
    return render_template('user_regist.html', form=form)


@app.route('/center/')
@user_login_req
def user_center():
    return render_template("user_center.html")


@app.route('/detail/')
@user_login_req
def user_detail():
    user = query_user_by_name(session.get("user_name"))
    return render_template("user_detail.html", user=user)


@app.route('/pwd/', methods=["GET", "POST"])
@user_login_req
def user_pwd():
    form = PwdForm()
    if form.validate_on_submit():
        old_pwd = form.old_pwd.data
        new_pwd = form.data["new_pwd"]
        user = query_user_by_name(session.get("user_name"))
        if str(old_pwd) == str(user.pwd):
            user.pwd = new_pwd
            update_user_by_name(user.name, user)
            session.pop("user_name", None)
            flash(message="修改密码成功，请重新登录！", category='ok')
            return redirect(url_for("user_login", username=user.name))
        else:
            flash(message="旧密码输入错误！", category='err')
            return render_template("user_pwd.html", form=form)
    return render_template("user_pwd.html", form=form)


@app.route('/info/', methods=["GET", "POST"])
@user_login_req
def user_info():
    form = InfoForm()
    user = query_user_by_name(session.get("user_name"))
    if form.validate_on_submit():
        old_name = user.name
        user.name = form.data["user_name"]
        user.email = form.data["user_email"]
        user.age = form.data["user_edge"]
        user.birthday = form.data["user_birthday"]
        user.face = form.data["user_face"]
        update_user_by_name(old_name, user)
        session["user_name"] = user.name
        return redirect(url_for("user_detail"))
    return render_template("user_info.html", user=user, form=form)


@app.route('/del/', methods=["GET", "POST"])
@user_login_req
def user_del():
    if request.method == "POST":
        delete_user_by_name(session.get("user_name"))
        return redirect(url_for("logout"))
    return render_template("user_del.html")


@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    return resp


if __name__ == '__main__':
    app.run(debug=True)
