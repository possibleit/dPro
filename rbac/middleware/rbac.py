#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf import settings
from django.shortcuts import HttpResponse,redirect
import re

class MiddlewareMixin(object):
    def __init__(self,get_response = None):
        self.get_response = get_response
        super(MiddlewareMixin,self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self,'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self,'process_response'):
            response = self.process_response(request,response)
        return response

class RbacMiddleware(MiddlewareMixin):
    def process_request(self,request):
        request_url = request.path_info
        permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
        print('访问url',request_url)
        print('权限--',permission_url)
        for url in settings.SAFE_URL:
            if re.match(url,request_url):
                return None

        if not permission_url:
            return redirect(settings.LOGIN_URL)

        flag = False
        for url in permission_url:
            url_pattern = settings.REGEX_URL.format(url=url)
            if re.match(url_pattern,request_url):
                flag = True
                break
        if flag:
            return None
        else:
            if settings.DEBUG:
                info = '<br/>' + ('<br/>'.join(permission_url))
                return HttpResponse('无权限，请尝试访问以下地址：%s'%info)
            else:
                return HttpResponse('无权限')