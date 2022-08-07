from dao.JobDao import JobDao


class JobService:
    def getJobSalaryByJobType(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobSalaryStatisticByJobType()
        finally:
            jobDao.close()
        return data

    def getJobCountByJobType(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobCountStatisticByJobType()
        finally:
            jobDao.close()
        return data

    def getJobCountByJobCity(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobCountStatisticByJobCity()
        finally:
            jobDao.close()
        return data

    def getJobPageList(self, search, page):
        jobDao = JobDao()
        try:
            pageList = jobDao.getJobPageList(search, page)
            count = jobDao.getTotalCount(search)
        finally:
            jobDao.close()
   
    def addJob(self, data={}):
        jobDao = JobDao()
        try:
            result = jobDao.addJob()
            print("ok")
        finally:
            jobDao.close()
        return result

        return pageList, count

    def updateJob(self, data={}):
        jobDao = JobDao()
        try:
            result = jobDao.updateJob(data)
        finally:
            jobDao.close()
        return result

    def getJobSalaryAndCity(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobSalaryAndCity()
        finally:
            jobDao.close()
        return data

    def removeJob(self, jobId):
        jobDao = JobDao()
        try:
            result = jobDao.removeJob(jobId)
        finally:
            jobDao.close()
        return result

    def getJobByCityAndType(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobByCityAndType()
        finally:
            jobDao.close()
        return data

    def updateJobDetail(self, data={}):
        jobDao = JobDao()
        try:
            result = jobDao.updateJobDetail(data)
        finally:
            jobDao.close()
        return result

    def getAllJobList(self):
        jobDao = JobDao()
        try:
            data = jobDao.getAllJobList()
        finally:
            jobDao.close()
        return data

    def createSimilarJob(self, data={}):
        jobDao = JobDao()
        try:
            result = jobDao.createSimilarJob(data)
        finally:
            jobDao.close()
        return result

    def getJobDetail(self, id):
        jobDao = JobDao()
        try:
            job, sjobList = jobDao.getJobDetail(id)
        finally:
            jobDao.close()
        return job, sjobList

