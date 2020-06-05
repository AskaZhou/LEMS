from django.shortcuts import render
from user import models
from django.http import JsonResponse, HttpResponse


def m_show(request):
    """界面"""
    return render(request, "maintenance/show.html")


def statefailure(request):
    """故障状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="故障")
    return render(request, "maintenance/equipmentlist.html", {"equipments": equipments})


def service(request):
    """维修状态设备列表"""
    equipments = models.Equipment.objects.all().filter(eState="维修")
    return render(request, "maintenance/equipmentlist.html", {"equipments": equipments})


def servicelist(request):
    """维修状态设备列表"""
    services = models.Service.objects.all()
    return render(request, "maintenance/servicelist.html", {"services": services})


def breakequipmentlist(request):
    """设备列表"""
    breakequipments = models.BreakEquipment.objects.all()
    return render(request, "maintenance/breakequipmentlist.html", {"breakequipments": breakequipments})


def edit(request):
    """同意维修申请"""
    eid = request.GET["eid"]
    breakequipment = models.BreakEquipment.objects.get(BreakEquipmentNum=int(eid))
    return render(request, "maintenance/agree.html", {"breakequipment": breakequipment})


def save(request):
    """保存设备信息"""
    eid = request.GET["eid"]
    be = models.BreakEquipment.objects.get(BreakEquipmentNum=eid)
    e = models.Equipment.objects.get(eNum=be.eNum.eNum)
    e.eState = "维修"
    ServiceNum = request.POST["ServiceNum"]
    ServiceTxt = request.POST["ServiceTxt"]
    Change = request.POST["Change"]
    ServiceCost = request.POST["ServiceCost"]
    ServiceName = request.POST["ServiceName"]
    try:
        models.Service.objects.create(eNum=e, BreakEquipmentNum=be, ServiceNum=ServiceNum, ServiceTxt=ServiceTxt,
                                             Change=Change, ServiceCost=ServiceCost, ServiceName=ServiceName)
        e.save()
    except Exception:
        return JsonResponse({"code": 1})
    else:
        return JsonResponse({"code": 2})


def success(request):
    """维修成功"""
    eid = request.GET["eid"]
    se = models.Service.objects.get(ServiceNum=eid)
    be = models.BreakEquipment.objects.get(BreakEquipmentNum=se.BreakEquipmentNum.BreakEquipmentNum)
    e = models.Equipment.objects.get(eNum=se.eNum.eNum)
    e.eState = "可借"
    try:
        e.save()
        be.delete()
        se.delete()
    except Exception:
        return HttpResponse("确认失败！")
    else:
        return HttpResponse("确认成功！")


def fail(request):
    """维修失败"""
    eid = request.GET["eid"]
    se = models.Service.objects.get(ServiceNum=eid)
    be = models.BreakEquipment.objects.get(BreakEquipmentNum=se.BreakEquipmentNum.BreakEquipmentNum)
    e = models.Equipment.objects.get(eNum=se.eNum.eNum)
    e.eState = "报销"
    try:
        e.save()
        be.delete()
        se.delete()
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