from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Nhân viên'),
        ('teacher', 'Giáo viên'),
        ('student', 'Học viên'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"


# Bảng Học Viên
class Student(models.Model):
    student_id = models.CharField(max_length=8, primary_key=True)
    fullName = models.CharField(max_length=40)
    gender = models.CharField(max_length=1,choices=[('M', 'Male'), ('F', 'Female')] )
    birthDay = models.DateField()
    email = models.CharField(max_length=40)
    sdt = models.CharField(max_length=15)
    address = models.CharField(max_length=30)
    debt = models.IntegerField()

    def __str__(self):
        return self.fullName


# Bảng Nhân Viên
class Staff(models.Model):
    MaNV = models.CharField(max_length=8, primary_key=True)
    fullName = models.CharField(max_length=40)
    gender = models.CharField(max_length=1,choices=[('M', 'Male'), ('F', 'Female')] )
    birthDay = models.DateField()
    email = models.CharField(max_length=40)
    sdt = models.CharField(max_length=15)
    address = models.CharField(max_length=30)

    def __str__(self):
        return self.fullName


# Bảng Giảng Viên
class Teacher(models.Model):
    MaGV = models.CharField(max_length=8, primary_key=True)
    fullName = models.CharField(max_length=40)
    gender = models.CharField(max_length=1,choices=[('M', 'Male'), ('F', 'Female')] )
    birthDay = models.DateField()
    email = models.CharField(max_length=40)
    sdt = models.CharField(max_length=15)
    address = models.CharField(max_length=30)

    def __str__(self):
        return self.fullName


# Bảng Lớp Học
class Class(models.Model):
    class_id = models.CharField(max_length=8, primary_key=True)
    ClassName = models.CharField(max_length=40)
    ClassType = models.CharField(max_length=1,choices=[('I', 'Intro'), ('M', 'Mastery'), ('O', 'Optimize'), ('E', 'Excellent')])
    room = models.CharField(max_length=15)
    Khai_Giang = models.DateField()
    Ket_Thuc = models.DateField()
    SiSo = models.IntegerField()
    Price = models.IntegerField()
    MaGV = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True,blank=True)
    MaNV = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.ClassName


# Bảng Điểm Danh
class Attendance(models.Model):
    id_attend = models.CharField(max_length=8, primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.student_id} - {self.class_id} - {self.attendance_date}"


# Bảng Lịch Học
class Schedule(models.Model):
    id_schedule = models.CharField(max_length=8, primary_key=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_id} - {self.day}"


# Bảng Đăng Ký Lớp
class Enrollment(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    minitest1 = models.FloatField()
    minitest2 = models.FloatField()
    minitest3 = models.FloatField()
    minitest4 = models.FloatField()
    midterm = models.FloatField()
    final = models.FloatField()

    def __str__(self):
        return f"{self.student_id} - {self.class_id}"


# Bảng Phản Hồi
class Feedback(models.Model):
    id_feedback = models.CharField(max_length=8, primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_rate = models.FloatField()
    teacher_rate = models.FloatField()

    def __str__(self):
        return f"Feedback {self.id_feedback} - {self.class_id}"
