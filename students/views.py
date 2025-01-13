from django.shortcuts import render,redirect
from .models import StudentAttendance, Students,Teacher,StudentApplication
from django.contrib import messages
from django.db.models import Q 
# from django.contrib.auth import login, logout,authenticate
import cv2 
import os 
import numpy as np 
from PIL import Image
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth import login,logout 
from datetime import datetime, date,timedelta 
import re 
from django.contrib.auth.hashers import make_password
cascade_path = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")
face_classifier = cv2.CascadeClassifier(cascade_path)# Create your views here.

# Password Validation Function is here....
def validate_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if re.match(pattern, password):
        print("Password is correct--------------------------")
        return True
    else:
        return False
def name_validation(name):
    pattern = r'^[A-Za-z]+$'
    if re.match(pattern, name):
        print("Name is correct--------------------------")
        return True
    else:
        return False
    
def ID_validation(ID):
    pattern = r'^[0-9]+$'
    if re.match(pattern, ID):
        return True
    else:
        return False




def student_registration(request):
    if request.method == "POST":
        firstname:str = str(request.POST.get('firstname')).strip()
        lastname:str = str(request.POST.get('lastname')).strip()
        studentid:str = str(request.POST.get('studentid')).strip()
        semester:str = str(request.POST.get('semester')).strip()
        program:str = str(request.POST.get('program')).strip()
        password1:str = str(request.POST.get('password1')).strip()
        password2:str = str(request.POST.get('password2')).strip()
        try:
            studentid = int(studentid)
        except ValueError:
            messages.add_message(request,messages.ERROR,"Sorry Only Numbers are Allowed")
            return render(request,"students/register_students.html")
        if password1 == password2 and validate_password(password1) and name_validation(firstname) and name_validation(lastname):
            student, created = Students.objects.get_or_create(StudentID=studentid,defaults={'First_Name':firstname,'Last_Name':lastname,"Semester":semester,"Program":program,"Password":password1})
            if created:
                messages.add_message(request,messages.SUCCESS,"Student Registered Successfully!")
                request.session['student_id'] = studentid
                return redirect("sample_collection")
            else:
                messages.add_message(request,messages.ERROR,"Student with This ID already Exists")
        
        else:
            messages.add_message(request,messages.ERROR,"Sorry Password Don't Match either Not Strong Password! or Not Valid Name")
        return redirect("student_register")
    return render(request,"students/register_students.html")

def teacher_registration(request):
    if request.method == "POST":
        name:str = str(request.POST.get('name')).strip()
        teacherid:str = str(request.POST.get('teacherid')).strip()
        email:str = str(request.POST.get('email')).strip()
        password1:str = str(request.POST.get('password1')).strip()
        password2:str = str(request.POST.get('password2')).strip()
        fname,lname = name.split(" ")
        try:
            teacherid = int(teacherid)
        except ValueError:
            messages.add_message(request,messages.ERROR,"Sorry Only Numbers are Allowed")
            return render(request,"students/register_teachers.html")
        
        if password1 == password2 and validate_password(password1) and name_validation(fname) and name_validation(lname):
            teacher, created = Teacher.objects.get_or_create(TeacherID=teacherid,defaults={"TeacherName":name,"TeacherEmail":email,"TeacherPassword":password1})
            if created:
                messages.add_message(request,messages.SUCCESS,"Teacher Registered Successfully")
                request.session['teacher_id'] = teacherid
                return redirect("teacher_login")
            else:
                messages.add_message(request,messages.ERROR,"Teacher with this ID already Exists!")
        else:
            # print(name,password1,password2)
            messages.add_message(request,messages.ERROR,"Sorry Password Don't Match or Name is Not Valid")
        return redirect("teacher_register")
    return render(request,"students/register_teachers.html")


def LoginStudent(request):
    if 'student_id' in request.session:
        return redirect("studentprofile",request.session['student_id']) 
    if request.method == "POST":
        firstname = str(request.POST.get('username')).strip()
        password = request.POST.get("password")
        try:
            user = Students.objects.get(First_Name=firstname, Password=password)
            id = user.StudentID
            request.session['student_id'] = user.StudentID
            messages.add_message(request, messages.SUCCESS, "Login successful")
            return redirect("studentprofile",id)
        except Students.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Invalid Username or Password")
            return redirect("student_login")
    
    return render(request, "students/login_student.html")




def LoginTeacher(request):
    if 'teacher_id' in request.session:
        return redirect("teacherprofile",request.session['teacher_id'])
    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get("password")
        # password = make_password(password)

        try:
            user = Teacher.objects.get(TeacherName=name, TeacherPassword=password)
            request.session['teacher_id'] = user.TeacherID
            messages.add_message(request, messages.SUCCESS, "Login successful")
            return redirect("teacherprofile",user.TeacherID)
        except Teacher.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Invalid Username or Password")
            return redirect("teacher_login")
    
    return render(request, "students/login_teacher.html")


def train_classifier():
    data_dir = "Resources/train_images"
    path = [ os.path.join(data_dir,file) for file in os.listdir(data_dir)]
    
    faces = []
    ids = []
    
    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img,'uint8')
        id = int(os.path.split(image)[1].split('.')[1])
        faces.append(imageNp)
        ids.append(id)
        # cv2.imshow("Training",imageNp)
        cv2.waitKey(1) == 13
    ids = np.array(ids)
    
    
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces,ids)
    clf.write('classifier.xml')
    cv2.destroyAllWindows()


def face_cropped(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        face_cropped = img[y:y+h, x:x+w]
        return face_cropped
    return None  


def Samplecollection(request):
    if request.method == "GET":
        
        id = request.session['student_id']
        fname = Students.objects.get(StudentID=id).First_Name
        lname = Students.objects.get(StudentID=id).Last_Name
        # fname = request.POST.get("fname")
        # lname = request.POST.get("lname")
        try:
            stu = Students.objects.get(Q(StudentID=id) & Q(First_Name=fname) & Q(Last_Name=lname))
        except Students.DoesNotExist:
            messages.add_message(request,messages.ERROR,"Sorry Invalid Credentials")
            return render(request,"students/samplecollector.html")
        capture = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
        if not capture.isOpened():
            print("Error: Could not open camera.")
        else:
            img_id = 0
            user_id = id
            while True:
                ret, myframe = capture.read()
                if not ret:
                    print("Failed to grab frame.")
                    break

                cropped_face = face_cropped(myframe)
                if cropped_face is not None:
                    img_id += 1
                    face = cv2.resize(cropped_face, (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    save_dir = 'Resources/train_images'
                    os.makedirs(save_dir, exist_ok=True)
                    file_path_name = os.path.join(save_dir, f'user.{user_id}.{img_id}.jpg')

                    # file_path_name = f'Resources/train_images/user.{user_id}.{img_id}.jpg'
                    cv2.imwrite(file_path_name, face)  # Save the image here
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 2)
                    cv2.imshow("Cropped Faces", face)
                
                
                if cv2.waitKey(1) == 13 or img_id == 100:
                    break

            capture.release()
            cv2.destroyAllWindows()
            train_classifier()

    return render(request,"students/samplecollector.html",{"msg":"Sample Collected Successfully"})

def index(request):
    # train_classifier()
    return render(request,"students/index.html")

def recognize_face():
    def draw_boundary(img,classifier,scalefactor,minNeighbours,color,text,clf):
        gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image,scalefactor,minNeighbours)
        
        coordinates = []
        
        for (x,y,w,h) in features:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            id,predict =clf.predict(gray_image[y:y+h,x:x+w])
            confidence = int((100*(1-predict/300)))

            
            if confidence > 80:
                try:
                    
                    student = Students.objects.get(pk=id)
                    
                    today = datetime.now().date()
                    if not StudentAttendance.objects.filter(StudentID=student, Date=today).exists():
                        StudentAttendance.objects.create(
                        StudentID=student,
                        First_Name=student.First_Name,
                        Last_Name=student.Last_Name,
                        semester=student.Semester,
                        Date=today,
                        status='P'
                    )
                        cv2.putText(img,f"id:{id} {student.First_Name} Attendance Marked",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                      
                    else:
                        pass 
                       
                        
                    cv2.putText(img,f"id:{id} {student.First_Name} Already Marked",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                except Students.DoesNotExist:
                    cv2.putText(img,"Not Registered",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                    
            else:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                cv2.putText(img,"Not Found",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                
            coordinates = [x,y,w,h]
        return coordinates
    def recognization(img,clf,faceCascade):
        coordinates = draw_boundary(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
        return img
    # faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")
    
    video_cap = cv2.VideoCapture(0)
    while True:
        ret, img = video_cap.read()
        img = recognization(img,clf,face_classifier)
        cv2.imshow("Welcome to Face Recognization",img)
        
        if cv2.waitKey(1) == 13:
            break
    video_cap.release()
    cv2.destroyAllWindows()        

# check In function
def CheckIn(request):
    # recognize_face()
    def draw_boundary(img,classifier,scalefactor,minNeighbours,color,text,clf):
        gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image,scalefactor,minNeighbours)
        
        coordinates = []
        
        for (x,y,w,h) in features:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            id,predict =clf.predict(gray_image[y:y+h,x:x+w])
            confidence = int((100*(1-predict/300)))

            
            if confidence > 80:
                try:
                    
                    student = Students.objects.get(pk=id)
                    
                    today = datetime.now().date()
                    if not StudentAttendance.objects.filter(StudentID=student, Date=today).exists():
                        StudentAttendance.objects.create(
                        StudentID=student,
                        First_Name=student.First_Name,
                        Last_Name=student.Last_Name,
                        semester=student.Semester,
                        Date=today,
                        check_in = localtime(timezone.now()) 
                        # status='P'
                    )
                        cv2.putText(img,f"id:{id} {student.First_Name} Attendance Marked",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                      
                    else:
                        pass 
                       
                        
                    cv2.putText(img,f"id:{id} {student.First_Name} Already Marked",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                except Students.DoesNotExist:
                    cv2.putText(img,"Not Registered",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                    
            else:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                cv2.putText(img,"Not Found",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                
            coordinates = [x,y,w,h]
        return coordinates
    def recognization(img,clf,faceCascade):
        coordinates = draw_boundary(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
        return img
    # faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")
    
    video_cap = cv2.VideoCapture(0)
    while True:
        ret, img = video_cap.read()
        img = recognization(img,clf,face_classifier)
        cv2.imshow("Welcome to Face Recognization",img)
        
        if cv2.waitKey(1) == 13:
            break
    video_cap.release()
    cv2.destroyAllWindows()
    return redirect("teacherprofile",request.session['teacher_id'])


## Check out function 
def CheckOut(request):
    # recognize_face()
    def draw_boundary(img,classifier,scalefactor,minNeighbours,color,text,clf):
        gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image,scalefactor,minNeighbours)
        
        coordinates = []
        
        for (x,y,w,h) in features:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            id,predict =clf.predict(gray_image[y:y+h,x:x+w])
            confidence = int((100*(1-predict/300)))

            
            if confidence > 80:
                try:
                    today = datetime.now().date()
                    # print("------------------Today Date-----------------------",today)
                    student = Students.objects.get(StudentID=id)
                    attendance_record = StudentAttendance.objects.get(Q(StudentID=student) & Q(Date=today))
                    checkintime = attendance_record.check_in
                    checkouttime = attendance_record.check_out 
                    if not checkintime:
                        cv2.putText(img,"Not Check In ",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                        return
                    # current_time = localtime(timezone.now()).time()
                    received_time = datetime.strptime(str(checkintime), "%H:%M:%S.%f").time()
                    current_time = datetime.now().time()
                    received_time_full = datetime.combine(datetime.today(), received_time)
                    current_time_full = datetime.combine(datetime.today(), current_time)
                    time_diff = current_time_full - received_time_full
                    if time_diff <= timedelta(hours=1):
                        attendance_record.check_out = localtime(timezone.now())
                        attendance_record.status = 'A'
                        attendance_record.save() 

                    elif time_diff >=timedelta(hours=2):
                        attendance_record.check_out = localtime(timezone.now())
                        attendance_record.status = 'P'
                        attendance_record.save()
                        
                    cv2.putText(img,f"id:{id} {student.First_Name} Attendance Marked",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                        
                except Students.DoesNotExist:
                    cv2.putText(img,"Not Registered",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                    
            else:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                cv2.putText(img,"Not Found",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)
                
            coordinates = [x,y,w,h]
        return coordinates
    def recognization(img,clf,faceCascade):
        coordinates = draw_boundary(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
        return img
    # faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")
    
    video_cap = cv2.VideoCapture(0)
    while True:
        ret, img = video_cap.read()
        img = recognization(img,clf,face_classifier)
        cv2.imshow("Welcome to Face Recognization",img)
        
        if cv2.waitKey(1) == 13:
            break
    video_cap.release()
    cv2.destroyAllWindows()
    return redirect("teacherprofile",request.session['teacher_id'])

def Student_Profile(request,id):
    stu = Students.objects.get(pk=id)
    try:
        attendance_report = StudentAttendance.objects.get(StudentID=stu)
        return render(request,"students/student_profile.html",{"student":stu,"attendance":attendance_report})
    except:
        attendance_report = None 
    return render(request,"students/student_profile.html",{"student":stu,"attendance":attendance_report})

def teacher_profile(request,id,appid=None,status=None):
    teacher = Teacher.objects.get(pk=id)
    applications = StudentApplication.objects.filter(Q(TeacherID=id) & Q(status="Pending"))
    if appid and status:
       
        app = StudentApplication.objects.get(id=appid)
        app.status=status
        student = Students.objects.get(pk=app.StudentID.StudentID)
        
        today = datetime.now().date()
        if status == "Approve":
            if not StudentAttendance.objects.filter(StudentID=student, Date=today).exists():
                
                StudentAttendance.objects.create(
                        StudentID=student,
                        First_Name=student.First_Name,
                        Last_Name=student.Last_Name,
                        semester=student.Semester,
                        Date=today,
                        status='P'
                    )
                app.status="Approved"
        elif status == 'Reject':
            if not StudentAttendance.objects.filter(StudentID=student, Date=today).exists():
               
                StudentAttendance.objects.create(
                        StudentID=student,
                        First_Name=student.First_Name,
                        Last_Name=student.Last_Name,
                        semester=student.Semester,
                        Date=today,
                        status='A'
                    )
                app.status="Rejected"
        app.save()
        applications = StudentApplication.objects.filter(status="Pending")
    return render(request,"students/teacher_profile.html",{"teacher":teacher,"applications":applications,"tid":id})



# Attendace checking
def Attendance(request):
    semester = request.GET.get('Semester')
    specific_date = request.GET.get('date')
    start_of_month = date.today().replace(day=1)
    current_date = timezone.now().date()
    if not specific_date:
        sem = StudentAttendance.objects.filter(Q(semester=semester) & Q(Date__range=(start_of_month,current_date)))
        #total = StudentAttendance.objects.filter(Q(semester=semester) & Q(Date__range=(start_of_month,current_date))).count()
        #present = StudentAttendance.objects.filter(Q(semester=semester) & Q(status='P') & Q(Date__range=(start_of_month,current_date))).count()
        #absent = StudentAttendance.objects.filter(Q(semester=semester) & Q(status='A') & Q(Date__range=(start_of_month,current_date))).count()
        #leave = StudentAttendance.objects.filter(Q(semester=semester) &  Q(status='L') & Q(Date__range=(start_of_month,current_date))).count()
        return render(request,"students/attendance_report.html",{"semester":sem,"present":None,"absent":None,"leave":None,"date":None,"total":None})
    elif semester and specific_date:
        sem = StudentAttendance.objects.filter(Q(semester=semester) & Q(Date=specific_date))
        total = StudentAttendance.objects.filter(Q(semester=semester) & Q(Date=specific_date)).count()
        present = StudentAttendance.objects.filter(Q(semester=semester) & Q(status='P') & Q(Date=specific_date)).count()
        absent = StudentAttendance.objects.filter(Q(semester=semester) & Q(status='A') & Q(Date=specific_date)).count()
        leave = StudentAttendance.objects.filter(Q(semester=semester) &  Q(status='L') & Q(Date=specific_date)).count()
        return render(request,"students/attendance_report.html",{"semester":sem,"present":present,"absent":absent,"leave":leave,"date":specific_date,"total":total})
    else:
        return render(request,"students/attendance_report.html")
    

def StudentAttendanceReport(request):
    if 'student_id' in request.session:
        id =  request.session['student_id']
        stu = Students.objects.get(pk=id)
    else:
        return redirect("student_login")
    if request.method == "POST":
        specific_date_str = request.POST.get('date')
        start_of_month = date.today().replace(day=1)
        current_date = timezone.now().date()
        print("-------------current-----date------------")
        try:
            specific_date = (
                datetime.strptime(specific_date_str, "%Y-%m-%d").date() if specific_date_str else None
            )
            if specific_date and (specific_date <= current_date):
                print("-------------specfic date part date less than future------------")
                attendance_report = StudentAttendance.objects.filter(Q(StudentID=id) & Q(Date=specific_date))
               
                return render(request,"students/student_profile.html",{"student":stu,"attendance":attendance_report})
            elif specific_date > current_date:
                messages.add_message(request,messages.ERROR,"Invalid Date Found")
                print("..............Eror date part is working.........................")
                return render(request,"students/student_profile.html",{"student":stu})
            else:
                print("-------------no specfic date------------")
                attendance_report = StudentAttendance.objects.filter(Q(StudentID=stu) & Q(Date__range=(start_of_month,current_date)))
              
                return render(request,"students/student_profile.html",{"student":stu,"attendance":attendance_report})
        except:
            attendance_report = StudentAttendance.objects.filter(StudentID=stu)
            print("-----------Except part----------------------")
            return render(request,"students/student_profile.html",{"student":stu,"attendance":attendance_report})
            # attendance_report = StudentAttendance.objects.filter()
    return render(request,"students/student_profile.html",{"student":stu})

    
def ApplicationStatus(request):
    if request.method == 'POST':
        if 'student_id' in request.session:
                applications = StudentApplication.objects.filter(StudentID=request.session['student_id'])
                return render(request,"students/Application_status.html",{"Applications":applications})
        else:
            messages.add_message(request,messages.ERROR,"No Application submitted")
    return render(request,"students/Application_status.html")


def Application_submission(request):
    if request.method == "POST":
        student = Students.objects.get(StudentID=request.session['student_id'])
        date = request.POST.get('date')
        if StudentApplication.objects.filter(Q(StudentID=student)& Q(Date=date)).exists():
            messages.add_message(request,messages.ERROR,"Sorry Only Application can be submitted in day")
            return render(request,"students/student_application.html")
        FirstName = student.First_Name
        LastName = student.Last_Name
        semester = student.Semester
        program = student.Program
        teacherID = request.POST.get('teacherID')
        teachername = request.POST.get('teachername')
        applicationcontent = request.POST.get('applicationcontent')
        # stu = Students.objects.get(pk=studentID)
        teacher = Teacher.objects.get(pk=teacherID)
        if teachername == teacher.TeacherName:
            StudentApplication.objects.create(StudentID=student,Full_Name=f"{FirstName} {LastName}",Semester=semester,Program=program,TeacherID=teacher,TeacherName=teachername,ApplicationContent=applicationcontent,Date=date)
            messages.add_message(request,messages.SUCCESS,"Application Submitted Successfully!")
            return redirect("studentprofile",request.session['student_id'])
        else:
            messages.add_message(request,messages.ERROR,"Name invalid")
            return render(request,"students/student_application.html")
    return render(request,"students/student_application.html")


def student_logout(request):
    if 'student_id' in request.session:
            request.session.flush()
            return redirect("student_login")
    else:
        return redirect("student_login")
    
def teacher_logout(request):
    if 'teacher_id' in request.session:
            request.session.flush()
            return redirect("teacher_login")
    else:
        return redirect("teacher_login")