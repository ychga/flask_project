from flask import Blueprint, render_template, request, session, redirect
from service.UserService import UserService
import json


userController = Blueprint('userController', __name__)


# 获取前端数据，该页面上的CRUD均使用该方法，通过表单中的opr域来判断所需数据库操作
@userController.route("/userlist", methods=['post', 'get'])
def userList():
    # 获取分页所需数据
    searchName = request.form.get('searchName')
    currentPage = request.form.get('currentPage')
    pageSize = request.form.get('pageSize')
    opr = request.form.get('opr')

    currentPage = 1 if not currentPage else int(currentPage)
    pageSize = 10 if not pageSize else int(pageSize)
    startRow = (currentPage - 1) * pageSize
    search = {}
    if searchName:
        search = {'userName': searchName}

    # 初始化页面分页信息page
    page = {'currentPage': currentPage, 'pageSize': pageSize, 'startRow': startRow}

    userService = UserService()
    # 删除，修改，添加的判定
    result = 0
    if opr == "del":  # 删除用户
        userId = request.form.get("userId")
        result = userService.removeUser(userId)
    elif opr == "update":  # 修改用户信息
        userId = request.form.get("userId")
        realName = request.form.get("realName")
        data = {"realName": realName, "userId": userId}
        result = userService.updateUser(data)
    elif opr == "create":  # 新建用户
        userName = request.form.get("searchName")
        userPwd = request.form.get("userPwd")
        realName = request.form.get("realName")
        data = {"userName": userName, "userPwd": userPwd, "realName": realName}
        result = userService.createUser(data)

    # 完善分页信息page
    pageList, count = userService.getUserPageList(search, page)
    page['pageList'] = pageList
    page['count'] = count['counts']
    totalPage = (count['counts'] // pageSize) if count['counts'] % pageSize == 0 else (count['counts'] // pageSize + 1)
    page['totalPage'] = totalPage

    # 携带数据渲染、返回网页
    return render_template("userlist.html", page=page, search=search, result=result)


# AJAX接口
@userController.route("/ajax", methods=['get', 'post'])
def ajaxUserList():
    userService = UserService()
    userList = userService.getAllUserList()  # [{'userName':'zhangsan'},{'userName':'lisi'}]
    return json.dumps(userList, ensure_ascii=False)


#
@userController.route("/ajaxpage")
def ajaxPage():
    return render_template("ajaxtest.html")
