from flask import Flask, render_template, redirect, request, session
from service.UserService import UserService
from controller.UserController import userController
from controller.JobController import jobController


app = Flask(__name__)
# app.config.update(DEBUG=True)
app.config['SECRET_KEY'] = "SESSIONKEYAAAABBBXXXYYYYY"  # 给session加密用
app.register_blueprint(userController)
app.register_blueprint(jobController)


@app.route('/')  # 路由 url -- 响应的函数进行绑定
def hello_world():  # put application's code here
    return render_template('index.html')  # 返回一个页面


# rest
@app.route('/testrest/<int:id>')
def testRest(id):
    return str(id)


@app.route('/login', methods=['post'])
def login():
    # request.args.get()
    userName = request.form['userName']
    userPwd = request.form.get('userPwd')
    userService = UserService()

    user = userService.getUserByUserName(userName)

    if user and user.get('userPwd') == userPwd:
        session['user'] = user
        return render_template('main.html', userName=userName)
    else:
        return render_template('index.html', message="用户名或者密码错误")


# 退出
@app.route('/logout')
def logout():
    session.pop('user')
    session.clear()
    return render_template("index.html")


@app.route('/main')
def mainPage():
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
