
# Tugas 4

Dalam tugas ini, mengikuti tutorial 4, saya menambahkan fitur untuk memberi star untuk Model Proyek dan Blog.

Saya menghapus sistem otentikasi naif yang sebelumnya saya pakai. Saya menggunakan dan bahkan membuat decorator lagi disini untuk otentikasi. Saya menggunakan dekorator `login_required` dan membuat dekorator `group_required` untuk cek apabila user berada dalam suatu kelompok grup atau tidak, kalau tidak, akan raise PermissionDenied yang akan meredirect ke halaman 403.html, "unauthorized".

Saya kebanyakan hanya merapihkan beberapa halaman seperti _flushing_ message yang sebelumnya tertumpuk karena saya tidak tahu harus ditampilkan -- Saya terkadang langsung menghapus bagian dari template-dari-asdos yang saya rasa tidak perlu, jadi sepertinya itu terlewat -- agar tidak menumpuk. 

## AI Disclosure

Semua kode dan teks dalam tugas 4 ini __100% diketik tanpa menggunakan AI__. Saya juga __tidak memakai AI untuk mendesain, memberi ide, ataupun mengedit hal-hal tekstual__ dalam tugas ini.

## Referensi 
- https://docs.djangoproject.com/en/6.1/ref/contrib/messages/ 
- https://css-tricks.com/almanac/rules/k/keyframes/ 
- https://docs.djangoproject.com/en/6.1/topics/auth/default/ 
- https://www.stanza.dev/courses/django-authentication/groups-roles/django-authentication-groups-basics 
