
# Tugas 5

Dalam tugas ini saya hanya benar-benar refaktor apa yang terjadi di tutorial 5, karena jujur saja, templatenya sangat bertumpuk tumpuk dan berantakan.

Saya merefaktor fungsionalitas ajax, dipisah menjadi beberapa file terpisah agar lebih enak dilihatnya dan diaturnya. NAMUN, ini membuat suatu dependency hell karena 'saya' bisa saja tidak tahu bahwa variabel global yang dipakai sudah terdefinisi atau tidak. `templates/components/ajax-instances.html` memberi konteks variabel global melalui sintaks `{%  %}` django untuk routing url, mengetahui superuser, dan token csrf, ke elemen <script>, lalu file dalam `static/js/*.js` mengambil konteksnya. Ini mempersimpel pengulangan kode walau memperumit navigasi. Saya harus akui ini agak spagheti, tapi saya berpendapat tidak lebih buruk daripada template tutorial 5 yang 'memuntahkan' <script>nya ke html.

## [Pertanyaan Reflektif](https://pbp.cs.ui.ac.id/assignments/individual/tugas-5.html#pertanyaan-reflektif)

> 1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

Debouncing bertindak semacam _delay_ agar javascript tidak terus menerus _fetch_ sebuah request. Dalam konteks kode saya, misalnya search query, diberi debounce agar setiap huruf yang saya ketik/hapus tidak mengeksekusi _fetch_ secara langsung, melainkan mengunggu dulu setelah saya berhenti mengetik lalu baru _fetch_ query title saya.

> 2. Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await? 

Dalam keanehan dunia asinkronus javascript, await digunakan dalam fungsi asinkronus agar memberhentikan proses kode sebelum menerima suatu 'efek' asinkronus, yaitu fetching resource, atau operasi komputasi asinkronus lain. await sebenarnya membungkus kode Promise dengan .then() dan try/catch otomatis agar syntaxnya lebih modern (a fugazi). Jadi tanpa await, sebenarnya proses tidak akan berhenti untuk menerima data, melainkan langsung menerima objek Promise secara utuh, dan melanjutkan eksekusi dengan type error di baris baris berikutnya apabila memakai javascript, i mean its a weakly-dynamic-type language whatd you expect.

> 3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django! 

Balik lagi ke dasar, HTML hanyalah sebuah text yang dikirim lewat HTTP. Semua teks input yang berisikan html, akan di-parse sebagai HTML. Apabila seorang user ingin menamai dirinya `<button>Hi!</button>`, maka tergambarlah tombol di username dia di layarnya. Hal ini bisa dicegah dengan _escaping_, yaitu mengubah semua data yang "valid html" menjadi teks biasa, niatnya kita menolak me-render html seenak jidat user.

Data dari template Django otomatis terfilter (_escaped_), jadi semua datanya aman (tidak akan dianggap html), kecuali filter |safe dieksekusi. Untuk JavaScript, sebaliknya, dengan innerHTML, semua string valid html akan di-parse sebagai html, kita harus memfilter manual melalui `escapeHTML()` dengan mengubah data valid html menjadi teks alternatif yang jika dirender akan secara harfiah merender teks tersebut dan bukan elemen html. XSS adalah semacam teknik peretasan yang memanfaatkan celah keamanan ini.

## AI Disclosure

Semua kode dan teks dalam tugas 5 ini __100% diketik tanpa menggunakan AI__. Saya juga __tidak memakai AI untuk mendesain, memberi ide, ataupun mengedit hal-hal tekstual__ dalam tugas ini.

## Referensi 
- https://docs.djangoproject.com/en/6.1/ref/templates/builtins/#if
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS/Promises 
- https://docs.djangoproject.com/en/6.1/topics/security/ 

