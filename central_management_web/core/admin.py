from django.contrib import admin
from .models import NhanVien, Teacher, HocVien, Class, Schedule, Enrollment, Attendance, FeedBack

@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ('ma_nv', 'full_name', 'gender', 'birth_day', 'email', 'sdt', 'address')
    search_fields = ('ma_nv', 'full_name', 'email', 'sdt')
    list_filter = ('gender',)
    ordering = ('ma_nv',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'full_name', 'gender', 'birth_day', 'email', 'sdt', 'address')
    search_fields = ('teacher_id', 'full_name', 'email', 'sdt')
    list_filter = ('gender',)
    ordering = ('teacher_id',)

@admin.register(HocVien)
class HocVienAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'gender', 'birth_day', 'email', 'sdt', 'address')
    search_fields = ('student_id', 'full_name', 'email', 'sdt')
    list_filter = ('gender',)
    ordering = ('student_id',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'class_name', 'nhan_vien', 'teacher', 'class_type', 'room', 
                   'khai_giang_date', 'ket_thuc_date', 'si_so', 'price')
    search_fields = ('class_id', 'class_name', 'room')
    list_filter = ('class_type', 'khai_giang_date', 'ket_thuc_date')
    ordering = ('class_id',)
    raw_id_fields = ('nhan_vien', 'teacher')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id_schedule', 'class_obj', 'day', 'start_time', 'end_time')
    search_fields = ('id_schedule', 'class_obj__class_name', 'day')
    list_filter = ('day',)
    ordering = ('id_schedule',)
    raw_id_fields = ('class_obj',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'enrollment_date', 'midterm1', 'midterm2', 
                   'midterm3', 'midterm4', 'final')
    search_fields = ('student__full_name', 'class_obj__class_name')
    list_filter = ('enrollment_date',)
    ordering = ('-enrollment_date',)
    raw_id_fields = ('student', 'class_obj')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id_attend', 'student', 'class_obj', 'attendance_date', 'status')
    search_fields = ('id_attend', 'student__full_name', 'class_obj__class_name')
    list_filter = ('status', 'attendance_date')
    ordering = ('-attendance_date',)
    raw_id_fields = ('student', 'class_obj')

@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('id_feedback', 'student', 'class_obj', 'teacher', 'class_rate', 'teacher_rate')
    search_fields = ('id_feedback', 'student__full_name', 'class_obj__class_name', 'teacher__full_name')
    list_filter = ('class_rate', 'teacher_rate')
    ordering = ('id_feedback',)
    raw_id_fields = ('student', 'class_obj', 'teacher')
