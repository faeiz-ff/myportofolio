
# Tugas 3 

Dalam tugas ini, mengikuti tutorial 3, saya menambahkan fungsionalitas CRUD berbasis Form, untuk semua Model yang saya buat sebelumnya.

Saya suka _refactoring_, dan saya tidak suka melanggar [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself), jadi saya buat View yang mengolah request untuk Create/Update/Delete menjadi generik (dapat mengolah data apa saja yang sesuai kriterianya). Saya pertama-tama hanya _copy-paste_ fungsionalitas CRUD tutorial 3 terlebih dahulu yang saya terapkan di model Project; mulai refaktor untuk model Blog, dan saat benar-benar terabstraksi saya terapkan kepada model Experience. Saya cukup lama menentukan abstraksi yang tepat untuk `create_or_update_instance()` dan `delete_instance()` dalam `main/instance_views.py`, tapi saya rasa sekarang abstraksinya sudah cukup. Namun, saya sepertinya lumayan melanggar [SRP](https://en.wikipedia.org/wiki/Single-responsibility_principle) dalam fungsi `create_or_update_instance()` dan halaman `model_form.html`, tapi apa boleh buat, Django bisa melakukan update dan create dalam metode `.save()` yang sama, saya cukup malas untuk mengulang kode yang hampir sama.

Saya suka menggunakan fitur bahasa dengan semaksimal mungkin. Dalam python, hampir semuanya adalah nilai, termasuk `class` dan `function` saya cukup lempar sana-sini tanpa hirauan apa apa. _I can't help it_. Saya gunakan seluruh python kalau saya disuruh memakai python. `ProtectedForm` dalam `main/forms.py` adalah dekorator yang 'memasangkan' `Field` _password_ ke sebuah kelas. Jadi jika saya nanti memakai sistem otentikasi yang lebih terstruktur, saya bisa tinggal menghapus dekorasinya. Begitu juga dengan `MODEL_VIEW_INFO` dalam `main/instance_views.py` di mana saya menyimpan sebuah `class` dalam _object_ yang disimpan di `dictionary`, agar saya dapat mengaksesnya dengan `str` saja, mudah diubah nantinya apabila ada penggantinamaan URL.

Dalam hubungan model-view data-data saya, semuanya _insecure_ terhadap XSS apabila semua orang dapat mengganti isi kontennya, apalagi `Blog` yang erat kaitannya pada 'pemikiran saya', saya tidak mau ada orang jahil yang mengubah-ubah isi konten seenaknya. Jadi saya membuat sistem password sederhana yang cek isi Form setiap saya me-POST ke server, _create_ dan _update_ mempunyai kolom password untuk validasi form, begitu pula dengan _delete_ pada _pop up_ konfirmasi. _Input_ Form ini akan di cek terhadap `FORM_PASSWORD` yang berada dalam `.env` pws. 

## [Pertanyaan Reflektif](https://pbp.cs.ui.ac.id/assignments/individual/tugas-3.html#pertanyaan-reflektif)

> 1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut! 

Saya menggunakan ModelForm karena hal itu akan otomatis membuat Form dari bentuk Model yang saya terapkan kepada form itu. Saya hanya harus set-up `label` dan `placeholder` untuk masing-masing Input dari Form. 

CSRF token adalah salah satu pencegahan suatu serangan yang berasal dari luar situs. Tanpa CSRF Token, seseorang dapat mengirim suatu link situs eksternal jahat yang jika dibuka dapat mengeksekusi request 'jahat' langsung ke situs target, dengan memanfaatkan _Session Cookie_ yang browser otomatis akan taruh bersama requestnya. Dengan CSRF token bawaan Django yang sudah teracak dengan _secret_ otomatis, penyerang tidak dapat mengirimnya lewat request di situs eksternal karena sifat tokennya yang harus dibaca di situs yang sama (CORS). Ini lebih menjamin bahwa request yang saya kirim benar-benar dari saya yang mengakses Formnya melalui request GET yang sebelumnya saya eksekusi, di mana browser akan otomatis menyangkutkan cookie csrf_token karena berasal dari situs yang sama.

> 2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML? 

Lebih mudah dibaca, dibuat, disimpan, dan di-_parsing_. Menurut saya alasan yang paling terakhir yang membuat adoptasinya luas, karena hanya [seperti ini](https://www.json.org/json-en.html) _grammar_-nya. JSON juga merupakan subset dari _grammar_ JavaScript yang semua orang web sudah familiar. 

> 3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan? 

Alur saya untuk mengembalikan data portofolio adalah melalui `/api/`, saat request masuk misalnya kepada `/api/proyek`, view `get_projects_json` akan terpanggil yang didalamnya memanggil `get_instances_json(request, 'project')`. Dalam fungsi itu, semua data dari database akan ter-serialisasi menjadi sebuah string, lalu fungsi mengembalikan HttpResponse dengan tipe konten JSON. 

Perlunya serialisasi karena response/request HTTP hanya bisa mengirim text/bytes, bukan objek Model itu sendiri. JSON adalah format dari teks yang bisa dibaca ulang (di-_parse_) menjadi sebuah objek, jadi saat menulis response untuk dikembalikan ke browser, fungsi `get_instances_json` men-serialisasi (mengubah objek menjadi representasi teks format JSON) objek terlebih dahulu, baru mengembalikan HttpResponse dengan teks JSON yang ter-serialisasi dan semua metadata seperti '_content-type_' JSON.

## AI Disclosure
Semua kode dan teks dalam tugas 3 ini __100% diketik tanpa menggunakan AI__. Saya juga __tidak memakai AI untuk mendesain, memberi ide,
ataupun mengedit hal-hal tekstual__ dalam tugas ini.

## Referensi
- https://daniel.feldroy.com/posts/overloading-form-fields
- https://realpython.com/primer-on-python-decorators/
- https://docs.djangoproject.com/en/6.1/ref/request-response/
- https://docs.djangoproject.com/en/6.1/ref/models/instances/#how-django-knows-to-update-vs-insert
- https://docs.djangoproject.com/en/6.1/topics/forms/
- https://stackoverflow.com/questions/61077802/how-to-use-a-datepicker-in-a-modelform-in-django
- https://docs.djangoproject.com/en/6.1/topics/http/urls/#url-namespaces-and-included-urlconfs
- https://docs.djangoproject.com/en/6.1/ref/csrf/ 
- https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF 
- https://stackoverflow.com/questions/74412651/csrf-tokens-vs-session-cookies 
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS 
