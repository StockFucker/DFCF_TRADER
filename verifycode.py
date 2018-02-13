#!/usr/bin/env python
#-*- coding:utf-8 -*-

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print '模块导入错误,请使用pip安装,pytesseract依赖以下库：'
    print 'http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil'
    print 'http://code.google.com/p/tesseract-ocr/'
    raise SystemExit

#将图片放到内存中
import cStringIO,  requests, random , string
# import matplotlib.pyplot as plt
import sys
import urllib, urllib2, sys
import base64
import json

class VerifyCode(object):
    def __init__(self):
        self.s = requests.session()
        
    def get_verify_code(self,url_yzm):
        #url ="http://www.qqct.com.cn/console/captcha"

        img = Image.open(cStringIO.StringIO(self.s.get(url_yzm).content))
        buffer = cStringIO.StringIO()
        img.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue())
        '''
        im_1=img.crop((10,0,85,35)) #crop() : 从图像中提取出某个矩形大小的图像。它接收一个四元素的元组作为参数，
                            #各元素为（left, upper, right, lower），坐标系统的原点（0, 0）是左上角。
        imgry = img.convert('L')
        #imgry.show()
        threshold = 190  
        table = []  
        for i in range(256):  
            if i < threshold:  
                table.append(0)  
            else:  
                table.append(1) 
        out = imgry.point(table,'1')        
        #print im.format, im.size, im.mode
        #im.show()
        '''
        try:
            host = 'http://jisuyzmsb.market.alicloudapi.com'
            path = '/captcha/recognize'
            method = 'POST'
            appcode = '6349909e80664219a6b6a3d580c05687'
            querys = 'type=n4'
            bodys = {}
            url = host + path + '?' + querys

            bodys['pic'] = img_str
            post_data = urllib.urlencode(bodys)
            request = urllib2.Request(url, post_data)
            request.add_header('Authorization', 'APPCODE ' + appcode)
            # //根据API的要求，定义相对应的Content-Type
            request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            response = urllib2.urlopen(request)
            content = json.loads(response.read())
            vcode = content["result"]["code"]
            return vcode
        except Exception, e:
            print e
            host = 'http://op.juhe.cn'
            path = '/captcha/recognize'
            method = 'GET'
            querys = 'codeType=4004&key=5d0d9d396af4b72b71d251b5cf700319&base64Str=' + img_str
            bodys = {}
            url = host + path + '?' + querys

            bodys['pic'] = img_str
            post_data = urllib.urlencode(bodys)
            request = urllib2.Request(url, post_data)
            # request.add_header('Authorization', 'APPCODE ' + appcode)
            # //根据API的要求，定义相对应的Content-Type
            # request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            response = urllib2.urlopen(request)
            content = json.loads(response.read())
            vcode = content["result"]
            return vcode
        

# def download_images():
#     randNum="%.16f" % float(random.random())
#     url_yzm="https://jy.xzsec.com/Login/YZM?randNum=" + randNum
#     test = VerifyCode()
#     for i in range(0,100):
#     image = Image.open(cStringIO.StringIO(self.s.get(url_yzm).content))
#     image.write(label, os.path.join(gen_dir, label+'_num'+str(i)+'.png'))


if __name__=="__main__":
    randNum="%.16f" % float(random.random())
    url_yzm="https://jy.xzsec.com/Login/YZM?randNum=" + randNum
    test=VerifyCode()
    vcode = test.get_verify_code(url_yzm)
    print vcode