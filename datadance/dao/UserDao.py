from dao.BaseDao import BaseDao


class UserDao(BaseDao):
    # 从userName获取用户信息
    def getUserByUserName(self, userName):
        sql = "select * from t_user where userName=%s"
        params = [userName]
        self.execute(sql, params=params)
        return self.fetchone()  # 如果没有查到，返回None

    # 获取全部用户，数据量大时不推荐使用
    def getAllUserList(self):
        sql = "select * from t_user"
        self.execute(sql)
        return self.fetchall()

    # 分页查询方法
    def getUserPageList(self, search={}, page={}):  # search={'userName':'zhangsan'} page={'currentPage':1, 'pageSize':10}
        sql = "select * from t_user where 1=1"  # where 1=1 便于添加and
        params = []
        if search.get('userName'):
            sql += " and userName like %s"
            params.append("%" + search.get('userName') + "%")

        # 分页
        sql += " limit %s, %s"  # limit startRow, rows
        params.append(page.get('startRow'))
        params.append(page.get('pageSize'))

        self.execute(sql, params)
        return self.fetchall()

    # 统计数量
    def getTotalCount(self, search={}):
        sql= "select count(*) as counts from t_user where 1=1"  # where 1=1 便于添加and
        params = []
        if search.get('userName'):
            sql += " and userName like %s"
            params.append("%" + search.get('userName') + "%")

        self.execute(sql, params)
        return self.fetchone()

    # 删除用户
    def removeUser(self, userId):
        sql = "delete from t_user where userId=%s"
        result = self.execute(sql, [userId])
        self.commit()
        return result

    # 修改用户信息
    def updateUser(self, data={}):
        sql = "update t_user set realName=%s where userId=%s"
        result = self.execute(sql, [data.get("realName"), data.get("userId")])
        self.commit()
        return result

    # 新增用户
    def createUser(self, data={}):
        sql = "insert into t_user(userName, userPwd, realName) values(%s, %s, %s)"
        result = self.execute(sql, [data.get("userName"), data.get("userPwd"), data.get("realName")])
        self.commit()
        return result

    # 关闭数据库连接，避免连接数达上限
    def close(self):
        super().close()
