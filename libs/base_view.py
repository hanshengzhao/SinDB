#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from django.shortcuts import render
from django.views.generic.base import View
from django.http.response import HttpResponse


# 创建类 通用视图
class Add_View(View):
    AddForm = None
    form_title = '添加'
    form_desc = ''
    template_name = 'base/add_or_update_form.html'

    def _handler_item(self, request, item):
        # 为保存前的item 添加属性
        pass

    def get(self, request, *args, **kwargs):
        add_or_update_form = self.AddForm()
        form_title = self.form_title
        form_desc = self.form_desc
        return render(request, self.template_name, locals(), )

    def post(self, request, *args, **kwargs):
        form = self.AddForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            # 特殊添加处理的
            self._handler_item(request, item)
            form.save()
            return HttpResponse("success")
        else:
            print(form.errors)
            return HttpResponse(str(form.errors))


# 删除 通用视图
class Delete_View(View):
    model = None

    def _permission(self, request, *args, **kwargs):
        return True

    def post(self, request, *args, **kwargs):
        record = self.model.objects.get(*args, **kwargs)
        try:
            if self._permission(request, *args, **kwargs):
                record.delete()
            else:
                return HttpResponse('fail')
        except:
            return HttpResponse("fail")
        else:
            return HttpResponse("success")


# 修改 通用视图
class Update_View(View):
    model = None
    form = None
    template_name = 'base/add_or_update_form.html'
    form_title = None
    form_desc = None

    def _permission(self, request, *args, **kwargs):
        return True

    def _handler_item(self, request, item):
        pass

    def get(self, request, *args, **kwargs):
        try:
            if self._permission(request, *args, **kwargs):
                item = self.model.objects.get(*args, **kwargs)
                add_or_update_form = self.form(instance=item)
                return render(request, self.template_name, locals())
            else:
                return render(request, self.template_name, locals())
        except Exception as e:
            print(e)
            return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        item = self.model.objects.get(*args, **kwargs)
        form = self.form(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            # 特殊添加处理的
            self._handler_item(request, item)
            form.save()
            return HttpResponse("success")
        else:
            return HttpResponse(str(form.errors))


def get_buttons_html(buttons_info):
    # 返回按钮的html
    primary_button = buttons_info['primary']
    primary_button_html = '<button type="button" class="btn btn-primary" onclick="{onclick}">{text}</button>'.format(
        onclick=primary_button['onclick'],text=primary_button['text'])
    dropdown_buttons = buttons_info['dropdown_buttons']
    dropdown_buttons_html = ''
    for button in dropdown_buttons:
        dropdown_buttons_html += '<li><a class="font-bold"  href="#" class="font-bold" onclick="{click}">{text}</a></li>'.format(
            click=button['onclick'],text=button['text']
        )

    base_buttons_html = '''<div class="btn-group">
                      {primary_button_html}
                      <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <span class="caret"></span>
                        <span class="sr-only">Toggle Dropdown</span>
                      </button>
                      <ul class="dropdown-menu">
                      {dropdown_primary_button_html}
                      </ul>
                    </div>
                '''.format(primary_button_html=primary_button_html,dropdown_primary_button_html=dropdown_buttons_html)
    return base_buttons_html


