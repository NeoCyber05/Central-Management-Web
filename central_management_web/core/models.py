from django.db import models

# Lưu ý về MaNV:
# Sơ đồ gốc có NhanVien.MaNV là INT, nhưng Class.MaNV (FK) là CHAR(8).
# Để nhất quán, MaNV của NhanVien được định nghĩa là CharField(max_length=8) ở đây.
# Nếu MaNV của NhanVien thực sự là INT, thì FK trong Class cũng cần điều chỉnh.

class NhanVien(models.Model):
    ma_nv = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Nhân Viên")
    full_name = models.CharField(max_length=40, verbose_name="Họ và Tên")
    gender = models.CharField(max_length=1, verbose_name="Giới tính") # Cân nhắc dùng choices, ví dụ: ('M', 'Nam'), ('F', 'Nữ'), ('O', 'Khác')
    birth_day = models.DateField(verbose_name="Ngày sinh")
    email = models.EmailField(max_length=40, unique=True, verbose_name="Email")
    sdt = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.CharField(max_length=30, verbose_name="Địa chỉ")

    def __str__(self):
        return f"{self.full_name} ({self.ma_nv})"

    class Meta:
        verbose_name = "Nhân Viên"
        verbose_name_plural = "Nhân Viên"

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Giáo Viên")
    full_name = models.CharField(max_length=40, verbose_name="Họ và Tên")
    gender = models.CharField(max_length=1, verbose_name="Giới tính") # Cân nhắc dùng choices
    birth_day = models.DateField(verbose_name="Ngày sinh")
    email = models.EmailField(max_length=40, unique=True, verbose_name="Email")
    sdt = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.CharField(max_length=30, verbose_name="Địa chỉ")

    def __str__(self):
        return f"{self.full_name} ({self.teacher_id})"

    class Meta:
        verbose_name = "Giáo Viên"
        verbose_name_plural = "Giáo Viên"

class HocVien(models.Model):
    student_id = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Học Viên")
    full_name = models.CharField(max_length=40, verbose_name="Họ và Tên")
    gender = models.CharField(max_length=1, verbose_name="Giới tính") # Cân nhắc dùng choices
    birth_day = models.DateField(verbose_name="Ngày sinh")
    email = models.EmailField(max_length=40, unique=True, verbose_name="Email")
    sdt = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.CharField(max_length=30, verbose_name="Địa chỉ")

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

    class Meta:
        verbose_name = "Học Viên"
        verbose_name_plural = "Học Viên"

class Class(models.Model):
    class_id = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Lớp học")
    # Giả định MaNV trong NhanVien là CharField(max_length=8) như đã lưu ý ở trên.
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, blank=True, db_column='MaNV', verbose_name="Nhân viên quản lý")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, db_column='teacher_id', verbose_name="Giáo viên")
    class_name = models.CharField(max_length=40, verbose_name="Tên lớp học")
    class_type = models.CharField(max_length=1, verbose_name="Loại lớp") # Ví dụ: 'O' (Online), 'F' (Offline)
    room = models.CharField(max_length=15, verbose_name="Phòng học")
    khai_giang_date = models.DateField(verbose_name="Ngày khai giảng")
    ket_thuc_date = models.DateField(verbose_name="Ngày kết thúc")
    si_so = models.IntegerField(verbose_name="Sĩ số tối đa")
    price = models.IntegerField(verbose_name="Học phí") # Cân nhắc dùng DecimalField nếu cần độ chính xác cao hơn cho tiền tệ

    def __str__(self):
        return f"{self.class_name} ({self.class_id})"

    class Meta:
        verbose_name = "Lớp Học"
        verbose_name_plural = "Lớp Học"

class Schedule(models.Model):
    id_schedule = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Lịch học")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', related_name='schedules', verbose_name="Lớp học")
    day = models.CharField(max_length=20, verbose_name="Ngày trong tuần/Buổi học") # Ví dụ: "Thứ 2", "Buổi 1" hoặc một ngày cụ thể
    start_time = models.TimeField(verbose_name="Thời gian bắt đầu")
    end_time = models.TimeField(verbose_name="Thời gian kết thúc")

    def __str__(self):
        return f"Lịch học {self.id_schedule} cho lớp {self.class_obj.class_name}"

    class Meta:
        verbose_name = "Lịch Học"
        verbose_name_plural = "Lịch Học"
        # unique_together = (('class_obj', 'day', 'start_time'),) # Cân nhắc nếu cần đảm bảo không trùng lịch

class Enrollment(models.Model):
    # Django không hỗ trợ composite primary key trực tiếp.
    # Một AutoField được thêm làm PK, và unique_together được sử dụng để đảm bảo tính duy nhất.
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(HocVien, on_delete=models.CASCADE, db_column='student_id', verbose_name="Học viên")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', verbose_name="Lớp học")
    enrollment_date = models.DateField(verbose_name="Ngày đăng ký")
    midterm1 = models.FloatField(null=True, blank=True, verbose_name="Điểm giữa kỳ 1")
    midterm2 = models.FloatField(null=True, blank=True, verbose_name="Điểm giữa kỳ 2")
    midterm3 = models.FloatField(null=True, blank=True, verbose_name="Điểm giữa kỳ 3")
    midterm4 = models.FloatField(null=True, blank=True, verbose_name="Điểm giữa kỳ 4")
    final = models.FloatField(null=True, blank=True, verbose_name="Điểm cuối kỳ")

    def __str__(self):
        return f"{self.student.full_name} đăng ký lớp {self.class_obj.class_name}"

    class Meta:
        verbose_name = "Đăng Ký Học"
        verbose_name_plural = "Đăng Ký Học"
        unique_together = (('student', 'class_obj'),) # Đảm bảo một học viên chỉ đăng ký một lớp một lần

class Attendance(models.Model):
    id_attend = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Điểm danh")
    student = models.ForeignKey(HocVien, on_delete=models.CASCADE, db_column='student_id', verbose_name="Học viên")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', verbose_name="Lớp học")
    attendance_date = models.DateField(verbose_name="Ngày điểm danh")
    status = models.CharField(max_length=15, verbose_name="Trạng thái") # Ví dụ: 'Có mặt', 'Vắng', 'Trễ'

    def __str__(self):
        return f"Điểm danh {self.student.full_name} - Lớp {self.class_obj.class_name} - Ngày {self.attendance_date}"

    class Meta:
        verbose_name = "Điểm Danh"
        verbose_name_plural = "Điểm Danh"
        # unique_together = (('student', 'class_obj', 'attendance_date'),) # Đảm bảo không điểm danh trùng

class FeedBack(models.Model):
    id_feedback = models.CharField(max_length=8, primary_key=True, verbose_name="Mã Feedback")
    student = models.ForeignKey(HocVien, on_delete=models.CASCADE, db_column='student_id', verbose_name="Học viên")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', verbose_name="Lớp học")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, db_column='teacher_id', verbose_name="Giáo viên")
    class_rate = models.FloatField(null=True, blank=True, verbose_name="Đánh giá lớp học") # Ví dụ: thang điểm 1-5
    teacher_rate = models.FloatField(null=True, blank=True, verbose_name="Đánh giá giáo viên") # Ví dụ: thang điểm 1-5
    # content = models.TextField(null=True, blank=True, verbose_name="Nội dung feedback") # Có thể thêm nếu cần feedback dạng văn bản

    def __str__(self):
        return f"Feedback {self.id_feedback} từ {self.student.full_name} cho lớp {self.class_obj.class_name}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"