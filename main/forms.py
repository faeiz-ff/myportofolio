from django.forms import (
    DateInput,
    ModelForm,
    TextInput,
    Textarea,
    URLInput,
)
from django.forms.widgets import Select

from main.models import Blog, Experience, Project


class DatePicker(DateInput):
    input_type = 'date'


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'git_link',
            'other_link',
            'description',
            'started_at',
            'ended_at',
        ]

        labels = {
            'title': 'Nama proyek',
            'git_link': 'Link origin git proyek',
            'other_link': 'Link lainnya tentang proyek',
            'description': 'Deskripsi proyek',
            'started_at': 'Tanggal proyek dimulai',
            'ended_at': 'Tanggal proyek diselesaikan',
        }

        widgets = {
            'title': TextInput(
                attrs={
                    'placeholder': 'Portofolio Website',
                    'maxlength': 255,
                }
            ),
            'git_link': URLInput(
                attrs={
                    'placeholder': 'https://github.com/faeiz-ff/',
                }
            ),
            'other_link': URLInput(
                attrs={
                    'placeholder': 'https://example.com',
                },
            ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Deskripsi proyek',
                    'rows': 3,
                }
            ),
            'started_at': DatePicker(),
            'ended_at': DatePicker(),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            'title',
            'description',
            'category',
            'started_at',
            'ended_at',
        ]

        labels = {
            'title': 'Nama pengalaman',
            'description': 'Deskripsi pengalaman',
            'category': 'kategori pengalaman',
            'started_at': 'Tanggal pengalaman dimulai',
            'ended_at': 'Tanggal pengalaman diselesaikan',
        }

        widgets = {
            'title': TextInput(
                attrs={
                    'placeholder': 'Nama pengalaman',
                    'maxlength': 255,
                }
            ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Deskripsi pengalaman',
                    'rows': 3,
                }
            ),
            'category': Select(),
            'started_at': DatePicker(),
            'ended_at': DatePicker(),
        }


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title',
            'text',
            'created_at',
        ]

        labels = {
            'title': 'Judul blog',
            'text': 'Isi blog (markdown)',
            'created_at': 'Tanggal blog dibuat',
        }

        widgets = {
            'title': TextInput(
                attrs={
                    'placeholder': 'Pemikiran Saya',
                    'maxlength': 255,
                }
            ),
            'text': Textarea(
                attrs={
                    'placeholder': 'Pada suatu hari...',
                    'rows': 3,
                }
            ),
            'created_at': DatePicker(),
        }
