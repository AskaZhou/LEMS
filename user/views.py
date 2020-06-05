from django.shortcuts import render
from django.http import JsonResponse
from . import models
from django.contrib.auth.hashers import make_password, check_password


# 主页
def index(request):
    return render(request, 'user/index.html')


# 注册
def register(request):
    userName = request.POST['userName']
    userNum = request.POST['userNum']
    useride = request.POST['useride']
    userPhone = request.POST['userPhone']
    userPwd1 = request.POST['userPwd1']
    userPwd2 = request.POST['userPwd2']

    # 判断两次密码是否一致
    if userPwd1 != userPwd2:
        return JsonResponse({"code": 1})
    # 判断输入是否合法
    try:
        int(userPhone)
        int(userNum)
    except ValueError:
        return JsonResponse({"code": 4})

    # 通过学号判断用户是否已经注册
    if models.User.objects.filter(userNum=userNum):
        return JsonResponse({"code": 2})

    # 通过电话号判断用户是否已经注册
    if models.User.objects.filter(userPhone=userPhone):
        return JsonResponse({"code": 5})
    else:
        # 注册信息
        if useride == "教师" and userNum != "0" and userNum != "1" and (not models.Teacher.objects.filter(tPhone=userPhone)):
            models.Teacher.objects.create(tName=userName, tPhone=userPhone)
        models.User.objects.create(userName=userName, userNum=userNum, userPhone=userPhone,
                                   useride=useride, userPwd=make_password(userPwd1))
        return JsonResponse({"code": 3})


# 登录验证
def checklogin(request):
    userNum = request.POST['userNum']
    userPwd = request.POST['userPwd']
    request.session["userNum"] = userNum
    Flag = 0
    # 查询是否已经注册
    if models.User.objects.filter(userNum=userNum):
        if models.User.objects.filter(userNum=userNum).get().userNum == "0":
            Flag = 1
        elif models.User.objects.filter(userNum=userNum).get().userNum == "1":
            Flag = 2
        # 查询密码是否正确
        if check_password(userPwd, models.User.objects.filter(userNum=userNum).get().userPwd):
            if Flag == 1:
                # 管理员登录成功
                return JsonResponse({"code": 0})
            elif Flag == 2:
                # 维修员登录成功
                return JsonResponse({"code": 1})
            else:
                if models.User.objects.filter(userNum=userNum).get().useride == "学生":
                    # 学生登录成功
                    return JsonResponse({"code": 2})
                else:
                    # 教师登录成功
                    return JsonResponse({"code": 3})
        else:
            # 密码错误
            return JsonResponse({"code": 4})
    else:
        # 用户不存在
        return JsonResponse({"code": 5})






