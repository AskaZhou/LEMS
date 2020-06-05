from django.shortcuts import render
from user import models
from django.http import JsonResponse, HttpResponse

def t_show(request):
    """教师界面"""
    return render(request, "teacher/show.html")


def equipmentlist(request):
    """设备列表"""
    equipments = models.Equipment.objects.all()
    return render(request, "teacher/equipmentlist.html", {"equipments": equipments})


def kindjsj(request):
    """计算机类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="计算机类")
    return render(request, "teacher/kindjsj.html", {"equipments": equipments})


def kindsw(request):
    """生物类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="生物类")
    return render(request, "teacher/kindsw.html", {"equipments": equipments})


def kindhx(request):
    """化学类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="化学类")
    return render(request, "teacher/kindhx.html", {"equipments": equipments})


def kindwl(request):
    """物理类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="物理类")
    return render(request, "teacher/kindwl.html", {"equipments": equipments})


def kindjx(request):
    """机械类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="机械类")
    return render(request, "teacher/kindjx.html", {"equipments": equipments})


def kindqt(request):
    """其它类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="其它类")
    return render(request, "teacher/kindqt.html", {"equipments": equipments})


def stateable(request):
    """可借状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="可借")
    return render(request, "teacher/stateable.html", {"equipments": equipments})


def stateunable(request):
    """借出状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="借出")
    return render(request, "teacher/stateunable.html", {"equipments": equipments})


def statefailure(request):
    """故障状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="故障")
    return render(request, "teacher/statefailure.html", {"equipments": equipments})


def service(request):
    """维修状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="维修")
    return render(request, "teacher/equipmentlist.html", {"equipments": equipments})


def broken(request):
    """维修状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="报销")
    return render(request, "teacher/equipmentlist.html", {"equipments": equipments})


def myequipments(request):
    """我的设备列表"""
    userNum = request.session.get("userNum")
    request.session["userNum"] = userNum
    user = models.User.objects.get(userNum=userNum)
    teacher = models.Teacher.objects.get(tPhone=user.userPhone)
    equipments = models.Equipment.objects.all().filter(eTeacher=teacher)
    return render(request, "teacher/myequipments.html", {"equipments": equipments})


def main(request):
    """申请维修"""
    eid = request.GET["eid"]
    equipment = models.Equipment.objects.get(eNum=int(eid))
    return render(request, "teacher/main.html", {"equipment": equipment})


def mainupdate(request):
    """设置故障状态"""
    eid = request.GET["eid"]
    e = models.Equipment.objects.get(eNum=eid)
    e.eState = "故障"
    BreakEquipmentNum = request.POST["BreakEquipmentNum"]
    BreakEquipmentName = request.POST["BreakEquipmentNum"]
    BreakTxt = request.POST["BreakTxt"]
    DealPerson = request.POST["Dealperson"]
    try:
        e.save()
        models.BreakEquipment.objects.create(BreakTxt=BreakTxt, eNum=e, BreakEquipmentNum=BreakEquipmentNum,
                                             BreakEquipmentName=BreakEquipmentName, DealPerson=DealPerson)
    except Exception:
        return JsonResponse({"code": 1})
    else:
        return JsonResponse({"code": 2})


def applylist(request):
    """申请列表"""
    userNum = request.session.get("userNum")
    request.session["userNum"] = userNum
    user = models.User.objects.get(userNum=userNum)
    teacher = models.Teacher.objects.get(tPhone=user.userPhone)
    equipments = models.Equipment.objects.all().filter(eState="待确认", eTeacher=teacher)
    return render(request, "teacher/applylist.html", {"equipments": equipments})


def yes(request):
    """确认归还"""
    eid = request.GET["eid"]
    uid = request.GET["uid"]
    equipment = models.Equipment.objects.get(eNum=eid)
    user = models.User.objects.get(id=uid)
    apply = models.Applylist.objects.get(equipment=equipment)
    equipment.eStudent = None
    equipment.eState = "可借"
    user.useCount -= 1
    try:
        user.save()
        equipment.save()
        apply.delete()
    except Exception:
        return HttpResponse("确认失败！")
    else:
        return HttpResponse("确认成功！")


def search(request):
    """设备搜索"""
    sear = request.GET["sear"]
    try:
        int(sear)
    except Exception:
        equipments = models.Equipment.objects.all().filter(eName=sear)
        content = {'equipments': equipments}
        return render(request, "teacher/search.html", content)
    else:
        equipments = models.Equipment.objects.all().filter(eNum=sear)
        content = {'equipments': equipments}
        return render(request, "teacher/search.html", content)
