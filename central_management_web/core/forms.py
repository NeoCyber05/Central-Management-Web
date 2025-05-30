from django import forms
from .models import teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = teacher
        fields = ['teacher_id', 'full_name', 'gender', 'birth_day', 'email', 'sdt', 'address', 'trinh_do']