from django.urls import path 
from .views import * 

urlpatterns = [
    path("",index,name="index"),
    path("registerstudents/",student_registration,name="student_register"),
    path("registerteacher/",teacher_registration,name="teacher_register"),
    path("student_login",LoginStudent,name="student_login"),
    path("teacher_login",LoginTeacher,name="teacher_login"),
    path("sampleCollections/",Samplecollection,name="sample_collection"),
    path("checkin/",CheckIn,name="checkin"),
    path("checkout/",CheckOut,name="checkout"),
    path("studentprofile/<int:id>/",Student_Profile,name="studentprofile"),
    path("teacherprofile/<int:id>/",teacher_profile,name="teacherprofile"),
    path("teacherprofile/<int:id>/<int:appid>/<str:status>/",teacher_profile,name="teacherprofile"),
    path("attendance_report/",Attendance,name="attendance_report"),
    path("studentattendacereport/",StudentAttendanceReport,name="studentattendacereport"),
    path("studentapplicationstatus/",ApplicationStatus,name="studentapplicationstatus"),
    path("studentapplication/",Application_submission,name="studentapplication"),
    path("studentlogout/",student_logout,name="studentlogout"),
    path("teacherlogout/",teacher_logout,name="teacherlogout"),
]
