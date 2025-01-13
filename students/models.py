from django.db import models

# Create your models here.
class Students(models.Model):
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    StudentID = models.IntegerField(unique=True,primary_key=True)
    Semester = models.CharField(max_length=20)
    Program = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.StudentID}"
    
    
class Teacher(models.Model):
    TeacherID = models.IntegerField(unique=True,primary_key=True)
    TeacherName = models.CharField(max_length=100)
    TeacherEmail = models.EmailField(max_length=100)
    TeacherPassword = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f"{self.TeacherID}"
    
    
class StudentAttendance(models.Model):
    STUDENT_STATUS = (
        ('P','Present'),
        ('A','Absent'),
        ('L','Leave'),
    )
    StudentID = models.ForeignKey(Students,on_delete=models.SET_NULL,null=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    Date = models.DateField()
    check_in = models.TimeField(blank=True,null=True)
    check_out = models.TimeField(blank=True,null=True)
    status = models.CharField(max_length=10,choices=STUDENT_STATUS,blank=True)
    
    def __str__(self):
        return f"{self.StudentID}"
    
    
    
class StudentApplication(models.Model):
    StudentID = models.ForeignKey(Students,on_delete=models.SET_NULL,null=True)
    Full_Name = models.CharField(max_length=100)
    Semester =  models.CharField(max_length=100)
    Program = models.CharField(max_length=100)
    TeacherID = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True)
    TeacherName = models.CharField(max_length=100)
    ApplicationContent = models.TextField()
    Date = models.DateField()
    status = models.CharField(max_length=10,default="Pending")