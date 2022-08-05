import pymysql
import json
import os


# print(os.getcwd())
class BaseDao:
    """
    数据库访问基类
    """
    def __init__(self, config="mysql.json"):
        self.__config = json.load(open(os.path.dirname(__file__) + os.sep + config, mode="r", encoding="utf-8"))
        self.__conn = None
        self.__cursor = None

    def getConnection(self):
        if self.__conn:
            return self.__conn
        else:
            self.__conn = pymysql.connect(**self.__config)
            return self.__conn

    def execute(self, sql, params=[], ret="dict"):
        result = 0
        try:
            self.__conn = self.getConnection()
            if ret == "dict":
                self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)  # 返回字典数据
            else:
                self.__cursor = self.__conn.cursor()                            # 返回元组数据
            result = self.__cursor.execute(sql, params)
            return result
        except pymysql.DatabaseError as e:
            print(e)

    def fetchone(self):
        if self.__cursor:
            return self.__cursor.fetchone()

    def fetchall(self):
        if self.__cursor:
            return self.__cursor.fetchall()

    def close(self):
        if self.__cursor:
            self.__cursor.close()
        # if self.__conn:
        #     self.__conn.close()

    def commit(self):
        if self.__conn:
            self.__conn.commit()

    def rollback(self):
        if self.__conn:
            self.__conn.rollback()
