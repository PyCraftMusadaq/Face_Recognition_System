from django.contrib import admin
from .models import Students, StudentAttendance, Teacher, StudentApplication
from django.contrib.auth.models import Group,User


admin.site.unregister(Group)
admin.site.unregister(User)

@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['First_Name', 'Last_Name', 'StudentID', 'Semester', 'Program', 'Password']
    def has_add_permission(self, request):
        return False 
    
    def has_change_permission(self, request, obj=None):
        return False  

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['TeacherID', 'TeacherName', 'TeacherEmail', 'TeacherPassword']
    def has_add_permission(self, request):
        return False  
    
    def has_change_permission(self, request, obj=None):
        return False  

@admin.register(StudentAttendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['StudentID', 'First_Name', 'Last_Name', 'semester', 'Date','check_in','check_out','status']
    def has_add_permission(self, request):
        return False  
    
    def has_change_permission(self, request, obj=None):
        return False  

@admin.register(StudentApplication)
class AdminStudentApplication(admin.ModelAdmin):
    list_display = ['id', 'StudentID', 'Full_Name', 'Semester', 'Program', 'TeacherID', 'TeacherName', 'ApplicationContent', 'Date', 'status']
    def has_add_permission(self, request):
        return False 
    
    def has_change_permission(self, request, obj=None):
        return False