from django.contrib import admin
from .models import User, Equipment, BreakEquipment, Service
from teacher.models import Teacher


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
