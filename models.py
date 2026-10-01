from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [('student','Student'),('mentor','Mentor'),('company','Company/HR'),('admin','Admin')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    college = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    def __str__(self): return f'{self.user.username} ({self.role})'

class Company(models.Model):
    name = models.CharField(max_length=150)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Internship(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    mode = models.CharField(max_length=30, default='Hybrid')
    duration = models.CharField(max_length=50)
    stipend = models.CharField(max_length=50, blank=True)
    skills = models.CharField(max_length=250)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Course(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.title

class Application(models.Model):
    STATUS = [('pending','Pending'),('shortlisted','Shortlisted'),('selected','Selected'),('rejected','Rejected')]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    cover_note = models.TextField(blank=True)
    class Meta: unique_together = ('student','internship')

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

class Task(models.Model):
    title = models.CharField(max_length=150)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, default='Pending')
    submission = models.TextField(blank=True)

class Feedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    certificate_no = models.CharField(max_length=50, unique=True)
    issued_on = models.DateField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
