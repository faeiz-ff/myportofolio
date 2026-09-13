
# Tugas 2

Dalam tugas ini, mengikuti tutorial 2, saya menambahkan model baru yaitu `Project` dan `Blog`. 

Model `Project` tidak begitu beda dengan `Experience` dari tutorial 2. Hanya saja semua `Project` saya pasti akan mempunyai link git di suatu cloud service, dan suatu link lain yang opsional untuk diisi. `Project` mempunyai started_at dan ended_at juga seperti model `Experience` saya. Jika ended_at bernilai `None`, proyek itu belum selesai dan masih  dalam tahap pembangunan. Overall, mengerjakan model `Project` tidak jauh beda dari mengerjakan model `Experience`, saya _copy-paste_ banyak hal.

Model `Blog` merepresentasikan blog yang saya ketik, saya memikirkan setidaknya 3 atribut untuk blog: Judul, Tanggal dibuat, dan isi blognya. Namun, berdasarkan pengalaman saya menulis blog, saya sering mengutip suatu website tertentu di dalam teks. Saya juga tidak jarang memberi _emfasis_ kepada beberapa kata ataupun memakai _foreign words_, yang dalam peraturan [PUEBI](https://puebi.js.org/huruf/miring) harus ditulis miring (yang dalam html: dibungkus dengan elemen <i>italic</i>). Maka dari itu, untuk mempermudah penulisan blog kedepannya, saya akan memakai format Markdown yang lebih ringkas untuk ditulis. 

Untuk mengubah teks markdown ke html, saya memakai _external library_ [python-markdown](https://python-markdown.github.io/). _Library_ tersebut secara mudah akan menerjemah teks markdown menjadi teks html. _Namun_, saya tahu proses pengubahan html melalui sebuah input teks [bisa berbahaya](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/XSS). Oleh sebab itu, hanya saya yang boleh menulis ke _database_ melalui page `admin`. Untuk sekarang, saya pribadi yang memastikan input markdown saya tidak memuat elemen html yang aneh. Untuk kedepannya apabila saya mengizinkan orang lain untuk _write_ ke _database_ (misalnya, komentar, atau apapun), saya tahu untuk meng-_sanitize_ input teksnya terlebih dahulu.

## [Pertanyaan Reflektif](https://pbp.cs.ui.ac.id/assignments/individual/tugas-2.html#pertanyaan-reflektif)

> 1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template. 

Saat pengguna membuka halaman portofolio, _request_ HTTP masuk dan meminta halaman dengan _routing_ (nama lengkap 'link') yang sesuai. _Routing_ tersebut didefinisikan pada `urls.py` dalam folder portofolio (proyek). Pada `urls.py` tersebut, terdapat bahwa routing yang berawalan `''` (teks kosong) semua didelegasikan pada _routing_ URL milik `main`. Selanjutnya, `urls.py` dalam folder `main` mencocokkan _routing_ yang diharapkan, lalu situs akan memanggil fungsi yang telah terdefinisi dalam `views.py` untuk mengembalikan suatu _response_ HTTP.

Dalam Views, _request_ dari pengguna dapat diolah, tetapi untuk portofolio ini, hanya halaman yang kita pedulikan. Views akan mengatur keluar masuk data sesuai _request_ pengguna. Dalam semua contoh yang saya buat, semua Views akan menampilkan sebuah data yang saya tulis dalam _database_. Apabila pengguna masuk ke direktori `'proyek'`, semua proyek saya akan ditampilkan. Data yang diambil ini merupakan sebuah model `Project` yang saya definisikan bentuknya. Data ini disimpan dalam _database table_ yang menyimpan atribut `Project` saya baris per baris per data. Setelah diambil datanya, Views memasukkan data dalam konteks Template, yang merupakan file html dengan atribut dinamis sesuai konteks yang diberi views.

Setelah Views mengembalikan halaman Template html yang sudah diisikan konteks dari suatu Model data dalam _database_, halaman pun tersajikan dalam _browser_

> 2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi. 

Karena jika ditulis langsung di dalam template, perubahan akan susah diterapkan. Jika saya ingin menambahkan `Blog` baru misalnya, saya harus menulis ulang semua elemen html termasuk header, footer, dan link lainnya. Dan jika saya ingin mengubah header, footer, atau layout halaman blog saya, saya harus mengubahnya secara manual di __semua halaman blog__. Dengan MVT, saya dapat mendefinisikan sebuah yaa.. __Template__ yang seragam untuk menampilkan data saya yang seragam. Hal ini tentunya sangat mempermudah pemeliharaan aplikasi, apalagi yang sering berubah datanya.

> 3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut. 

Ketika saya mengubah bentuk model saya, saya mengeksekusi `makemigrations` untuk mendefinisikan perubahannya pada sistem sejarah bentuk model milik Django. Saat saya ingin mengakses langsung datanya, Django akan kebingungan dengan dua bentuk Model yang berbeda, karena saya belum apa apakan data yang _sudah ada_ dalam _database_, saya hanya sudah mengubah bentuk datanya diluar _database_. Untuk itu, saya mengeksekusi `migrate` untuk menerapkan bentuk data yang paling terkini terhadap _database_.

## AI Disclosure

Semua kode dalam tugas 2 ini __100% diketik tanpa menggunakan AI__. Saya juga __tidak memakai AI untuk mendesain, memberi ide,
ataupun mengedit hal-hal tekstual__ dalam tugas ini.

## Referensi

datetime = [Python3 Docs: datetime](https://docs.python.org/3/library/datetime.html)
models field = [Django docs](https://docs.djangoproject.com/en/6.1/ref/models/fields)
admin page = [Django docs](https://docs.djangoproject.com/en/6.1/ref/contrib/admin)
url routing = [Django docs](https://docs.djangoproject.com/en/6.1/topics/http/urls/)
queries = [Django docs](https://docs.djangoproject.com/en/6.1/topics/db/queries/)
url reverse (for test) = [Django docs](https://docs.djangoproject.com/en/6.1/ref/urlresolvers/#reverse)
python-markdown = [Docs](https://python-markdown.github.io/)
