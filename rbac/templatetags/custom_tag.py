#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import re,os
register = template.Library()


def get_structure_data(request):
    """处理菜单结构"""
    menu = request.session[settings.SESSION_GROUP_KEY]
    all_menu = menu[settings.ALL_GROUP_KEY]
    permission_url = menu[settings.PERMISSION_GROUP_KEY]


    # 定制数据结构
    all_menu_dict = {}
    for item in all_menu:
        item['status'] = False
        item['open'] = False
        item['children'] = []
        all_menu_dict[item['id']] = item


    request_rul = request.path_info

    for url in permission_url:
        # 添加两个状态：显示 和 展开
        url['status'] = True
        pattern = url['url']
        if re.match(pattern, request_rul):
            url['open'] = True
        else:
            url['open'] = False

        # 将url添加到菜单下
        all_menu_dict[url['group_id']]["children"].append(url)

        # 显示菜单：url 的菜单及上层菜单 status: true
        pid = url['group_id']
        while pid:
            all_menu_dict[pid]['status'] = True
            pid = all_menu_dict[pid]['parent_id']

        # 展开url上层菜单：url['open'] = True, 其菜单及其父菜单open = True
        if url['open']:
            ppid = url['group_id']
            while ppid:
                all_menu_dict[ppid]['open'] = True
                ppid = all_menu_dict[ppid]['parent_id']

    # 整理菜单层级结构：没有parent_id 的为根菜单， 并将有parent_id 的菜单项加入其父项的chidren内
    menu_data = []
    for i in all_menu_dict:
        if all_menu_dict[i]['parent_id']:
            pid = all_menu_dict[i]['parent_id']
            parent_menu = all_menu_dict[pid]
            parent_menu['children'].append(all_menu_dict[i])
        else:
            menu_data.append(all_menu_dict[i])

    return menu_data


def get_menu_html(menu_data):
    """显示：菜单 + [子菜单] + 权限(url)"""
    option_str = """
              <div class='rbac-menu-item'>
                    <div class='rbac-menu-header'>{menu_title}</div>
                    <div class='rbac-menu-body {active}'>{sub_menu}</div>
                </div>
        """

    url_str = """
            <a href="{permission_url}" class="{active}">{permission_title}</a>
        """
    '''
    menu_data = [
    {
        'id': 1, 
        'title': '老师', 
        'parent_id': None, 
        'status': True, 
        'open': False, 
        'children': [
                        {
                            'title': 'test', 
                            'url': '/test/', 
                            'group_id': 1, 
                            'status': True, 
                            'open': False
                        }, 
                        {
                            'title': 'python正则表达式',
                            'url': '/test/test/', 
                            'group_id': 1, 
                            'status': True, 
                            'open': False
                        }
                    ]
                }
        ]

[{'title': 'test', 'url': '/test/', 'group_id': 1, 'status': True, 'open': False}, {'title': 'python正则表达式', 'url': '/test/test/', 'group_id': 1, 'status': True, 'open': False}]
    '''
    menu_html = ''
    for item in menu_data:
        if not item['status']:  # 如果用户权限不在某个菜单下，即item['status']=False, 不显示
            continue
        else:
            if item.get('url'):  # 说明循环到了菜单最里层的url
                menu_html += url_str.format(permission_url=item['url'],
                                            active="rbac-active" if item['open'] else "",
                                            permission_title=item['title'])
            else:
                menu_html += option_str.format(menu_title=item['title'],
                                               sub_menu=get_menu_html(item['children']),
                                               active="" if item['open'] else "rbac-hide")

    return menu_html


@register.simple_tag
def rbac_menu(request):
    """
    显示多级菜单：
    请求过来 -- 拿到session中的菜单，权限数据 -- 处理数据 -- 作显示
    数据处理部分抽象出来由单独的函数处理；渲染部分也抽象出来由单独函数处理
    """
    menu_data = get_structure_data(request)
    menu_html = get_menu_html(menu_data)

    return mark_safe(menu_html)
    # 因为标签无法使用safe过滤器，这里用mark_safe函数来实现


@register.simple_tag
def rbac_css():
    """
    rabc要用到的css文件路径，并读取返回；注意返回字符串用mark_safe，否则传到模板会转义
    :return:
    """
    css_path = os.path.join('rbac', 'style_script','rbac.css')
    css = open(css_path,'r',encoding='utf-8').read()
    return mark_safe(css)


@register.simple_tag
def rbac_js():
    """
    rabc要用到的js文件路径，并读取返回
    :return:
    """
    js_path = os.path.join('rbac', 'style_script', 'rbac.js')
    js = open(js_path, 'r', encoding='utf-8').read()
    return mark_safe(js)