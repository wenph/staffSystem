#coding=cp936
__author__ = 'admin'

# 职称
TITLE_NAME_LIST = [u'教授', u'副教授', u'工程师']
# 职位
POSITION_NAME_LIST = [u'科长', u'副科长', u'小弟']
# 学历
EDUCATION_NAME_LIST = [u'博士后', u'博士', u'硕士', u'大学本科', u'大学专科', u'高中', u'初中', u'小学']
# 项目来源
SOURCE_PLACE_NAME_LIST = [u'国家', u'企业']

# 员工页面的列名
STAFF_COLUMN = [
    u'ID',
    u'姓名',
    u'工号',
    u'手机',
    u'电话',
    u'出生年月',
    u'职称',
    u'职位',
    u'学历',
    u'正在进行的项目',
    u'本月出差天数'
]
# 员工搜索列名
STAFF_SEARCH_COLUMN = [
    u'姓名',
    u'项目',
    u'开始时间',
    u'结束时间',
    u'参与此项目人员'
]
# 工程页面的列名
PROJECT_COLUMN = [
    u'ID',
    u'工程名称',
    u'检索号',
    u'来源',
    u'主设人',
    u'设总',
    u'负责主工',
    u'开始时间',
    u'结束时间',
    u'参加人员'
]