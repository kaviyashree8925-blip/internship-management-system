from django.contrib import admin
from .models import Profile, Company, Internship, Course, Application, Enrollment, Attendance, Task, Feedback, Certificate, Notification
admin.site.register([Profile, Company, Internship, Course, Application, Enrollment, Attendance, Task, Feedback, Certificate, Notification])
