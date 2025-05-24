from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Count, Sum, Avg, Q
from .models import NhanVien, Teacher, HocVien, Class, Schedule, Enrollment, Attendance, FeedBack
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

# Home View
def home(request):
    # Luôn chuyển hướng về login
    return redirect('core:login')

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Kiểm tra user có phải admin không
            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('core:admin_dashboard')
            else:
                messages.error(request, 'Bạn không có quyền truy cập hệ thống này')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng')
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')

# Dashboard Views
@login_required
@user_passes_test(is_admin, login_url='core:login')
def admin_dashboard(request):
    context = {
        'total_students': HocVien.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_classes': Class.objects.count(),
        'total_schedules': Schedule.objects.count(),
        'recent_attendance': Attendance.objects.order_by('-attendance_date')[:5],
        'recent_feedback': FeedBack.objects.order_by('-id_feedback')[:5],
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def statistics(request):
    context = {
        'student_stats': HocVien.objects.aggregate(
            total=Count('student_id'),
        ),
        'teacher_stats': Teacher.objects.aggregate(
            total=Count('teacher_id'),
        ),
        'class_stats': Class.objects.aggregate(
            total=Count('class_id'),
        ),
        'attendance_stats': Attendance.objects.aggregate(
            total=Count('id_attend'),
            present=Count('id_attend', filter=Q(status='Có mặt'))
        ),
        'feedback_stats': FeedBack.objects.aggregate(
            total=Count('id_feedback'),
            average_class_rating=Avg('class_rate'),
            average_teacher_rating=Avg('teacher_rate')
        ),
    }
    return render(request, 'core/statistics.html', context)

# User Management Views
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'core/user_list.html', {'users': users})

@login_required
def user_create(request):
    if request.method == 'POST':
        # Handle user creation
        pass
    return render(request, 'core/user_form.html')

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        # Handle user update
        pass
    return render(request, 'core/user_form.html', {'user': user})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Người dùng đã được xóa thành công')
        return redirect('core:user_list')
    return render(request, 'core/user_confirm_delete.html', {'user': user})

# Student Management Views
@login_required
def student_list(request):
    students = HocVien.objects.all()
    return render(request, 'core/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        # Handle student creation
        pass
    return render(request, 'core/student_form.html')

@login_required
def student_edit(request, pk):
    student = get_object_or_404(HocVien, pk=pk)
    if request.method == 'POST':
        # Handle student update
        pass
    return render(request, 'core/student_form.html', {'student': student})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(HocVien, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Học viên đã được xóa thành công')
        return redirect('core:student_list')
    return render(request, 'core/student_confirm_delete.html', {'student': student})

# Teacher Management Views
@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'core/teacher_list.html', {'teachers': teachers})

@login_required
def teacher_create(request):
    if request.method == 'POST':
        # Handle teacher creation
        pass
    return render(request, 'core/teacher_form.html')

@login_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        # Handle teacher update
        pass
    return render(request, 'core/teacher_form.html', {'teacher': teacher})

@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Giáo viên đã được xóa thành công')
        return redirect('core:teacher_list')
    return render(request, 'core/teacher_confirm_delete.html', {'teacher': teacher})

# Class Management Views
@login_required
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'core/class_list.html', {'classes': classes})

@login_required
def class_create(request):
    if request.method == 'POST':
        # Handle class creation
        pass
    return render(request, 'core/class_form.html')

@login_required
def class_edit(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        # Handle class update
        pass
    return render(request, 'core/class_form.html', {'class': class_obj})

@login_required
def class_delete(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, 'Lớp học đã được xóa thành công')
        return redirect('core:class_list')
    return render(request, 'core/class_confirm_delete.html', {'class': class_obj})

# Schedule Management Views
@login_required
def schedule_list(request):
    schedules = Schedule.objects.all()
    return render(request, 'core/schedule_list.html', {'schedules': schedules})

@login_required
def schedule_create(request):
    if request.method == 'POST':
        # Handle schedule creation
        pass
    return render(request, 'core/schedule_form.html')

@login_required
def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        # Handle schedule update
        pass
    return render(request, 'core/schedule_form.html', {'schedule': schedule})

@login_required
def schedule_delete(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Lịch học đã được xóa thành công')
        return redirect('core:schedule_list')
    return render(request, 'core/schedule_confirm_delete.html', {'schedule': schedule})

# Attendance Management Views
@login_required
def attendance_list(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'core/attendance_list.html', {'attendance_records': attendance_records})

@login_required
def attendance_create(request):
    if request.method == 'POST':
        # Handle attendance creation
        pass
    return render(request, 'core/attendance_form.html')

@login_required
def attendance_edit(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        # Handle attendance update
        pass
    return render(request, 'core/attendance_form.html', {'attendance': attendance})

@login_required
def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Điểm danh đã được xóa thành công')
        return redirect('core:attendance_list')
    return render(request, 'core/attendance_confirm_delete.html', {'attendance': attendance})

# Feedback Management Views
@login_required
def feedback_list(request):
    feedbacks = FeedBack.objects.all()
    return render(request, 'core/feedback_list.html', {'feedbacks': feedbacks})

@login_required
def feedback_view(request, pk):
    feedback = get_object_or_404(FeedBack, pk=pk)
    return render(request, 'core/feedback_detail.html', {'feedback': feedback})

@login_required
def feedback_delete(request, pk):
    feedback = get_object_or_404(FeedBack, pk=pk)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Đánh giá đã được xóa thành công')
        return redirect('core:feedback_list')
    return render(request, 'core/feedback_confirm_delete.html', {'feedback': feedback})

