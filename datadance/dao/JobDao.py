from dao.BaseDao import BaseDao
import xlrd


class JobDao(BaseDao):
    def createJobData(self, sql, params):
        result = self.execute(sql, params)
        self.commit()
        return result

    def getJobSalaryStatisticByJobCity(self):
        # 去除每个城市的最高工资和最低工资后取平均值，目前该sql语句不够好
        sql = 'select avg(jobMeanSalary) as jobsavg, jobCity from t_jobdata ' \
              'where (jobMeanSalary not in(select max(jobMeanSalary)from t_jobdata group by jobCity)) ' \
              'and (jobMeanSalary not in(select min(jobMeanSalary) from t_jobdata group by jobCity)) ' \
              'group by jobCity order by jobsavg desc;'
        result = self.execute(sql)
        print(result)
        print(self.fetchall())
        return self.fetchall()

    def getJobSalaryStatisticByJobType(self):
        # 去除每个职位的最高工资和最低工资后取平均值，目前该sql语句不够好
        sql = 'select avg(jobMeanSalary) as jobsavg, jobType from t_jobdata ' \
              'where (jobMeanSalary not in(select max(jobMeanSalary)from t_jobdata group by jobType)) ' \
              'and (jobMeanSalary not in(select min(jobMeanSalary) from t_jobdata group by jobType)) ' \
              'group by jobType order by jobsavg desc;'
        result = self.execute(sql)
        return self.fetchall()

    def getJobCountStatisticByJobType(self):
        sql = 'select count(*) as jobCount, jobType from t_jobdata group by jobType order by jobCount desc'
        result = self.execute(sql)
        return self.fetchall()

    def getJobCountStatisticByJobCity(self):
        sql = 'select count(*) as jobCount, jobCity from t_jobdata group by jobCity order by jobCount desc' \
              ' limit 0, 10'
        result = self.execute(sql)
        return self.fetchall()

    # 分页查询方法
    # search={'jobName':"机械", 'jobType': "机械学习",'jobCompany':"公司", 'jobCity':"北京"}  page={'currentPage':1, 'pageSize':10}
    def getJobPageList(self, search={}, page={}):
        sql = "select * from t_jobdata where 1=1"  # where 1=1 便于添加and
        params = []
        # 根据传入search中的字段存在与否，增加对应的sql限制
        if search.get('jobId'):
            sql += " and jobId = %s"
            params.append(search.get('jobId'))
        else:
            if search.get('jobName'):
                sql += " and jobName like %s"
                params.append("%" + search.get('jobName') + "%")
                pass
            if search.get('jobType'):
                sql += " and jobType like %s"
                params.append("%" + search.get('jobType') + "%")
                pass
            if search.get('jobCompany'):
                sql += " and jobCompany like %s"
                params.append("%" + search.get('jobCompany') + "%")
                pass
            if search.get('jobAddress'):
                sql += " and jobAddress like %s"
                params.append("%" + search.get('jobAddress') + "%")
                pass
            if search.get('jobOrder'):  # jobOrder不存在或为0时，以默认的id升序排序；为1时，按平均薪资降序排序；为2时，按平均薪资升序排序
                if search.get('jobOrder') == 1:
                    sql += " order by jobMeanSalary desc"
                    pass
                elif search.get('jobOrder') == 2:
                    sql += " order by jobMeanSalary asc"
                    pass
                pass

        print(sql)
        print(params)

        # 分页
        sql += " limit %s, %s"  # limit startRow, rows
        params.append(page.get('startRow'))
        params.append(page.get('pageSize'))

        self.execute(sql, params)
        return self.fetchall()

    # 统计数量
    def getTotalCount(self, search={}):
        sql = "select count(*) as counts from t_jobdata where 1=1"  # where 1=1 便于添加and
        params = []
        if search.get('jobId'):
            sql += " and jobId = %s"
            params.append(search.get('jobId'))
        else:
            if search.get('jobName'):
                sql += " and jobName like %s"
                params.append("%" + search.get('jobName') + "%")
                pass
            if search.get('jobType'):
                sql += " and jobType like %s"
                params.append("%" + search.get('jobType') + "%")
                pass
            if search.get('jobCompany'):
                sql += " and jobCompany like %s"
                params.append("%" + search.get('jobCompany') + "%")
                pass
            if search.get('jobAddress'):
                sql += " and jobAddress like %s"
                params.append("%" + search.get('jobAddress') + "%")
                pass
        self.execute(sql, params)
        return self.fetchone()

    # 修改工作信息
    def updateJob(self, data={}):
        sql = "update t_jobdata set jobName=%s, jobSalary=%s, jobAddress=%s, jobCompany=%s, jobType=%s where jobId=%s"
        result = self.execute(sql,
                              [data.get("jobName"),
                               data.get("jobSalary"),
                               data.get("jobAddress"),
                               data.get("jobCompany"),
                               data.get("jobType"),
                               data.get("jobId")])
        self.commit()
        return result

    # 闲置未使用的查询，查询每一条城市和平均薪资信息
    def getJobSalaryAndCity(self):
        sql = "select jobCity, jobMeanSalary from t_jobdata"
        self.execute(sql)
        return self.fetchall()

    # 删除工作记录
    def removeJob(self, jobId):
        sql = "delete from t_jobdata where jobId=%s"
        result = self.execute(sql, [jobId])
        self.commit()
        return result

    # 查询城市和工种的数量排序
    def getJobByCityAndType(self):
        sql = "select count(*) as counts, jobCity, jobType from t_jobdata group by jobCity, jobType " \
              "order by counts desc limit 0,10"
        self.execute(sql)
        return self.fetchall()

    # 修改工作信息，jobDetail
    def updateJobDetail(self, data={}):
        sql = "update t_jobdata set jobDetail=%s where jobId=%s"
        result = self.execute(sql,
                              [data.get("jobDetail"),
                               data.get("jobId")])
        self.commit()
        return result

    def getAllJobList(self):
        sql = 'select * from t_jobdata where jobDetail is not null'
        self.execute(sql)
        return self.fetchall()

    def createSimilarJob(self, data={}):
        sql = 'insert into t_similar_job(jobId, similarJobId) values(%s, %s)'
        result = self.execute(sql, [data.get('jobId'), data.get('similarJobId')])
        self.commit()
        return result

    # 获取职位详情和相似职位信息
    def getJobDetail(self, id):
        sql = 'select * from t_jobdata where jobId=%s'
        self.execute(sql, [id])
        job = self.fetchone()
        sql = 'select t1.* from t_jobdata t1 where t1.jobId in (select similarJobId from t_similar_job t2 where t2.jobId=%s)'
        self.execute(sql, [id])
        sjobList = self.fetchall()
        return job, sjobList

    # 添加job数据，目前添加了工作名称 工作薪水 地址 公司名 要求 链接 类型。使用 xlsx导入 数据导出时需要按照下面的添加顺序导出，也可以更改下面的sql语句更改顺序和导入数据数量
    def addJob(self, data={}):
        path = "t_jobdata.xlsx"
        # path = r'D:\t_jobdata.xlsx'
        #  data = pd.read_csv(path, encoding='utf-8')
        #   con=self.getConnection(self)
        wkb = xlrd.open_workbook(path)
        # 2.获取sheet
        sheet = wkb.sheet_by_index(0)  # 获取第一个sheet表['job']
        # 3.获取总行数
        rows_number = sheet.nrows
        # 4.遍历sheet表中所有行的数据，并保存至一个空列表cap[]
        cap = []
        for i in range(rows_number):
            x = sheet.row_values(i)  # 获取第i行的值（从0开始算起）
            cap.append(x)
        #     c = self.fetchone(self):#con.cursor()
        for msg in cap:
            name = msg[0]  # A
            sal = msg[1]  # B
            add = msg[2]  # C
            com = msg[3]  # D
            detail = msg[4]  # E
            link = msg[5]  # F
            type = msg[7]  # H
            city = msg[8]  # I
            # 使用f-string格式化字符串，对sql进行赋值
            sql = (
                "insert into t_jobdata(jobName, jobSalary, jobAddress, jobCompany,jobLink,jobType, jobDetail, jobCity) value(%s,%s,%s,%s,%s,%s,%s,%s)")
            result = self.execute(sql, [name, sal, add, com,link,type, detail,city])
        self.commit()
        print("插入数据完成！")
        return result
