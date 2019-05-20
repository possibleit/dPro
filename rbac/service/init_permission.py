#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from ..models import PermissionGroup,User

def init_permission(request,user_obj):
    permission_item_list = user_obj.roles.values('permission_url',
                                           'permission_title',
                                           'permission_Group_id',).distinct()
    permission_url_list = []
    permission_group_list = []

    for item in permission_item_list:
        permission_url_list.append(item['permission_url'])
        if item['perssion_Group_id']:
            temp = {'title':item['permission_title'],
                    'url':item['permission_url'],
                    'group_id':item['permission_Group_id'],}
            permission_group_list.append(temp)

    group_list = list(PermissionGroup.objects.values('id','title','parent_id'))

    from django.conf import settings

    request.session[settings.SESSION_PERMISSION_URL_KEY] = permission_url_list

    request.session[settings.SESSION_GROUP_KEY] = {
        settings.ALL_GROUP_KEY : group_list,
        settings.PERMISSION_GROUP_KEY : permission_group_list,
    }

