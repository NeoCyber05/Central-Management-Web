from django import forms
from .models import teacher, hoc_vien , clazz, nhan_vien

class TeacherForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
    ]
    TRINH_DO_CHOICES = [
        ('Cử nhân', 'Cử nhân'),
        ('Thạc Sĩ', 'Thạc Sĩ'),
        ('Tiến Sĩ', 'Tiến Sĩ'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label="Giới tính")
    trinh_do = forms.ChoiceField(choices=TRINH_DO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label="Trình độ")

    class Meta:
        model = teacher
        fields = ['full_name', 'gender', 'birth_day', 'email', 'sdt', 'address', 'trinh_do']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_day': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'sdt': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


    
class HocVienForm(forms.ModelForm):
    class Meta:
        model = hoc_vien
        fields = [ 'full_name', 'gender', 'birth_day', 'email', 'sdt', 'address']

class ClassForm(forms.ModelForm):
    class Meta:
        model = clazz
        fields = ['class_id', 'nhan_vien', 'teacher', 'class_name', 'type', 'room', 'khai_giang', 'ket_thuc', 'si_so', 'price']
        widgets = {
            'nhan_vien': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'room': forms.TextInput(attrs={'class': 'form-control'}),
            'khai_giang': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ket_thuc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'si_so': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class NhanVienForm(forms.ModelForm):
    class Meta:
        model = nhan_vien
        fields = ['full_name', 'gender', 'birth_day', 'email', 'sdt', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_day': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'sdt': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }