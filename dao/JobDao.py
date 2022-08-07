from dao.BaseDao import BaseDao


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
    def getJobPageList(self, search={}, page={}):
        # search={'searchName':'北京', 'searchType': 'jobCity'}
        # page={'currentPage':1, 'pageSize':10}
        sql = "select * from t_jobdata where 1=1"  # where 1=1 便于添加and
        params = []
        if search.get('searchType'):
            if search.get('searchType') == 'jobId':
                sql += " and {0} = %s".format(search.get('searchType'))
                params.append(search.get('searchName'))
            else:
                sql += " and {0} like %s".format(search.get('searchType'))
                params.append("%" + search.get('searchName') + "%")
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
        sql= "select count(*) as counts from t_jobdata where 1=1"  # where 1=1 便于添加and
        params = []
        if search.get('searchType'):
            if search.get('searchType') == 'jobId':
                sql += " and {0} = %s".format(search.get('searchType'))
                params.append(search.get('searchName'))
            else:
                sql += " and {0} like %s".format(search.get('searchType'))
                params.append("%" + search.get('searchName') + "%")

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
        result = self.execute(sql,[data.get('jobId'),data.get('similarJobId')])
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

