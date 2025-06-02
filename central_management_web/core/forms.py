from django import forms
from .models import teacher, hoc_vien, clazz, nhan_vien, class_type

class TeacherForm(forms.ModelForm):
    class Meta:
        model = teacher
        fields = ['full_name', 'gender', 'birth_day', 'email', 'sdt', 'address', 'trinh_do']
        widgets = {
            'birth_day': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('M', 'Nam'), ('F', 'Nữ')]),
            'trinh_do': forms.Select(choices=[('Cử nhân', 'Cử nhân'), ('Thạc Sĩ', 'Thạc Sĩ'), ('Tiến Sĩ', 'Tiến Sĩ')])
        }

class HocVienForm(forms.ModelForm):
    class Meta:
        model = hoc_vien
        fields = ['full_name', 'gender', 'birth_day', 'email', 'sdt', 'address']
        widgets = {
            'birth_day': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('M', 'Nam'), ('F', 'Nữ')])
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model = clazz
        fields = ['class_name', 'nhan_vien', 'teacher', 'type', 'room', 'khai_giang', 'ket_thuc', 'si_so', 'price']
        widgets = {
            'khai_giang': forms.DateInput(attrs={'type': 'date'}),
            'ket_thuc': forms.DateInput(attrs={'type': 'date'})
        }

class NhanVienForm(forms.ModelForm):
    class Meta:
        model = nhan_vien
        fields = ['full_name', 'gender', 'birth_day', 'email', 'sdt', 'address']
        widgets = {
            'birth_day': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('M', 'Nam'), ('F', 'Nữ')])
        }

class ClassTypeForm(forms.ModelForm):
    class Meta:
        model = class_type
        fields = ['describe', 'code']