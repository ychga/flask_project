import time

import jieba
from flask import Blueprint, request, render_template
from service.JobService import JobService
import json

jobController = Blueprint('jobController', __name__)


@jobController.route('/getjobsalarybytype', methods=['get', 'post'])
def getJobSalaryByJobType():
    jobService = JobService()
    data = jobService.getJobSalaryByJobType()
    return json.dumps(data, ensure_ascii=False)


@jobController.route('/getjobcountbytype', methods=['get', 'post'])
def getJobCountByJobType():
    jobService = JobService()
    data = jobService.getJobCountByJobType()
    return json.dumps(data, ensure_ascii=False)


@jobController.route('/getjobcountbycity', methods=['get', 'post'])
def getJobCountByJobCity():
    jobService = JobService()
    data = jobService.getJobCountByJobCity()
    return json.dumps(data, ensure_ascii=False)


@jobController.route('/getjobsalaryandcity', methods=['get', 'post'])
def getJobSalaryAndCity():
    jobService = JobService()
    data = jobService.getJobSalaryAndCity()
    return json.dumps(data, ensure_ascii=False)


@jobController.route('/getjobbycityandtype', methods=['get', 'post'])
def getJobByCityAndType():
    jobService = JobService()
    data = jobService.getJobByCityAndType()
    for d in data:
        d['cityAndType'] = d.get('jobCity') + '-' + d.get('jobType')
    return json.dumps(data, ensure_ascii=False)


import ast


# 分页职位数据管理页面
@jobController.route('/joblist', methods=['get', 'post'])
def jobList():
    page = {'currentPage': 1 if not request.form.get('currentPage') else int(request.form.get('currentPage')),
            'pageSize': 10 if not request.form.get('pageSize') else int(request.form.get('pageSize'))}

    page['startRow'] = (page.get('currentPage') - 1) * page.get('pageSize')
    search={}
    # newOrder = (int(request.args.get('newOrder')) + 1) % 3 if request.args.get('newOrder') else 0
    if request.args.get('search'):
        search = ast.literal_eval(request.args.get('search'))
        search["jobOrder"] = (int(search["jobOrder"])+1)%3
    else:
        search = {"jobId": request.form.get('search_jobId'),
                  "jobName": request.form.get('search_jobName'),
                  "jobType": request.form.get('search_jobType'),
                  "jobCompany": request.form.get('search_jobCompany'),
                  "jobAddress": request.form.get('search_jobAddress'),
                  "jobOrder": 0}
    print(search)
    jobService = JobService()

    result = 0
    if request.form.get('opr') == 'update':
        data = {'jobId': request.form.get('jobId'),
                'jobName': request.form.get('jobName'),
                'jobSalary': request.form.get('jobSalary'),
                'jobAddress': request.form.get('jobAddress'),
                'jobCompany': request.form.get('jobCompany'),
                'jobType': request.form.get('jobType')}
        result = jobService.updateJob(data)
    elif request.form.get('opr') == 'del':
        jobId = request.form.get('jobId')
        result = jobService.removeJob(jobId)

    joblist, count = jobService.getJobPageList(search, page)
    page['jobList'] = joblist
    page['count'] = count['counts']
    if page['count'] == 0 or page['jobList'] is None:
        search = {}
        joblist, count = jobService.getJobPageList(search, page)
        page['jobList'] = joblist
        page['count'] = count['counts']
    page['totalPage'] = count['counts'] // page.get('pageSize') if count['counts'] % page.get('pageSize') == 0 \
        else (count['counts'] // page.get('pageSize') + 1)

    return render_template('joblist.html', page=page, search=search, result=result)


@jobController.route('/jobchart', methods=['post', 'get'])
def jobChartPage():
    return render_template('jobchart.html')


import requests
from lxml import etree


@jobController.route('/scrapyjobdetail', methods=['post', 'get'])
def scrapyJobDetail():
    search = {}
    headers = {"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
               "Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
               "Upgrade-Insecure-Requests": "1"
               }

    page = {'currentPage': 1,
            'pageSize': 50,
            'startRow': 0}
    jobService = JobService()
    pageList, count = jobService.getJobPageList(search, page)

    currentPage = 1
    while pageList:
        for row in pageList:
            url = row.get('jobLink')
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                htmlText = response.text
                xtree = etree.HTML(htmlText)
                item = xtree.xpath('/html/body/main/content/section[2]/dl/dd/text()')
                if item:
                    content = item[0]
                    print(content)
                    data = {'jobId': row.get('jobId'), 'jobDetail': content}
                    jobService.updateJobDetail(data)
            time.sleep(3)
        currentPage += 1
        startRow = (currentPage - 1) * 50
        page = {'currentPage': currentPage,
                'pageSize': 50,
                'startRow': startRow}
        pageList, count = jobService.getJobPageList(search, page)


from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np


@jobController.route('/jobsimilar', methods=['post', 'get'])
def jobSimilar():
    jobService = JobService()
    jobList = jobService.getAllJobList()

    texts = []
    for row in jobList:
        detail = row.get('jobDetail')
        texts.append(" ".join(jieba.cut(detail)))
        pass

    vectorizer = CountVectorizer()
    tf = vectorizer.fit_transform(texts)
    words = vectorizer.get_feature_names()

    tfidfTransformer = TfidfTransformer()

    tfiwf = tfidfTransformer.fit_transform(tf)
    for i in range(len(jobList)):
        job = jobList[i]
        cosine_similarities = linear_kernel(tfiwf[i], tfiwf).flatten()
        top10List = []

        for t in range(11):
            index = np.argmax(cosine_similarities)
            top10List.append(jobList[index])
            cosine_similarities[index] = -1
            pass

        # 写入数据库
        for row in top10List:
            if row.get('jobId') != job.get('jobId'):
                data = {'jobId': job.get('jobId'), 'similarJobId': row.get('jobId')}
                jobService.createSimilarJob(data)
            pass
    pass


@jobController.route('/jobdetail', methods=['post', 'get'])
def getJobDetail():
    jobId = request.args.get('jobId')
    jobService = JobService()
    job, sjobList = jobService.getJobDetail(jobId)

    return render_template('jobdetail.html', job=job, sjobList=sjobList)

#add
@jobController.route('/add', methods=['post', 'get'])
def add():


    jobService = JobService()
    jobService.addJob()

    page = {'currentPage': 1 if not request.form.get('currentPage') else int(request.form.get('currentPage')),
            'pageSize': 10 if not request.form.get('pageSize') else int(request.form.get('pageSize'))}
    page['startRow'] = (page.get('currentPage') - 1) * page.get('pageSize')
    search = {}

    joblist, count = jobService.getJobPageList(search, page)
    page['jobList'] = joblist
    page['count'] = count['counts']
    page['totalPage'] = count['counts'] // page.get('pageSize') if count['counts'] % page.get('pageSize') == 0 \
        else (count['counts'] // page.get('pageSize') + 1)

    return render_template('joblist.html', page=page, search=search)

@jobController.route('/getjobsalarybyjobcity', methods=['post', 'get'])
def getjobSalaryByJobCity():
    jobService = JobService()
    data = jobService.getJobSalaryStatisticByJobCity()
    print("jobsc")
    print(data)
    return json.dumps(data, ensure_ascii=False)

@jobController.route('/jobsalarybyjobcity', methods=['post', 'get'])
def jobSalaryByJobCityPage():
    return render_template('jobsalarybyjobcity.html')

@jobController.route('/jobsalarybyjobtype', methods=['post', 'get'])
def jobSalaryByJobTypePage():
    return render_template('jobsalarybyjobtype.html')

@jobController.route('/jobcountbyjobtype', methods=['post', 'get'])
def jobCountByJobTypePage():
    return render_template('jobcountbyjobtype.html')

@jobController.route('/jobcountbyjobcity', methods=['post', 'get'])
def jobCountByJobCityPage():
    return render_template('jobcountbyjobcity.html')

@jobController.route('/jobcitycontrast', methods=['post', 'get'])
def jobCityContrastPage():
    return render_template('jobcitycontrast.html')

@jobController.route('/jobcityandjobtype', methods=['post', 'get'])
def jobCityAndJobTypePage():
    return render_template('jobcityandjobtype.html')