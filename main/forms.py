from django.forms import (
    CharField,
    DateInput,
    ModelForm,
    TextInput,
    Textarea,
    URLInput,
)

from main.models import Blog, Project


# Decorates ModelForm class with an additional password field on it
# Kinda hacky, but this is temporary anyway. TODO: swap with proper auth
def ProtectedForm(cls):
    class InnerForm(cls):
        password = None

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password'] = CharField()

            passwordField = self.fields['password']
            passwordField.required = True
            passwordField.widget = TextInput()
            passwordField.widget.label = 'Password'
            passwordField.widget.attrs['placeholder'] = \
                'Password untuk validasi pengiriman form'

    return InnerForm


@ProtectedForm
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
            'started_at': DateInput(),
            'ended_at': DateInput(),
        }


@ProtectedForm
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
            'created_at': DateInput(),
        }
