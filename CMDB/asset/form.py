#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.forms import ModelForm
from django import forms
from asset.models import *


class EnvironmentForm(ModelForm):
    """
    环境信息form
    """
    class Meta:
        model = Environment
        fields = "__all__"  # 对所有字段转换
        widgets = {

            'name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'abs_name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'note': forms.TextInput(
                attrs={'class': 'form-control'}),
        }
        # <input type="text" name="name" class="form-control" maxlength="32" required id="id_name">
        # 前端已经根据models.py中的设置进行了设置，输入的时候会发现只能最多输入32个字符
        # error_messages = {
        #     'name': {'invalid': "name无效", "max_length": "太长了"},
        #     'abs_name': {'invalid': "name无效", },
        #     'note': {'invalid': "name无效", },
        #
        # }


class SystemForm(ModelForm):
    """
    系统信息form
    """

    class Meta:
        model = System
        fields = "__all__"  #

        widgets = {

            'name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'abs_name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'note': forms.TextInput(
                attrs={'class': 'form-control'}),
            'operate_person': forms.Select(
                attrs={'class': 'form-control'}),
            'environment': forms.SelectMultiple(
                attrs={
                    'class': 'form-control'})
        }


class ApplicationForm(ModelForm):
    """
    应用信息form
    """
    class Meta:
        model = Application
        fields = "__all__"  # 对所有字段转换
        widgets = {

            'middleware': forms.TextInput(
                attrs={'class': 'form-control'}),
            'name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'log_path': forms.TextInput(
                attrs={'class': 'form-control'}),
            'start_script': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': "ansible不支持tail -f 实时命令,ansible执行脚本时会自动去除"}),
            'stop_script': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': "ansible不支持tail -f 实时命令,ansible执行脚本时会自动去除"}),
            'restart_script': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': "ansible不支持tail -f 实时命令,ansible执行脚本时会自动去除"}),
            'access_url': forms.TextInput(
                attrs={'class': 'form-control'}),
            'note': forms.TextInput(
                attrs={'class': 'form-control'}),
        }


class DateInput(forms.DateInput):
    """
    事件字段渲染到前端，还是为input标签
    这样设置后，会出现时间选择器
    """
    input_type = 'date'


class HostLoginUserForm(ModelForm):
    """
    主机登录用户信息form
    """
    # key_file = forms.FileField(label="私钥文件",
    #                            required=False,
    #                            widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = HostLoginUser
        fields = "__all__"  # 对所有字段转换
        widgets = {

            'name_info': forms.TextInput(
                attrs={'class': 'form-control'}),
            'name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'password': forms.TextInput(
                attrs={'class': 'form-control'}),
            'expire_date': DateInput(attrs={'class': 'form-control'}),
        }


class HostForm(ModelForm):
    """
    主机登录用户信息form
    """
    # key_file = forms.FileField(label="私钥文件",
    #                            required=False,
    #                            widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Host
        fields = "__all__"  # 对所有字段转换
        widgets = {

            'ip': forms.TextInput(
                attrs={'class': 'form-control'}),
            'port': forms.TextInput(
                attrs={'class': 'form-control'}),
            'note': forms.TextInput(
                attrs={'class': 'form-control'}),
            'MAC': forms.TextInput(
                attrs={'class': 'form-control'}),
            'hostname': forms.TextInput(
                attrs={'class': 'form-control'}),
            'expire_date': DateInput(attrs={'class': 'form-control'}),
            'cpu': forms.TextInput(
                attrs={'class': 'form-control'}),
            'disk': forms.TextInput(
                attrs={'class': 'form-control'}),
            'mem': forms.TextInput(
                attrs={'class': 'form-control'}),
            'operate_person': forms.Select(
                attrs={'class': 'form-control'}),
            'system': forms.Select(
                attrs={'class': 'form-control'}),
            'environment': forms.Select(
                attrs={'class': 'form-control'}),
            'application': forms.SelectMultiple(
                attrs={'class': 'form-control'}),
            'login_user': forms.SelectMultiple(
                attrs={
                    'class': 'form-control'}),
        }
        error_messages = {
            'mem': {'invalid': "无效的输入", },
            'cpu': {'invalid': "无效的输入", },
            'disk': {'invalid': "无效的输入", },

        }
