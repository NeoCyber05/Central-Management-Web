from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = 'Tạo các nhóm người dùng và phân quyền'

    def handle(self, *args, **kwargs):
        # Tạo nhóm Admin
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        admin_group.permissions.set(Permission.objects.all())
        self.stdout.write('✔ Admin group created with all permissions')

        # Tạo nhóm Nhân viên
        staff_group, _ = Group.objects.get_or_create(name='Staff')
        permissions = Permission.objects.filter(
            content_type__app_label='yourapp',
            codename__in=[
                'add_hocvien', 'change_hocvien', 'delete_hocvien', 'view_hocvien',
                'add_lophoc', 'change_lophoc', 'view_lophoc',
                'add_enrollments', 'view_enrollments',
                'add_attendance', 'view_attendance'
            ]
        )
        staff_group.permissions.set(permissions)
        self.stdout.write('✔ Staff group created with assigned permissions')

        # Tạo nhóm Giáo viên
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        permissions = Permission.objects.filter(
            codename__in=[
                'view_schedule', 'add_attendance', 'change_grades', 'view_grades'
            ]
        )
        teacher_group.permissions.set(permissions)
        self.stdout.write('✔ Teacher group created')

        # Tạo nhóm Học viên
        student_group, _ = Group.objects.get_or_create(name='Student')
        permissions = Permission.objects.filter(
            codename__in=['view_hocvien', 'view_schedule', 'view_grades']
        )
        student_group.permissions.set(permissions)
        self.stdout.write('✔ Student group created')
