# from django.contrib.auth.backends import BaseBackend
# from .models import Students, Teacher

# class StudentBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             student = Students.objects.get(First_Name=username)
#             if student.Password == password:
#                 return student  # Assumes Students model is compatible with Django's auth system
#         except Students.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return Students.objects.get(pk=user_id)
#         except Students.DoesNotExist:
#             return None


# class TeacherBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             teacher = Teacher.objects.get(TeacherName=username)
#             if teacher.TeacherPassword == password:
#                 return teacher
#         except Teacher.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return Teacher.objects.get(pk=user_id)
#         except Teacher.DoesNotExist:
#             return None
