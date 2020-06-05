from django.contrib import admin
from .models import User, Equipment, Teacher, Service, BreakEquipment


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['userName', 'userNum', 'userPhone']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['eName', 'eKind', 'eRoom', 'eTeacher', 'eStudent', 'eState']


@admin.register(Teacher)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['tName', 'tPhone']


@admin.register(BreakEquipment)
class BreakEquipmentAdmin(admin.ModelAdmin):
    list_display = ['BreakEquipmentNum', 'BreakEquipmentName', 'BreakTxt']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['ServiceNum', 'ServiceTxt', 'ServiceCost']