from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import auth
import json
from app.models import *


def login(request):
    # 登录函数
    if request.method == "POST":
        res = {"user": None, "info": None}
        # 获取前端传过来的数据
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user_obj = User.objects.filter(username=user)
        # 用户存在
        if user_obj:
            # 验证用户名和密码是否正确
            auth_user_obj = auth.authenticate(username=user, password=pwd)
            if auth_user_obj:
                # 验证通过
                auth.login(request, auth_user_obj)

                res["user"] = user
                # 登录成功后，设置返回首页的url,由于多处使用，所以防在了session中
                request.session["back_url"] = "/index/"

            else:
                res["user"] = user
                res["info"] = "密码错误！"

        else:
            # 用户不存在时
            res["info"] = "用户不存在！"
        #     这种方式可以传中文到前端
        return JsonResponse(res)

    return render(request, "login.html")


@login_required
def register(request):
    # 注册函数
    if request.method == "POST":
        res = {"user": None, "info": None}
        # 获取前端传过来的用户名与密码
        user = request.POST.get("user").strip()
        pwd = request.POST.get("pwd").strip()
        # 验证前端传过来的数据
        if user == "" or pwd == "":
            res["info"] = "user or password can not be null!"
            return HttpResponse(json.dumps(res))
        # 到数据库中获取用户信息
        user_obj = User.objects.filter(username=user)

        # 如果该用户已经存在，返回信息，不存在，插入该用户信息到数据库
        if user_obj:
            res["info"] = "user already exist!"

            return HttpResponse(json.dumps(res))
        # 用户不存在，就创建该用户
        User.objects.create_user(username=user, password=pwd)
        # 创建成功
        res["user"] = user
        # 这种方式不能传中文，前端会解析报错
        return HttpResponse(json.dumps(res))

# 需要auth.login()之后，才允许登录。auth.login会设置相关信息到session中
@login_required
def index(request):
    # 展示信息页面
    logout_url = "/logout/"
    author_list = Author.objects.all()
    publish_list = Publish.objects.all()
    return render(request, "index.html", locals())


@login_required
def logout(request):
    # 退出登录，删除session,cookie信息
    auth.logout(request)
    return redirect("/login/")


@login_required
def add_author(request):
    # 添加作者信息
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        author_name = request.POST.get("author_name").strip()
        author_age = request.POST.get("author_age").strip()
        # 验证前端传过来的数据
        if author_name == "" or author_age == "":
            res["info"] = "作者名或年龄不能为空"
        elif not author_age.isnumeric():
            res["info"] = "年龄必须是数字"
        else:
            try:
                Author.objects.create(name=author_name, age=author_age)
                res["success"] = True
                res["info"] = "%s 作者添加成功" % author_name
            except Exception as e:
                print(e)
                res["info"] = "插入数据报错，请查看端日志！"
        return JsonResponse(res)


@login_required
def edit_author(request, author_id):
    # 编辑作者信息
    author_id = int(author_id)
    author_obj = Author.objects.get(id=author_id)
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        author_name = request.POST.get("author_name").strip()
        author_age = request.POST.get("author_age").strip()
        # 验证前端传过来的数据
        if author_name == "" or author_age == "":
            res["info"] = "作者名或年龄不能为空"
        elif not author_age.isnumeric():
            res["info"] = "年龄必须是数字"
        else:
            try:
                Author.objects.filter(id=author_id).update(name=author_name, age=author_age)
                res["success"] = True
                res["info"] = "%s 作者修改成功" % author_name
            except Exception as e:
                print(e)
                res["info"] = "更新数据报错，请查看端日志！"
        return JsonResponse(res)
    return render(request, "author_edit.html", locals())


@login_required
def show_author(request, author_id):
    # 列出选择的作者出版了哪些书
    author_id = int(author_id)
    author_obj = Author.objects.get(id=author_id)
    author_book_list = Book.objects.filter(authors__id=author_id)

    return render(request, "author_book.html", locals())


@login_required
def del_author(request, author_id):
    # 删除作者信息
    Author.objects.get(id=author_id).delete()
    return redirect("/index/")


@login_required
def add_publish(request):
    # 插入出版社信息
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        publish_name = request.POST.get("publish_name").strip()
        publish_city = request.POST.get("publish_city").strip()
        publish_email = request.POST.get("publish_email").strip()
        # 验证前端传过来的数据
        if publish_name == "" or publish_city == "" or publish_email == "":
            res["info"] = "出版社名字-城市-邮箱不能为空哦！"
        elif not publish_email.__contains__("@"):
            res["info"] = "出版社邮箱格式错误！"
        elif Publish.objects.filter(name=publish_name, city=publish_city):
            res["info"] = "同样的城市中出版社只能有一个"
        else:
            # 插入数据可能报错
            try:
                Publish.objects.create(name=publish_name, city=publish_city, email=publish_email)
                res["success"] = True
                res["info"] = "%s 出版社添加成功" % publish_name
            except Exception as e:
                print(e)
                res["info"] = "插入数据报错，请查看端日志！"

        return JsonResponse(res)


@login_required
def edit_publish(request, publish_id):
    # 编辑出版社信息
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        publish_name = request.POST.get("publish_name").strip()
        publish_city = request.POST.get("publish_city").strip()
        publish_email = request.POST.get("publish_email").strip()
        # 验证前端传过来的数据
        if publish_name == "" or publish_city == "" or publish_email == "":
            res["info"] = "出版社名字-城市-邮箱不能为空哦！"
        elif not publish_email.__contains__("@"):
            res["info"] = "出版社邮箱格式错误！"
        elif Publish.objects.filter(name=publish_name, city=publish_city):
            res["info"] = "同样的城市中出版社只能有一个"
        else:
            # 插入数据可能报错
            try:
                Publish.objects.filter(id=publish_id).update(name=publish_name, city=publish_city, email=publish_email)
                res["success"] = True
                res["info"] = "%s 出版社编辑成功" % publish_name
            except Exception as e:
                print(e)
                res["info"] = "修改数据报错，请查看端日志！"

        return JsonResponse(res)
    
    # get请求时
    publish_obj = Publish.objects.get(id=publish_id)
    
    return render(request, "publish_edit.html", locals())


@login_required
def show_publish(request, publish_id):
    # 展示出版社出版的书籍信息
    publish_obj = Publish.objects.get(id=publish_id)
    publish_book_list = Book.objects.filter(publish__id=publish_id)
    return render(request, "publish_book.html", locals())


@login_required
def del_publish(request, publish_id):
    # 删除出版社信息
    Publish.objects.get(id=publish_id).delete()
    return redirect("/index/")