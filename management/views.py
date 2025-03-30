from django.db import models

# 1. Bảng Học Viên
class HocVien(models.Model):
    student_id = models.CharField(max_length=8, primary_key=True)
    fullName = models.CharField(max_length=40)
    gender = models.CharField(max_length=1)
    birthDay = models.DateField()
    email = models.CharField(max_length=40)
    sdt = models.CharField(max_length=15)
    address = models.CharField(max_length=30)
    debt = models.IntegerField()

    def __str__(self):
        return self.fullName

# 2. Bảng Giáo Viên
class Teacher(models.Model):
    MaGV = models.CharField(max_length=8, primary_key=True)
    fullName = models.CharField(max_length=40)
    gender = models.CharField(max_length=1)
    birthDay = models.DateField()
    email = models.CharField(max_length=40)
    sdt = models.CharField(max_length=15)
    address = models.CharField(max_length=30)

    def __str__(self):
        return self.fullName

# 3. Bảng Nhân Viên
class NhanVien(models.Model):
    MaNV = models.CharField(max_length=8, primary_key=True)
    fullName = models.CharField(max_length=40)
    gender = models.CharField(max_length=1)
    birthDay = models.DateField()
    email = models.CharField(max_length=40)
    sdt = models.CharField(max_length=15)
    address = models.CharField(max_length=30)

    def __str__(self):
        return self.fullName

# 4. Bảng Lớp Học
class LopHoc(models.Model):
    class_id = models.CharField(max_length=8, primary_key=True)
    ClassName = models.CharField(max_length=40)
    ClassType = models.CharField(max_length=1)  # I, M, O, E
    room = models.CharField(max_length=15)
    Khai_Giang = models.DateField()
    Ket_Thuc = models.DateField()
    SiSo = models.IntegerField()
    Rate = models.FloatField()
    Price = models.IntegerField()

    def __str__(self):
        return self.ClassName

# 5. Bảng Giảng Dạy (Teacher - Class mối quan hệ n-n)
class Teaching(models.Model):
    MaGV = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(LopHoc, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('MaGV', 'class_id')

# 6. Bảng Điểm Danh
class Attendance(models.Model):
    id_attend = models.CharField(max_length=8, primary_key=True)
    student_id = models.ForeignKey(HocVien, on_delete=models.CASCADE)
    class_id = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(max_length=15)  # Present, Absent

# 7. Bảng Lịch Học
class Schedule(models.Model):
    id_schedule = models.CharField(max_length=8, primary_key=True)
    class_id = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

# 8. Bảng Đăng Ký Lớp Học
class Enrollments(models.Model):
    id_enroll = models.CharField(max_length=8, primary_key=True)
    student_id = models.ForeignKey(HocVien, on_delete=models.CASCADE)
    class_id = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    enrollment_date = models.DateField()

# 9. Bảng Điểm Số Học Viên
class Grades(models.Model):
    id_grade = models.CharField(max_length=8, primary_key=True)
    student_id = models.ForeignKey(HocVien, on_delete=models.CASCADE)
    class_id = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    minitest1 = models.FloatField()
    minitest2 = models.FloatField()
    minitest3 = models.FloatField()
    minitest4 = models.FloatField()
    midterm = models.FloatField()
    final = models.FloatField()

# 10. Bảng Feedback
class Feedback(models.Model):
    id_feedback = models.CharField(max_length=8, primary_key=True)
    student_id = models.ForeignKey(HocVien, on_delete=models.CASCADE)
    class_id = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_rate = models.FloatField()
    teacher_rate = models.FloatField()
