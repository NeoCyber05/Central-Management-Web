from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Count, Sum, Avg
from .models import NhanVien, Teacher, HocVien, Class, Enrollment, Attendance, FeedBack
from django.contrib import messages

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

@login_required
def dashboard(request):
    # Statistics for dashboard
    total_students = HocVien.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()
    total_enrollments = Enrollment.objects.count()

    # Calculate ratings if FeedBack model exists and has these fields
    avg_teacher_rating = FeedBack.objects.aggregate(Avg('teacher_rate'))['teacher_rate__avg'] or 0
    avg_class_rating = FeedBack.objects.aggregate(Avg('class_rate'))['class_rate__avg'] or 0

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_enrollments': total_enrollments,
        'avg_teacher_rating': avg_teacher_rating,
        'avg_class_rating': avg_class_rating,
    }
    return render(request, 'core/admin/dashboard.html', context)
# User Management
@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'core/admin/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_add(request):
    if request.method == 'POST':
        # Process the form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = 'is_staff' in request.POST
        is_superuser = 'is_superuser' in request.POST

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên người dùng đã tồn tại')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            messages.success(request, f'Người dùng {username} đã được tạo thành công')
            return redirect('core:user_list')

    return render(request, 'core/admin/user_form.html', {'action': 'Thêm'})

@login_required
@user_passes_test(is_admin)
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Process the form data
        email = request.POST.get('email')
        is_staff = 'is_staff' in request.POST
        is_superuser = 'is_superuser' in request.POST

        user.email = email
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        if 'password' in request.POST and request.POST.get('password'):
            user.set_password(request.POST.get('password'))

        user.save()
        messages.success(request, f'Người dùng {user.username} đã được cập nhật')
        return redirect('core:user_list')

    return render(request, 'core/admin/user_form.html', {
        'action': 'Sửa',
        'user': user
    })

@login_required
@user_passes_test(is_admin)
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Người dùng {username} đã bị xóa')
        return redirect('core:user_list')

    return render(request, 'core/admin/user_confirm_delete.html', {'user': user})

# Class Management
@login_required
@user_passes_test(is_admin)
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'core/admin/class_list.html', {'classes': classes})

# Teacher Management
@login_required
@user_passes_test(is_admin)
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'core/admin/teacher_list.html', {'teachers': teachers})

# Student Management
@login_required
@user_passes_test(is_admin)
def student_list(request):
    students = HocVien.objects.all()
    return render(request, 'core/admin/student_list.html', {'students': students})