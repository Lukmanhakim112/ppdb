from primaseru import base_layouts as prim_layouts

from crispy_forms.layout import Layout, Fieldset, Row, Div, HTML, Field


DASHBOARD_STATUS = Layout(
    Row(
        Div(HTML('<h2 class="judul">Pilih Jurusan {{ name|title }}</h2><p>Silahkan pilih jurusan yang dikehendaki (click Edit Data), jika semua data telah sesuai, centang <samp class="text-danger">Diterima</samp> dan click save. Jika ingin mengedit data, silahkan click tombol <samp>edit</samp>, dan edit data, lalu save.</p>'),
            css_class="col-lg-10 col-md-12 border rounded shadow-sm mr-2 bg-white p-2"),
        Div(Fieldset(None,
                     HTML('<button role="submit" type="submit" class="btn btn-outline-success btn-block save-verify">Save</button> \
                     <button role="button" type="button" class="btn btn-outline-danger btn-block submit-parent" id="activate-form" data-toggle="button" aria-pressed="false">Edit Data</button>'),
                     css_class="p-2"
        ), css_class="col-md-12 col-lg rounded text-center border shadow-sm bg-white"),
        Div(
            Field('accepted', css_class="custom-select custom-select-sm"),
            Field('major', css_class="custom-select custom-select-sm"),
            css_class="col-md-12 rounded border shadow-sm mt-3 p-3 bg-white"),
    ),
)

DASHBOARD_STUDENT = Layout(
    Row(
        Div(HTML('<h2 class="judul">Verifikasi Data {{ name|title }}</h2><p>Silahkan lakukan verifikasi data calon siswa, jika semua data telah sesuai, centang <samp class="text-danger">verified</samp> dan click save. Jika ingin mengedit data, silahkan click tombol <samp>edit</samp>, dan edit data, lalu save.</p>'),
            css_class="col-lg-10 col-md-12 border rounded shadow-sm mr-2 bg-white p-2"),
        Div(Fieldset(None,
            'verified',
                     HTML('<button role="submit" type="submit" class="btn btn-outline-success btn-block save-verify">Save</button> \
                     <button role="button" type="button" class="btn btn-outline-danger btn-block submit-parent" id="activate-form" data-toggle="button" aria-pressed="false">Edit Data</button>'),
                     css_class="p-2"
        ), css_class="col-md-12 col-lg rounded text-center border shadow-sm bg-white"),
        Div(prim_layouts.STUDENT_BASE_LAYOUT, css_class="col-md-12 rounded border shadow-sm mt-3 p-3 bg-white"),
    ),
)


DASHBOARD_PARENT = Layout(
    Row(
        Div(HTML('<h2 class="judul">Verifikasi Data {{ name|title }}</h2><p>Silahkan lakukan verifikasi data orang tua calon siswa, jika semua data telah sesuai, centang <samp class="text-danger">verified</samp> dan click save. Jika ingin mengedit data, silahkan click tombol <samp>edit</samp>, dan edit data, lalu save.</p>'),
            css_class="col-lg-10 col-md-12 border rounded shadow mr-2 bg-white p-2"),
        Div(Fieldset(None,
            'verified',
                     HTML('<button role="submit" type="submit" class="btn btn-outline-success btn-block save-verify">Save</button> \
                     <button role="button" type="button" class="btn btn-outline-danger btn-block submit-parent" id="activate-form" data-toggle="button" aria-pressed="false">Edit Data</button>'),
                     css_class="p-2"
        ), css_class="col-md-12 col-lg rounded text-center border shadow bg-white"),
        Div(prim_layouts.PARENT_BASE_LAYOUT, css_class="col-md-12 rounded shadow border mt-3 p-3 bg-white"),
    ),
)

DASHBOARD_MAJOR = Layout(
    Row(
        Div(HTML('<h2 class="judul">Verifikasi Data {{ name|title }}</h2><p>Silahkan lakukan verifikasi data jurusan calon siswa, jika semua data telah sesuai, centang <samp class="text-danger">verified</samp> dan click save. Jika ingin mengedit data, silahkan click tombol <samp>edit</samp>, dan edit data, lalu save.</p>'),
            css_class="col-lg-10 col-md-12 border rounded mr-2 bg-white p-2"),
        Div(Fieldset(None,
            'verified',
                     HTML('<button role="submit" type="submit" class="btn btn-outline-success btn-block save-verify">Save</button> \
                     <button role="button" type="button" class="btn btn-outline-danger btn-block submit-parent" id="activate-form" data-toggle="button" aria-pressed="false">Edit Data</button>'),
                     css_class="p-2"
        ), css_class="col-md-12 col-lg rounded text-center border bg-white"),
        Div(prim_layouts.MAJOR_BASE_LAYOUT, css_class="col-md-12 rounded border mt-3 p-3 bg-white"),
    ),
)


DASHBOARD_FILES = Layout(
    Row(
        Div(HTML('<h2 class="judul">Verifikasi Data {{ name|title }}</h2><p>Silahkan lakukan verifikasi data berkas calon siswa, jika semua data telah sesuai, centang <samp class="text-danger">verified</samp> dan click save. Jika ingin mengedit data, silahkan click tombol <samp>edit</samp>, dan edit data, lalu save. Isi pesan jika ada berkas yang tidak valid.</p>'),
            css_class="col-lg-10 col-md-12 border rounded mr-2 bg-white p-2"),
        Div(Fieldset(None,
            'verified',
                     HTML('<button role="submit" type="submit" class="btn btn-outline-success btn-block save-verify">Save</button> \
                     <button role="button" type="button" class="btn btn-outline-danger btn-block submit-parent" id="activate-form" data-toggle="button" aria-pressed="false">Edit Data</button>'),
                     css_class="p-2"
        ), css_class="col-md-12 col-lg rounded text-center border bg-white"),
        Div('msg', css_class="col-md-12 col-lg-12 border rounded bg-white mt-3 px-4 py-1"),
        Div(prim_layouts.FILE_BASE_LAYOUT, css_class="col-md-12 rounded border mt-3 p-3 bg-white"),
    ),
)
