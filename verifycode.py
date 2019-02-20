#!/usr/bin/env python
#-*- coding:utf-8 -*-

try:
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

# coding=utf-8
import sys
import requests
from apig_sdk import signer
from fateadm_api import *

class VerifyCode(object):
    def __init__(self):
        self.s = requests.session()

    def get_verify_code(self,url_yzm):
        #url ="http://www.qqct.com.cn/console/captcha"

        img = Image.open(cStringIO.StringIO(self.s.get(url_yzm).content))
        buffer = cStringIO.StringIO()
        img.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue())
        # img.save("log/img.png")
        try:
            sig = signer.Signer()
            sig.AppKey = "69a2b70f68e8457ab612083fa3dbccce"
            sig.AppSecret = "04779878ab2042dfaa00f2ec06b9336c"

            r = signer.HttpRequest()
            r.scheme = "http"
            r.host = "yscheckcode.apistore.huaweicloud.com"
            r.method = "POST"
            r.uri = "/checkCode/ys/"
            r.query = {'typeId':'14','needMorePrecise':'0','convert_to_jpg':'0','img_base64':img_str}
            r.headers = {"x-stage": "RELEASE"}
            sig.Sign(r)
            resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
            content = json.loads(resp.content)
            vcode = content["showapi_res_body"]["Result"]
            return vcode
        except Exception, e:
            print(e)
            return self.get_verify_code2(img_str)
            # line = sys.stdin.readline().strip('\n')   # 一次只读一行
            # return line

    def get_verify_code2(self,img_str):
        try:
            pd_id          = "109900";
            pd_key         = "2Pe+zgn0/PQ7+ahjIc7x76Gwiihgv07l";
            pred_type      = "10400";
            api            = FateadmApi(None, None, pd_id, pd_key);
            rsp            = api.Predict( pred_type, img_str);
            return rsp.pred_rsp.value
        except Exception as e:
            print(e)
            return self.get_verify_code3(img_str)

    def get_verify_code3(self,img_str):
        try:
            rc = RClient('sgcy1991', 'a1991311', '123064', '62842c265d2849408a4bd84f15e22959')
            result = rc.rk_create(img_str, 1040)
            return result["Result"]
        except Exception as e:
            print(e)
            line = sys.stdin.readline().strip('\n')   # 一次只读一行
            return line



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
