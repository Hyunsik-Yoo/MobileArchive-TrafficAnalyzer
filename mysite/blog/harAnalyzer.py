#-*- coding: utf-8 -*-
import json
import numpy
import datetime
import time
from .models import Trends
from django.shortcuts import get_object_or_404

def readJsonFile(fileName):
    f = open(fileName, 'r')
    js = json.loads(f.read())

    return js





def insertTrends(name,js):

    _app_name = name
    total_transfer = 0
    total_requests = 0

    html_transfer = 0
    html_request = 0

    js_transfer = 0
    js_request = 0

    css_transfer = 0
    css_request = 0

    image_transfer = 0
    image_request = 0

    flash_transfer = 0
    flash_request = 0

    font_transfer = 0
    font_request = 0

    other_transfer = 0
    other_request = 0

    for entry in js['log']['entries']:
        contentType = entry["response"]["content"]["mimeType"]
        size = int(entry["response"]["content"]["size"])

        if contentType.split('/')[0]=="image" :
            image_request += 1
            image_transfer += size

        elif contentType.split('/')[0] == "application":
            js_request +=1
            js_transfer += size

        elif contentType.split('/')[1] == "html":
            html_request += 1
            html_transfer += size
        
        elif contentType.split('/')[1] == "css":
            css_request += 1
            css_transfer += size

        elif contentType.split('/')[0] == "font":
            font_request += 1
            font_transfer += size

        else:
            other_request += 1
            other_transfer +=size

        total_requests += 1
        total_transfer += size

    print ('before create object')
    item = Trends(app_name=_app_name, total_transfer_size = total_transfer, total_requests = total_requests, html_transfer_size= html_transfer,
                  html_requests = html_request, js_transfer_size=js_transfer, js_requests=js_request, css_transfer_size=css_transfer, css_requests=css_request,
                  image_transfer_size=image_transfer, image_requests=image_request, flash_transfer_size=flash_transfer, flash_requests=flash_request,
                  font_transfer_size=font_transfer, font_requests=font_request, other_transfer_size=other_transfer, other_requests=other_request)
    print ('after create object')
    item.save()


    return True

def water_fall(js):
    # url, html, start time, dns, connect, ssl
    # html_request, html_response, js_request, js_response
    # css_request, css_response, image_request, image_response
    # flash_request, flash_response, font_request, font_response
    # other_request, other_response
    result = []
    firstTime = js['log']['entries'][0]['startedDateTime']
    firstTime = datetime.datetime.strptime(firstTime,'%Y-%m-%dT%H:%M:%S.%fZ')

    for entry in js['log']['entries']:
        tooltip = getTooltip(entry) # tooltip 안에 들어가는 내용을 HTML형태로...
        startedDateTime = entry['startedDateTime']
        endedDateTime = entry['endedDateTime']

        start = datetime.datetime.strptime(startedDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        end = datetime.datetime.strptime(endedDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')

        startTime = start - firstTime
        #totalTime = int(entry['time']) * 0.001 #ms이므로 다시 초로 환산
        url = entry['request']['url']

        dns = entry['timings']['dns'] * 0.001
        connect = entry['timings']['connect'] * 0.001
        ssl = 0
        contentType = entry['response']['content']['mimeType']
        contentType = contentType.split('/')

        if (contentType[0] == "image"):
            image_request = entry['timings']['wait'] * 0.001
            image_response = entry['timings']['receive'] * 0.001
        else:
            image_request = 0
            image_response = 0

        if (contentType[1] == "javascript"):
            js_request = entry['timings']['wait'] * 0.001
            js_response = entry['timings']['receive'] * 0.001
        else:
            js_request = 0
            js_response = 0

        if (contentType[1] == "html"):
            html_request = entry['timings']['wait'] * 0.001
            html_response = entry['timings']['receive'] * 0.001
        else:
            html_request = 0
            html_response = 0

        if (contentType[1] == "css"):
            css_request = entry['timings']['wait'] * 0.001
            css_response = entry['timings']['receive'] * 0.001
        else:
            css_request = 0
            css_response = 0

        if (contentType[1] == 'plain'):
            text_request = entry['timings']['wait'] * 0.001
            text_response = entry['timings']['receive'] * 0.001
        else:
            text_request = 0
            text_response = 0

        if (contentType[1] == 'xml'):
            xml_request = entry['timings']['wait'] * 0.001
            xml_response = entry['timings']['receive'] * 0.001
        else:
            xml_request = 0
            xml_response = 0

        if (contentType[1] == 'octet-stream'):
            octet_request = entry['timings']['wait'] * 0.001
            octet_response = entry['timings']['receive'] * 0.001
        else:
            octet_request = 0
            octet_response = 0

        if(contentType[1] == 'json'):
            json_request = entry['timings']['wait'] * 0.001
            json_response = entry['timings']['receive'] * 0.001
        else:
            json_request = 0
            json_response = 0

        #TODO : other 어떻게 처리하지?
        #other_request = entry['timings']['wait']
        #other_response = entry['timings']['receive']


        result.append([str(url), str(tooltip), startTime.total_seconds(), dns, connect, ssl, html_request, html_response,
            js_request, js_response, css_request, css_response, image_request, image_response, text_request, text_response,
            xml_request, xml_response, octet_request, octet_response, json_request, json_response])

        print (str(url), connect)


    return result

def getTooltip(entry):
    """
    URL:
    Host: img.naver.net
    IP: 101.79.247.157
    Error/Status Code: 200
    Client Port: 64780
    Request Start: 1.619 s
    Time to First Byte: 76 ms
    Content Download: 131 ms
    Bytes In (downloaded): 9.4 KB
    Bytes Out (uploaded): 0.4 KB
    """
    result = dict()
    result['url'] = entry['request']['url']
    headers = entry['request']['headers']

    for header in headers:
        if header['name'] == 'host':
            result['host'] = header['value']
    result['status'] = entry['response']['status']
    result['firstbyte'] = int(entry['timings']['connect']) + int(entry['timings']['wait'])
    result['receive'] = int(entry['timings']['receive'])
    result['byteIn'] = int(entry['response']['content']['size'])

    return "<p><br>URL: </br>"+str(result['url'])+"</p>" + "<p><br>Host: " + str(result['host']) + "</p>" + "<p><br>Error/Status Code: " + str(result['status']) + "</p>" + "<p><br>Time to First Byte: " + str(result['firstbyte']) + "</p>" + "<p><br>Content Download: " + str(result['receive']) + "</p>"


def averageBytesPerPageByContentTypeData(js):

    totlaSize = 0
    htmlSize = list()
    stylesheetsSize = list()
    imageSize = list()
    scriptSize = dict()


    for packet in js["log"]["entries"]:
        contentType = packet["response"]["content"]["mimeType"]
        size = int(packet["response"]["content"]["size"])

        if (contentType.split('/')[0] == "image"):
            imageSize.append(size)

        elif (contentType.split('/')[0] == "application"):
            item_type = contentType.split('/')[1]
            if item_type in scriptSize.keys():
                scriptSize[item_type].append(size)
            else:
                scriptSize[item_type] = list()

        elif (contentType.split('/')[1] == "html"):
            htmlSize.append(size)

        elif (contentType.split('/')[1] == "css"):
            stylesheetsSize.append(size)

        totlaSize = totlaSize + size

    imageSize = round(sum(imageSize) / 1024)
    for item in scriptSize:
        scriptSize[item] = round(sum(scriptSize[item]) / 1024)
    stylesheetsSize = round(sum(stylesheetsSize) / 1024)
    htmlSize = round(sum(htmlSize) / 1024)

    result = [["Type", "Size"], ["image - " + str(imageSize) + "KB", imageSize],
              ["stylesheet - " + str(stylesheetsSize) + "KB", stylesheetsSize],["html - " + str(htmlSize) + "KB", htmlSize]]


    for item in scriptSize.items():
        print [str(item[0])+" - "+str(item[1])+"KB", item[1]]
        result.append([str(item[0])+" - "+str(item[1])+"KB", item[1]])


    return result


#fileName = "/Users/macgongmon/Desktop/untitled/test.har"
#f = open(fileName, 'r')
#js = json.loads(f.read())


def averageIndividualResponseSize(js):
    htmlSize = list()
    imageSize = dict()
    stylesheetsSize = list()
    scriptSize = dict()


    for packet in js["log"]["entries"]:
        contentType = packet["response"]["content"]["mimeType"]
        size = int(packet["response"]["content"]["size"])

        if (contentType.split('/')[0] == "image"):
            item_type = contentType.split('/')[1]
            if item_type in imageSize.keys():
                imageSize[item_type].append(size)
            else:
                imageSize[item_type] = list()

        elif(contentType.split('/')[0] == "application"):
            item_type = contentType.split('/')[1]
            if item_type in scriptSize.keys():
                scriptSize[item_type].append(size)
            else:
                scriptSize[item_type] = list()

        elif(contentType.split('/')[1] == "html"):
            htmlSize.append(size)

        elif(contentType.split('/')[1] == "css"):
            stylesheetsSize.append(size)


    print ('stylesheetsSize : ',stylesheetsSize)
    print ('htmlSize : ', htmlSize)
    print ('iagmeSize : ',imageSize)
    print ('scriptSize : ',scriptSize)

    if len(stylesheetsSize)!= 0:
        stylesheetsSize = round(numpy.mean(stylesheetsSize)/1024)
    else:
        stylesheetsSize = 0

    if len(htmlSize)!= 0:
        htmlSize = round(numpy.mean(htmlSize)/1024)
    else:
        htmlSize = 0


    for item in imageSize:
        if len(imageSize[item]) != 0:
            imageSize[item] = round(numpy.mean(imageSize[item]) / 1024)
        else:
            imageSize[item] = 0

    for item in scriptSize:
        if len(scriptSize[item]) != 0:
            scriptSize[item] = round(numpy.mean(scriptSize[item]) / 1024)
        else:
            scriptSize[item] = 0


    result = [["Type","Size",] , ["css - " + str(stylesheetsSize) + "KB", stylesheetsSize],
          ["html - "+str(htmlSize)+"KB",htmlSize]]

    for item in scriptSize.items():
        print [str(item[0])+" - "+str(item[1])+"KB", item[1]]
        result.append([str(item[0])+" - "+str(item[1])+"KB", item[1]])

    for item in imageSize.items():
        print [str(item[0])+" - "+str(item[1])+"KB", item[1]]
        result.append([str(item[0])+" - "+str(item[1])+"KB", item[1]])
    print (result)
    return result



def imageRequestsByFormat(js):
    gifSize = 0
    jpgSize = 0
    pngSize = 0
    webpSize = 0
    svgSize = 0
    otherSize = 0

    for packet in js["log"]["entries"]:
        contentType = packet["response"]["content"]["mimeType"]
        #size = int(packet["response"]["content"]["size"])

        if (contentType.split('/')[0] == "image"):
            if (contentType.split('/')[1] == "gif"):
                gifSize = gifSize + 1

            elif (contentType.split('/')[1] == "png"):
                pngSize = pngSize + 1

            elif (contentType.split('/')[1] == "jpeg"):
                jpgSize = jpgSize + 1

            elif (contentType.split('/')[1] == "webp"):
                webpSize = webpSize + 1

            elif (contentType.split('/')[1] == "svg"):
                svgSize = svgSize + 1
            else:

                otherSize = otherSize + 1

    print ("gif : ", gifSize)
    print ("png : ", pngSize)
    print ("jpg : ", jpgSize)
    print ("css : ", webpSize)
    print ("html : ", svgSize)
    print ("script : ", otherSize)

    result = [["Type","Size"], ["gif " + str(gifSize), gifSize], ["png " + str(pngSize), pngSize], ["jpg " + str(jpgSize), jpgSize],
              ["Webp " + str(webpSize), webpSize], ["svg " + str(svgSize), svgSize], ["other " + str(otherSize), otherSize]]

    return result


def cacheLifetime(js):
    timezone1 = 0
    timezone2 = 0
    timezone3 = 0
    timezone4 = 0
    timezone5 = 0

    print ("len headers :" + str(len(js["log"]["entries"])))
    for packet in js["log"]["entries"]:

        headers = packet["response"]["headers"]
        for header in headers:
            if (header["name"] == "Cache-Control"):
                value = header["value"]
                value = value.split("max-age=")

                if (len(value) == 1):
                    continue

                value = int(value[1])
                print (value)

                if (value == 0):
                    timezone1 = timezone1 + 1
                elif (value > 0 and value <= 86400):
                    timezone2 = timezone2 + 1
                elif (value > 86400 and value <= 2592000):
                    timezone3 = timezone3 + 1
                elif (value > 2592000 and value <= 31536000):
                    timezone4 = timezone4 + 1
                elif (value > 31536000):
                    timezone5 = timezone5 + 1
                else:
                    print (value)

    total = timezone1 + timezone2 + timezone3 + timezone4 + timezone5
    if total !=0:
        timezone1 = round(float(timezone1) / total * 100, 1)
        timezone2 = round(float(timezone2) / total * 100, 1)
        timezone3 = round(float(timezone3) / total * 100, 1)
        timezone4 = round(float(timezone4) / total * 100, 1)
        timezone5 = round(float(timezone5) / total * 100, 1)

    result = [["Type", "Percentage"], ["t = 0", timezone1], ["0 < t <=1", timezone2], ["1 < t <= 30", timezone3],
              ["30 < t <= 365", timezone4], ["t > 365", timezone5]]

    return result


def total_transfer(objects):
    result = []

    for item in objects:
        result.append([float(item.date), int(item.total_transfer_size/1024), int(item.total_requests)])

    return result


def html_transfer(objects):
    result = []

    for item in objects:
        result.append([float(item.date), int(item.html_transfer_size/1024), int(item.html_requests)])

    return result


def js_transfer(objects):
    result = []

    for item in objects:
        result.append([float(item.date), int(item.js_transfer_size / 1024), int(item.js_requests)])

    return result


def css_transfer(objects):
    result = []

    for item in objects:
        result.append([float(item.date), int(item.css_transfer_size / 1024), int(item.css_requests)])

    return result


def image_transfer(objects):
    result = []

    for item in objects:
        result.append([float(item.date), int(item.image_transfer_size / 1024), int(item.image_requests)])

    return result


def flash_transfer(objects):
    result = []

    for item in objects:
        result.append([float(item.date), int(item.flash_transfer_size / 1024), int(item.flash_requests)])

    return result


def font_transfer(objects):
    result = []

    for item in objects:
        result.append([float(item.date), int(item.font_transfer_size / 1024), int(item.font_requests)])

    return result


def other_transfer(objects):
    result = []

    for item in objects:
        result.append([float(item.date), int(item.other_transfer_size / 1024), int(item.other_requests)])

    return result


    

