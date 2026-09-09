from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Faeiz Faiza Fasha",
        "npm": "2506602196",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Seniman, insinyur perangkat lunak, pemrogram rekreasional. "
            "Cinta dengan semua teori komputasi sejak saya baru lahir. "
            "Tertarik dengan systems programming, teknik kompilator. "
            "Suka berbahasa Zig dan TypeScript; "
            "mengenali banyak bahasa lain. Selamanya pelajar. "
        ),
    }
    return render(request, "about.html", context)


def show_experience(request):
    context = {
        "name": "Faeiz Faiza Fasha",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
