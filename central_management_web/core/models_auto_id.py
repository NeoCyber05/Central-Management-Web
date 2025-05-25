from django.db import models

class NhanVien(models.Model):
    ma_nv = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Nhân Viên")
    full_name = models.CharField(max_length=40, verbose_name="Họ và Tên")
    gender = models.CharField(max_length=1, choices=[('M', 'Nam'), ('F', 'Nữ')], verbose_name="Giới tính")
    birth_day = models.DateField(verbose_name="Ngày sinh")
    email = models.EmailField(max_length=40, unique=True, verbose_name="Email")
    sdt = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.CharField(max_length=30, verbose_name="Địa chỉ")

    def save(self, *args, **kwargs):
        if not self.ma_nv:
            # Tự động tạo ID tiếp theo
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT nextval('nhanvien_id_seq')")
                self.ma_nv = str(cursor.fetchone()[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.ma_nv})"

    class Meta:
        verbose_name = "Nhân Viên"
        verbose_name_plural = "Nhân Viên"

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Giáo Viên")
    full_name = models.CharField(max_length=40, verbose_name="Họ và Tên")
    gender = models.CharField(max_length=1, choices=[('M', 'Nam'), ('F', 'Nữ')], verbose_name="Giới tính")
    birth_day = models.DateField(verbose_name="Ngày sinh")
    email = models.EmailField(max_length=40, unique=True, verbose_name="Email")
    sdt = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.CharField(max_length=30, verbose_name="Địa chỉ")

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT nextval('teacher_id_seq')")
                self.teacher_id = str(cursor.fetchone()[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.teacher_id})"

    class Meta:
        verbose_name = "Giáo Viên"
        verbose_name_plural = "Giáo Viên"

class HocVien(models.Model):
    student_id = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Học Viên")
    full_name = models.CharField(max_length=40, verbose_name="Họ và Tên")
    gender = models.CharField(max_length=1, choices=[('M', 'Nam'), ('F', 'Nữ')], verbose_name="Giới tính")
    birth_day = models.DateField(verbose_name="Ngày sinh")
    email = models.EmailField(max_length=40, unique=True, verbose_name="Email")
    sdt = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.CharField(max_length=30, verbose_name="Địa chỉ")

    def save(self, *args, **kwargs):
        if not self.student_id:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT nextval('hocvien_id_seq')")
                self.student_id = str(cursor.fetchone()[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

    class Meta:
        verbose_name = "Học Viên"
        verbose_name_plural = "Học Viên"

class Class(models.Model):
    class_id = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Lớp học")
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, blank=True, db_column='ma_nv', verbose_name="Nhân viên quản lý")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, db_column='teacher_id', verbose_name="Giáo viên")
    class_name = models.CharField(max_length=40, verbose_name="Tên lớp học")
    class_type = models.CharField(max_length=1, choices=[('O', 'Online'), ('F', 'Offline')], verbose_name="Loại lớp")
    room = models.CharField(max_length=15, verbose_name="Phòng học")
    khai_giang_date = models.DateField(verbose_name="Ngày khai giảng")
    ket_thuc_date = models.DateField(verbose_name="Ngày kết thúc")
    si_so = models.IntegerField(verbose_name="Sĩ số tối đa")
    price = models.IntegerField(verbose_name="Học phí")

    def save(self, *args, **kwargs):
        if not self.class_id:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT nextval('class_id_seq')")
                self.class_id = str(cursor.fetchone()[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.class_name} ({self.class_id})"

    class Meta:
        verbose_name = "Lớp Học"
        verbose_name_plural = "Lớp Học"

class Schedule(models.Model):
    id_schedule = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Lịch học")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', related_name='schedules', verbose_name="Lớp học")
    day = models.CharField(max_length=20, verbose_name="Ngày trong tuần/Buổi học")
    start_time = models.TimeField(verbose_name="Thời gian bắt đầu")
    end_time = models.TimeField(verbose_name="Thời gian kết thúc")

    def save(self, *args, **kwargs):
        if not self.id_schedule:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT nextval('schedule_id_seq')")
                self.id_schedule = str(cursor.fetchone()[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lịch học {self.id_schedule} cho lớp {self.class_obj.class_name}"

    class Meta:
        verbose_name = "Lịch Học"
        verbose_name_plural = "Lịch Học"

class Enrollment(models.Model):
    student = models.ForeignKey(HocVien, on_delete=models.CASCADE, db_column='student_id', verbose_name="Học viên")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', verbose_name="Lớp học")
    enrollment_date = models.DateField(verbose_name="Ngày đăng ký")
    minitest1 = models.FloatField(null=True, blank=True, verbose_name="Điểm minitest 1")
    minitest2 = models.FloatField(null=True, blank=True, verbose_name="Điểm minitest 2")
    minitest3 = models.FloatField(null=True, blank=True, verbose_name="Điểm minitest 3")
    minitest4 = models.FloatField(null=True, blank=True, verbose_name="Điểm minitest 4")
    midterm = models.FloatField(null=True, blank=True, verbose_name="Điểm giữa kỳ")
    final = models.FloatField(null=True, blank=True, verbose_name="Điểm cuối kỳ")

    def __str__(self):
        return f"{self.student.full_name} đăng ký lớp {self.class_obj.class_name}"

    class Meta:
        verbose_name = "Đăng Ký Học"
        verbose_name_plural = "Đăng Ký Học"
        unique_together = (('student', 'class_obj'),)

class Attendance(models.Model):
    id_attend = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Điểm danh")
    student = models.ForeignKey(HocVien, on_delete=models.CASCADE, db_column='student_id', verbose_name="Học viên")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', verbose_name="Lớp học")
    attendance_date = models.DateField(verbose_name="Ngày điểm danh")
    status = models.CharField(max_length=15, choices=[
        ('Có mặt', 'Có mặt'),
        ('Vắng', 'Vắng'),
        ('Trễ', 'Trễ'),
        ('Có phép', 'Có phép')
    ], verbose_name="Trạng thái")

    def save(self, *args, **kwargs):
        if not self.id_attend:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT nextval('attendance_id_seq')")
                self.id_attend = str(cursor.fetchone()[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Điểm danh {self.student.full_name} - Lớp {self.class_obj.class_name} - Ngày {self.attendance_date}"

    class Meta:
        verbose_name = "Điểm Danh"
        verbose_name_plural = "Điểm Danh"

class FeedBack(models.Model):
    id_feedback = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Feedback")
    student = models.ForeignKey(HocVien, on_delete=models.CASCADE, db_column='student_id', verbose_name="Học viên")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', verbose_name="Lớp học")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, db_column='teacher_id', verbose_name="Giáo viên")
    class_rate = models.FloatField(null=True, blank=True, verbose_name="Đánh giá lớp học")
    teacher_rate = models.FloatField(null=True, blank=True, verbose_name="Đánh giá giáo viên")

    def save(self, *args, **kwargs):
        if not self.id_feedback:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT nextval('feedback_id_seq')")
                self.id_feedback = str(cursor.fetchone()[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback {self.id_feedback} từ {self.student.full_name} cho lớp {self.class_obj.class_name}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback" 