from dao.UserDao import UserDao


class UserService:

    def getUserByUserName(self, userName):
        userDao = UserDao()
        try:
            user = userDao.getUserByUserName(userName)
        finally:
            userDao.close()
        return user

    def getAllUserList(self):
        userDao = UserDao()
        try:
            userlist = userDao.getAllUserList()
        finally:
            userDao.close()
        return userlist

    def getUserPageList(self, search, page):
        userDao = UserDao()
        try:
            pageList = userDao.getUserPageList(search, page)
            count = userDao.getTotalCount(search)
        finally:
            userDao.close()
        return pageList, count

    def removeUser(self, userId):
        userDao = UserDao()
        try:
            result = userDao.removeUser(userId)
        finally:
            userDao.close()
        return result

    def updateUser(self, data={}):
        userDao = UserDao()
        try:
            result = userDao.updateUser(data)
        finally:
            userDao.close()
        return result

    def createUser(self, data={}):
        userDao = UserDao()
        try:
            result = userDao.createUser(data)
        finally:
            userDao.close()
        return result
