from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Count, Sum, Avg, Q
from .models import nhan_vien, teacher, hoc_vien, clazz, schedule, enrollments, attendance, feedback, class_type
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import teacher
from .forms import TeacherForm, HocVienForm, ClassForm, NhanVienForm, ClassTypeForm


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
        'total_students': hoc_vien.objects.count(),
        'total_teachers': teacher.objects.count(),
        'total_classes': clazz.objects.count(),
        'total_schedules': schedule.objects.count(),
        'recent_attendance': attendance.objects.order_by('-attendance_date')[:5],
        'recent_feedback': feedback.objects.order_by('-id_feedback')[:5],
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def statistics(request):
    context = {
        'student_stats': hoc_vien.objects.aggregate(
            total=Count('student_id'),
        ),
        'teacher_stats': teacher.objects.aggregate(
            total=Count('teacher_id'),
        ),
        'class_stats':clazz.objects.aggregate(
            total=Count('class_id'),
        ),
        'attendance_stats': attendance.objects.aggregate(
            total=Count('id_attend'),
            present=Count('id_attend', filter=Q(status='Có mặt'))
        ),
        'feedback_stats': feedback.objects.aggregate(
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
    students = hoc_vien.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = HocVienForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm học viên thành công!')
            return redirect('core:student_list')
    else:
        form = HocVienForm()
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Thêm'})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(hoc_vien, pk=pk)
    if request.method == 'POST':
        form = HocVienForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật học viên thành công!')
            return redirect('core:student_list')
    else:
        form = HocVienForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Sửa'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(hoc_vien, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Xóa học viên thành công!')
        return redirect('core:student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})

#-------------------------------
# Teacher Management Views
#-------------------------------
def teacher_list(request):
    teachers = teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'core/teacher_form.html', {'form': form, 'action': 'Thêm'})

def teacher_edit(request, pk):
    gv = get_object_or_404(teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=gv)
        if form.is_valid():
            form.save()
            return redirect('core:teacher_list')
    else:
        form = TeacherForm(instance=gv)
    return render(request, 'core/teacher_form.html', {'form': form, 'action': 'Sửa'})

def teacher_delete(request, pk):
    gv = get_object_or_404(teacher, pk=pk)
    if request.method == 'POST':
        gv.delete()
        return redirect('core:teacher_list')
    return render(request, 'core/teacher_confirm_delete.html', {'teacher': gv})

#-------------------------------
# Class Management Views
#-------------------------------
@login_required
def class_list(request):
    classes = clazz.objects.all()
    return render(request, 'core/class_list.html', {'classes': classes})

@login_required
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:class_list')
    else:
        form = ClassForm()
    return render(request, 'core/class_form.html', {'form': form, 'action': 'Thêm'})

@login_required
def class_edit(request, pk):
    class_obj = get_object_or_404(clazz, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            return redirect('core:class_list')
    else:
        form = ClassForm(instance=class_obj)
    return render(request, 'classes/class_form.html', {'form': form, 'action': 'Sửa'})

@login_required
def class_delete(request, pk):
    class_obj = get_object_or_404(clazz, pk=pk)
    if request.method == 'POST':
        class_obj.delete()
        return redirect('core:class_list')
    return render(request, 'classes/class_confirm_delete.html', {'class_obj': class_obj})

@login_required
def class_detail(request, pk):
    class_obj = get_object_or_404(clazz, pk=pk)
    enrolls = enrollments.objects.filter(class_obj=class_obj)
    students = hoc_vien.objects.exclude(enrollments__class_obj=class_obj)

    if request.method == 'POST':
        # Xử lý thêm học viên
        if 'student_id' in request.POST:
            student_id = request.POST.get('student_id')
            if student_id:
                student = get_object_or_404(hoc_vien, pk=student_id)
                # Kiểm tra sĩ số
                if enrolls.count() < class_obj.si_so:
                    enrollments.objects.create(
                        student=student,
                        class_obj=class_obj,
                        enrollment_date=timezone.now()
                    )
                    messages.success(request, 'Thêm học viên vào lớp thành công!')
                else:
                    messages.error(request, 'Lớp đã đủ sĩ số!')
        
        # Xử lý xóa học viên
        elif 'remove_student' in request.POST:
            student_id = request.POST.get('remove_student')
            if student_id:
                enrollment = get_object_or_404(enrollments, student_id=student_id, class_obj=class_obj)
                enrollment.delete()
                messages.success(request, 'Xóa học viên khỏi lớp thành công!')

        return redirect('core:class_detail', pk=pk)

    return render(request, 'classes/class_detail.html', {
        'class_obj': class_obj,
        'enrolls': enrolls,
        'students': students
    })

#-------------------------------
# Schedule Management Views
#-------------------------------
@login_required
def schedule_list(request):
    schedules = schedule.objects.all()
    return render(request, 'core/schedule_list.html', {'schedules': schedules})

@login_required
def schedule_create(request):
    if request.method == 'POST':
        # Handle schedule creation
        pass
    return render(request, 'core/schedule_form.html')

@login_required
def schedule_edit(request, pk):
    schedule = get_object_or_404(schedule, pk=pk)
    if request.method == 'POST':
        # Handle schedule update
        pass
    return render(request, 'core/schedule_form.html', {'schedule': schedule})

@login_required
def schedule_delete(request, pk):
    schedule = get_object_or_404(schedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Lịch học đã được xóa thành công')
        return redirect('core:schedule_list')
    return render(request, 'core/schedule_confirm_delete.html', {'schedule': schedule})

# Attendance Management Views
@login_required
def attendance_list(request):
    attendance_records = attendance.objects.all()
    return render(request, 'core/attendance_list.html', {'attendance_records': attendance_records})

@login_required
def attendance_create(request):
    if request.method == 'POST':
        # Handle attendance creation
        pass
    return render(request, 'core/attendance_form.html')

@login_required
def attendance_edit(request, pk):
    attendance = get_object_or_404(attendance, pk=pk)
    if request.method == 'POST':
        # Handle attendance update
        pass
    return render(request, 'core/attendance_form.html', {'attendance': attendance})

@login_required
def attendance_delete(request, pk):
    attendance = get_object_or_404(attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Điểm danh đã được xóa thành công')
        return redirect('core:attendance_list')
    return render(request, 'core/attendance_confirm_delete.html', {'attendance': attendance})

# Feedback Management Views
@login_required
def feedback_list(request):
    feedbacks = feedback.objects.all()
    return render(request, 'core/feedback_list.html', {'feedbacks': feedbacks})

@login_required
def feedback_view(request, pk):
    feedback = get_object_or_404(feedback, pk=pk)
    return render(request, 'core/feedback_detail.html', {'feedback': feedback})

@login_required
def feedback_delete(request, pk):
    feedback = get_object_or_404(feedback, pk=pk)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Đánh giá đã được xóa thành công')
        return redirect('core:feedback_list')
    return render(request, 'core/feedback_confirm_delete.html', {'feedback': feedback})

#-------------------------------
# Nhan Vien Management Views
#-------------------------------
@login_required
def nhanvien_list(request):
    nhanviens = nhan_vien.objects.all()
    return render(request, 'nhanvien/nhanvien_list.html', {'nhanviens': nhanviens})

@login_required
def nhanvien_create(request):
    if request.method == 'POST':
        form = NhanVienForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm nhân viên thành công!')
            return redirect('core:nhanvien_list')
    else:
        form = NhanVienForm()
    return render(request, 'nhanvien/nhanvien_form.html', {'form': form, 'action': 'Thêm'})

@login_required
def nhanvien_edit(request, pk):
    nv = get_object_or_404(nhan_vien, pk=pk)
    if request.method == 'POST':
        form = NhanVienForm(request.POST, instance=nv)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật nhân viên thành công!')
            return redirect('core:nhanvien_list')
    else:
        form = NhanVienForm(instance=nv)
    return render(request, 'nhanvien/nhanvien_form.html', {'form': form, 'action': 'Sửa'})

@login_required
def nhanvien_delete(request, pk):
    nv = get_object_or_404(nhan_vien, pk=pk)
    if request.method == 'POST':
        nv.delete()
        messages.success(request, 'Xóa nhân viên thành công!')
        return redirect('core:nhanvien_list')
    return render(request, 'nhanvien/nhanvien_confirm_delete.html', {'nhanvien': nv})

#-------------------------------
# Class Type Management Views
#-------------------------------
@login_required
def class_type_list(request):
    types = class_type.objects.all()
    return render(request, 'class_type/class_type_list.html', {'types': types})

@login_required
def class_type_create(request):
    if request.method == 'POST':
        form = ClassTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm loại lớp thành công!')
            return redirect('core:class_type_list')
    else:
        form = ClassTypeForm()
    return render(request, 'class_type/class_type_form.html', {'form': form, 'action': 'Thêm'})

@login_required
def class_type_edit(request, pk):
    ct = get_object_or_404(class_type, pk=pk)
    if request.method == 'POST':
        form = ClassTypeForm(request.POST, instance=ct)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật loại lớp thành công!')
            return redirect('core:class_type_list')
    else:
        form = ClassTypeForm(instance=ct)
    return render(request, 'class_type/class_type_form.html', {'form': form, 'action': 'Sửa'})

@login_required
def class_type_delete(request, pk):
    ct = get_object_or_404(class_type, pk=pk)
    if request.method == 'POST':
        ct.delete()
        messages.success(request, 'Xóa loại lớp thành công!')
        return redirect('core:class_type_list')
    return render(request, 'class_type/class_type_confirm_delete.html', {'class_type': ct})
