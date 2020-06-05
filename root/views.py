from django.shortcuts import render
from user import models
from django.http import JsonResponse, HttpResponse


def t_show(request):
    """教师界面"""
    return render(request, "root/show.html")


def equipmentlist(request):
    """设备列表"""
    equipments = models.Equipment.objects.all()
    return render(request, "root/equipmentlist.html", {"equipments": equipments})


def kindjsj(request):
    """计算机类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="计算机类")
    return render(request, "root/kindjsj.html", {"equipments": equipments})


def kindsw(request):
    """生物类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="生物类")
    return render(request, "root/kindsw.html", {"equipments": equipments})


def kindhx(request):
    """化学类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="化学类")
    return render(request, "root/kindhx.html", {"equipments": equipments})


def kindwl(request):
    """物理类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="物理类")
    return render(request, "root/kindwl.html", {"equipments": equipments})


def kindjx(request):
    """机械类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="机械类")
    return render(request, "root/kindjx.html", {"equipments": equipments})


def kindqt(request):
    """其它类设备列表"""
    equipments = models.Equipment.objects.all().filter(eKind="其它类")
    return render(request, "root/kindqt.html", {"equipments": equipments})


def stateable(request):
    """可借状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="可借")
    return render(request, "root/stateable.html", {"equipments": equipments})


def stateunable(request):
    """借出状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="借出")
    return render(request, "root/stateunable.html", {"equipments": equipments})


def statefailure(request):
    """故障状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="故障")
    return render(request, "root/statefailure.html", {"equipments": equipments})


def service(request):
    """维修状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="维修")
    return render(request, "root/equipmentlist.html", {"equipments": equipments})


def broken(request):
    """维修状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="报销")
    return render(request, "root/equipmentlist.html", {"equipments": equipments})



def edit(request):
    """编辑设备信息"""
    eid = request.GET["eid"]
    equipment = models.Equipment.objects.get(eNum=int(eid))
    return render(request, "root/edit.html", {"equipment": equipment})


def update(request):
    """更新设备信息"""
    eid = request.GET["eid"]
    e = models.Equipment.objects.get(eNum=eid)
    e.eName = request.POST["eName"]
    e.eKind = request.POST["eKind"]
    e.eRoom = request.POST["eRoom"]
    e.eCost = request.POST["eCost"]
    e.eManufacture = request.POST["eManufacture"]
    t = models.Teacher.objects.get(tName=e.eTeacher.tName)
    t.tName = request.POST["tName"]
    t.tPhone = request.POST["tPhone"]
    try:
        e.save()
        t.save()
    except Exception:
        return JsonResponse({"code": 1})
    else:
        return JsonResponse({"code": 2})


def delete(request):
    """删除设备信息"""
    eid = request.GET["eid"]
    equipment = models.Equipment.objects.filter(eNum=eid)
    try:
        equipment.delete()
    except Exception:
        return HttpResponse("删除失败")
    else:
        return HttpResponse("删除成功")


def addequipment(request):
    """添加设备"""
    teachers = models.Teacher.objects.all()
    return render(request, "root/addequipment.html", {"teachers": teachers})


def save(request):
    """保存添加的内容"""
    eNum = request.POST["eNum"]
    eName = request.POST["eName"]
    eCost = request.POST["eCost"]
    eKind = request.POST["eKind"]
    eRoom = request.POST["eRoom"]
    eManufacture = request.POST["eManufacture"]
    etName = request.POST["tName"]
    teacher = models.Teacher.objects.get(tName=etName)
    try:
        models.Equipment.objects.create(eNum=eNum, eKind=eKind, eName=eName, eCost=eCost,
                                        eManufacture=eManufacture, eRoom=eRoom, eTeacher=teacher)
    except Exception:
        return JsonResponse({"code": 1})
    else:
        return JsonResponse({"code": 2})


def userlist(request):
    users = models.User.objects.all()
    return render(request, "root/userlist.html", {"users": users})


def deleteuser(request):
    """删除用户信息"""
    uid = request.GET["uid"]
    user = models.User.objects.filter(id=uid)
    try:
        user.delete()
    except Exception:
        return HttpResponse("删除失败")
    else:
        return HttpResponse("删除成功")


def main(request):
    """申请维修"""
    eid = request.GET["eid"]
    equipment = models.Equipment.objects.get(eNum=int(eid))
    return render(request, "root/main.html", {"equipment": equipment})


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


def search(request):
    """设备搜索"""
    sear = request.GET["sear"]
    try:
        int(sear)
    except Exception:
        equipments = models.Equipment.objects.all().filter(eName=sear)
        content = {'equipments': equipments}
        return render(request, "root/search.html", content)
    else:
        equipments = models.Equipment.objects.all().filter(eNum=int(sear))
        content = {'equipments': equipments}
        return render(request, "root/search.html", content)
