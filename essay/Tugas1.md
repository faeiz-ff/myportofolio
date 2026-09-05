
# Tugas 1

## [Pertanyaan Reflektif](https://pbp.cs.ui.ac.id/assignments/individual/tugas-1.html#pertanyaan-reflektif)

> 1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti <section>, <article>, atau <aside>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda? 

Saya menggunakan elemen seperti `<section>`, `<article>`, `<i>` untuk italics, `<em>` untuk emphasis dan elemen semantik
html lainnya untuk menyangkutkan makna ke tujuan elemen itu ada. Hal tersebut membantu 'a11y' untuk _screen readers_, juga
membantu SEO (_Search Engine Optimization_) karena browser memahami bagaimana halaman statis web saya terstruktur.

> 2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile? 

Saya melakukan kesalahan dimana saya tidak mendesain dengan tujuan awal _mobile-first_. Jadi, banyak elemen harus saya susun
ulang. Saya memakai banyak `flexbox` dalam css saya untuk mengatur tata letak dengan intuitif, umumnya saya hanya mengubah 
arah flex dari yang kiri-kanan menjadi atas-bawah. Pengukuran elemen sangat dibantu dengan "pengukuran relatif" seperti 
persentase tinggi/lebar `svh`/`svw` (Smallest Viewport Height/Width, agar layar mobile menghitung ukuran tinggi/lebar 
tanpa halangan search bar) dan tekstual seperti `rem` yang menyesuaikan ukuran elemen relatif terhadap ukuran font layar.

> 3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya? 

Untuk portofolio murni, saya rasa website statis sudah memberi fungsionalitas yang cukup. Namun, saya memikirkan saya ingin
menambahkan suatu blogpost yang saya bisa edit _in-web_ kalau bisa, dan blog ini akan di setor ke suatu database yang website
bisa _fetch_ dan tampilkan html yang sudah di-_render_. Saya juga sejujurnya ingin menambahkan interaktifitas dalam halaman
dengan javascript, tetapi saya akan simpan untuk poin bonus tugas selanjutnya :)))

## AI Disclosure

Semua kode dalam tugas 1 ini __100% diketik tanpa menggunakan AI__. Saya juga __tidak memakai AI untuk mendesain, memberi ide,
ataupun mengedit hal-hal tekstual__ dalam tugas ini. __Namun__, saya tidak jarang membaca hasil search result google yang
ter-ringkas Gemini AI, tetapi tidak ada kode yang saya _copy-paste_.

## Referensi

- Django Template Inheritance: [Django documentation](https://docs.djangoproject.com/en/6.1/ref/templates/language/#template-inheritance)
- CSS Flexbox: [css-tricks](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- CSS Fadein: [carmenansio](https://www.carmenansio.com/articles/css-entry-exit-animations) 
- prefers-color-scheme: [web.dev](https://web.dev/articles/prefers-color-scheme)
- Referensi CSS: [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS)
- Referensi HTML: [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML)
