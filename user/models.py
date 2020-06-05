from django.db import models
import datetime


class Teacher(models.Model):
    tName = models.CharField(max_length=5, verbose_name="教师姓名")
    tPhone = models.CharField(max_length=11, verbose_name="联系电话", unique=True)

    def __str__(self):
        return self.tName


class User(models.Model):
    KIND_CHOICES = (
        ("学生", "学生"),
        ("教师", "教师"),
    )
    userName = models.CharField(max_length=11, verbose_name='姓名')
    userNum = models.CharField(max_length=15, verbose_name='学号', unique=True)
    useride = models.CharField(max_length=15, verbose_name='用户类别', choices=KIND_CHOICES)
    userPhone = models.CharField(max_length=11, verbose_name='联系方式', unique=True)
    userPwd = models.CharField(max_length=78, verbose_name='密码')
    useCount = models.IntegerField(default=0, verbose_name='已借数')

    def __str__(self):
        return "姓名：%s  学号：%s" % (self.userName, self.userNum)


class Equipment(models.Model):
    KIND_CHOICES = (
                    ("计算机类", "计算机类"),
                    ("机械类", "机械类"),
                    ("物理类", "物理类"),
                    ("化学类", "化学类"),
                    ("生物类", "生物类"),
                    ("其它类", "其它类"),
                    )
    eNum = models.CharField(max_length=15, verbose_name='设备号', unique=True, primary_key=True)
    eKind = models.CharField(max_length=10, verbose_name="设备类型", choices=KIND_CHOICES, default="请选择设备类型")
    eName = models.CharField(max_length=10, verbose_name="设备名称")
    eCost = models.CharField(max_length=11, verbose_name='价格')
    eManufacture = models.CharField(max_length=10, verbose_name="制造商", null=True)
    eManufactureData = models.DateField(auto_now_add=True, verbose_name="生产日期", null=True)
    eRoom = models.CharField(max_length=10, verbose_name="设备所在教室")
    eState = models.CharField(max_length=3, verbose_name="状态", choices=(('可借', '可借'), ('借出', '借出'), ('故障', '故障')), default="可借")
    eTeacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="负责教师")
    eStudent = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="借用学生", null=True, blank=True)

    def __str__(self):
        return self.eName


class BreakEquipment(models.Model):
    BreakEquipmentNum = models.CharField(max_length=15, verbose_name='故障序号', unique=True, primary_key=True)
    BreakEquipmentName = models.CharField(max_length=10, verbose_name='故障名称', null=True, blank=True, default=" ")
    BreakData = models.DateField(auto_now_add=True, verbose_name="故障日期")
    BreakTxt = models.CharField(max_length=11, verbose_name='故障信息', null=True, blank=True)
    DealPerson = models.CharField(max_length=11, verbose_name='经手人')
    eNum = models.OneToOneField(Equipment, to_field='eNum', verbose_name="设备号", on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.BreakEquipmentNum


class Service(models.Model):
    ServiceNum = models.CharField(max_length=15, verbose_name='维修号', unique=True, primary_key=True)
    ServiceData = models.DateField(auto_now_add=True, verbose_name="维修日期")
    ServiceTxt = models.CharField(max_length=11, verbose_name='维修信息')
    Change = models.CharField(max_length=11, verbose_name='改变配置')
    ServiceCost = models.CharField(max_length=11, verbose_name='维修金额')
    ServiceName = models.CharField(max_length=11, verbose_name='维修人')
    eNum = models.OneToOneField(Equipment, to_field='eNum', verbose_name="设备号", on_delete=models.CASCADE)
    BreakEquipmentNum = models.OneToOneField(BreakEquipment, to_field='BreakEquipmentNum', verbose_name="故障序号", on_delete=models.CASCADE)

    def __str__(self):
        return self.ServiceNum


class Applylist(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="归还学生")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="归还设备")