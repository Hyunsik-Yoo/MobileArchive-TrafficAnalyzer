# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from . import harAnalyzer
from time import localtime, strftime
import sqlite3
from blog.models import Trends
import socket
import ConfigParser

#한글 apk파일 이름 인식을 위해 설정
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

config = ConfigParser.ConfigParser()
config.read("setting.ini")

db_path = config.get("trafficAnalyzer","db_path")
har_path = config.get("trafficAnalyzer","har_path")
pcap_path = config.get("trafficAnalyzer","pcap_path")
mp4_path = config.get("trafficAnalyzer","mp4_path")
HOST = config.get("trafficAnalyzer","HOST")
PORT = config.get("trafficAnalyzer","PORT")


def dashboard(request):
    return render(request, 'blog/dashboard.html')


def index(request):
    return render(request, 'blog/index.html')


def selection_app(request):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT appName, package, imgSrc, apkName FROM list;")
    app_list = c.fetchall()
    c.close()
    conn.close()

    return render(request, 'blog/selection_app.html', {"app_list": app_list})


def after_selection_app(request):

    return render(request, 'blog/index.html',{"app_name":request.POST['app']})

def run_test(request):
    #print(request.POST['app_name'])

    har_name = socket_client(request.POST['app_name'])
    #har_name = har_path + '20170111093716네이버NAVER.har'


    harFile = harAnalyzer.readJsonFile(har_name)

    averageBytesPerPageByContentTypeData = harAnalyzer.averageBytesPerPageByContentTypeData(harFile)
    averageIndividualResponseSizeData = harAnalyzer.averageIndividualResponseSize(harFile)
    imageRequeestsByFormatData = harAnalyzer.imageRequestsByFormat(harFile)
    cacheLifetimeData = harAnalyzer.cacheLifetime(harFile)
    waterfall = harAnalyzer.water_fall(harFile)
    harAnalyzer.insertTrends(request.POST['app_name'], harFile)

    items = Trends.objects.filter(app_name =request.POST['app_name'])

    total_transfer = harAnalyzer.total_transfer(items)
    html_transfer = harAnalyzer.html_transfer(items)
    css_transfer = harAnalyzer.css_transfer(items)
    js_transfer = harAnalyzer.js_transfer(items)
    image_transfer = harAnalyzer.image_transfer(items)
    flash_transfer = harAnalyzer.flash_transfer(items)
    font_transfer = harAnalyzer.font_transfer(items)
    other_transfer = harAnalyzer.other_transfer(items)


    print(total_transfer)

    return render(request,'blog/dashboard.html',
                  {"averageBytesPerPageByContentTypeData": averageBytesPerPageByContentTypeData,
                   "averageIndividualResponseSize": averageIndividualResponseSizeData,
                   "imageRequestsByFormatData": imageRequeestsByFormatData, "cacheLifetimeData": cacheLifetimeData,
                   "total_transfer": total_transfer, "html_transfer":html_transfer, "css_transfer":css_transfer,
                   "js_transfer":js_transfer, "image_transfer":image_transfer, "flash_transfer":flash_transfer,
                   "font_transfer":font_transfer, "other_transfer":other_transfer, "app_name":request.POST['app_name'],
                   "waterfall":waterfall})

def run_auto_test(request):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT appName FROM list;")
    app_list = c.fetchall()
    
    for current_app in app_list:
        har_name = socket_client(current_app[0])
        harFile = harAnalyzer.readJsonFile(har_name)

        averageBytesPerPageByContentTypeData = harAnalyzer.averageBytesPerPageByContentTypeData(harFile)
        averageIndividualResponseSizeData = harAnalyzer.averageIndividualResponseSize(harFile)
        imageRequeestsByFormatData = harAnalyzer.imageRequestsByFormat(harFile)
        cacheLifetimeData = harAnalyzer.cacheLifetime(harFile)
        harAnalyzer.insertTrends(current_app[0], harFile)

        items = Trends.objects.filter(app_name = current_app[0])

        

    return render(request,'blog/index.html')


def socket_client(app_name):

    s = socket.socket()
    s.connect((HOST, int(PORT)))

    s.sendall('runTest') 
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT appName FROM list;")
    app_list = c.fetchall()

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    query = 'SELECT apkName,package FROM list WHERE appName="' + app_name + '"'
    apk_name = c.execute(query).fetchall()[0][0]
    pkg_name = c.execute(query).fetchall()[0][1]

    message = s.recv(1024)
    if message == 'ack':
        s.sendall(pkg_name)

    print('pkg_name was sended')
    message = s.recv(1024)
    if message == 'ack':
        s.sendall(apk_name)

    print('apk_name was sended')
    conn.close()


    #har 파일 수신
    print('write har file')
    file_name = remove_special_characters(app_name)
    har_name = har_path + strftime("%Y%m%d%H%M%S",localtime()) + file_name + '.har'
    f = open(har_name , 'wb')
    data = s.recv(1024)

    while (data):
        if data[len(data) - 8:] == 'finished':
            data = data[:-8]
            f.write(data)
            break
        else:
            f.write(data)
            data = s.recv(1024)
    f.close()
    print('finished transfer')
    

    #pcap 파일 수신
    print('write pcap file')
    f = open(pcap_path + strftime("%Y%m%d%H%M%S",localtime()) + file_name + '.pcap', 'wb')
    data = s.recv(1024)
    while (data):
       if data[len(data) - 8:] == 'finished':
           data = data[:-8]
           f.write(data)
           break
       else:
           f.write(data)
           data = s.recv(1024)
           #print(data)
    f.close()
    print('finished transfer') 


    print('write mp4 file')
    f = open(mp4_path + strftime("%Y%m%d%H%M%S",localtime()) + file_name + '.mp4', 'wb')
    data = s.recv(1024)
    while (data):
       if data[len(data) - 8:] == 'finished':
           data = data[:-8]
           f.write(data)
           break
       else:
           f.write(data)
           data = s.recv(1024)
           #print(data)
    f.close()
    print('finished transfer')

    
    s.close()
    return har_name

def remove_special_characters(input_string):
    input_string = input_string.replace(" ","")
    input_string = input_string.replace("/","")
    input_string = input_string.replace("-","")
    input_string = input_string.replace("(","")
    input_string = input_string.replace(")","")
    input_string = input_string.replace("!","")
    input_string = input_string.replace(":","")
    input_string = input_string.replace("[","")
    input_string = input_string.replace("]","")
    input_string = input_string.replace("&","")
    input_string = input_string.replace(",","")

    return input_string






