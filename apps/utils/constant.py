#coding=cp936
__author__ = 'admin'
import datetime

# ְ��
TITLE_NAME_LIST = [u'����', u'������', u'����ʦ']
# ְλ
POSITION_NAME_LIST = [u'�Ƴ�', u'���Ƴ�', u'С��']
# ѧ��
EDUCATION_NAME_LIST = [u'��ʿ��', u'��ʿ', u'˶ʿ', u'��ѧ����', u'��ѧר��', u'����', u'����', u'Сѧ']
# ��Ŀ��Դ
SOURCE_PLACE_NAME_LIST = [u'����', u'��ҵ']

# Ա��ҳ�������
STAFF_COLUMN = [
    u'ID',
    u'����',
    u'����',
    u'�ֻ�',
    u'�绰',
    u'��������',
    u'ְ��',
    u'ְλ',
    u'ѧ��',
    u'���ڽ��е���Ŀ',
    u'���³�������',
    u'��ע'
]
# Ա����������
STAFF_SEARCH_COLUMN = [
    u'����',
    u'��Ŀ',
    u'��ʼʱ��',
    u'����ʱ��',
    u'�������Ŀ��Ա',
    u'����������'
]
# ����ҳ�������
PROJECT_COLUMN = [
    u'ID',
    u'��������',
    u'������',
    u'��Դ',
    u'������',
    u'����',
    u'��������',
    u'��ʼʱ��',
    u'����ʱ��',
    u'�μ���Ա',
    u'��ע'
]

today = datetime.date.today()
first = datetime.date(day=1, month=today.month, year=today.year)
lastMonth = first - datetime.timedelta(days=1)
ONE_MONTH_TIME = {
    'start_time': datetime.date(day=20, month=lastMonth.month, year=lastMonth.year),
    'end_time': datetime.date(day=today.day if today.day <= 20 else 20, month=today.month, year=today.year)
}