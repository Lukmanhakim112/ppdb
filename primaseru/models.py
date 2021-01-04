from django.db import models
from django.utils import timezone

from PIL import Image

from users.models import CustomUser
from . import choices


def user_directory_path(instance, filename):
    return f'berkas_{instance.student.id}_{instance.student.full_name}/{filename}'

class StudentFile(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    msg = models.CharField("Pesan", max_length=120, null=True, blank=True)
    ra_sem_1 = models.FileField('Rapor Semester 1', upload_to=user_directory_path)
    ra_sem_2 = models.FileField('Rapor Semester 2', upload_to=user_directory_path)
    ra_sem_3 = models.FileField('Rapor Semester 3', upload_to=user_directory_path)
    ra_sem_4 = models.FileField('Rapor Semester 4', upload_to=user_directory_path)
    ra_sem_5 = models.FileField('Rapor Semester 5', upload_to=user_directory_path, null=True, blank=True)
    color_blind_cert = models.FileField('Semester Keterangan Tidak Buta Warna', upload_to=user_directory_path)
    healty_cert = models.FileField('Surat Keterangan Sehat', upload_to=user_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Raport {self.student}'

class PhotoProfile(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField('Photo', default='default_photo.png', upload_to='profile_pics')

    def __str__(self):
        return f'Photo {self.student}'

    def save(self, *args, **kwargs):
        super(PhotoProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 400:
            output_size = (400,400)
            img.thumbnail(output_size)
            img.save(self.image.path)


class StudentProfile(models.Model):
    verified = models.BooleanField(default=False)
    # Personal Information
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    no_regis = models.PositiveIntegerField('No. Pendaftaran', help_text="Bisa Konfirmasi Ke Bagian Pendaftaran, Contoh : 221321", unique=True, null=True)
    sex = models.CharField('Jenis Kelamin', max_length=1, choices=choices.SEX)
    religion = models.CharField('Agama', choices=choices.RELIGION, max_length=3)
    handpone = models.PositiveIntegerField('No. HP', null=True)
    city_born = models.CharField('Tempat Lahir', max_length=100, help_text="Contoh: Kabupaten Bandung")
    date_born = models.DateField('Tanggal Lahir', null=True)
    social_media = models.CharField('Akun Sosial Media', max_length=100, help_text="Seperti Alamat Twitter, IG, atau FB")
    achievement = models.TextField('Prestasi Akademik/Non Akademik', max_length=120, null=True, blank=True, help_text="Contoh : Juara 3 Lomba Basket Antar SMA Tingkat Kabupaten tahun 2018 atau Juara 3 Pencak Silat Ditingkat Kabupaten tahun 2018 ")

    # Documents Information
    nisn = models.PositiveIntegerField('NISN', unique=True, null=True, help_text="Isi berdasarkan NISN yang diberikan SMP Asal")
    nik = models.PositiveIntegerField('Nomor Induk Kependudukan (NIK)', unique=True, null=True, help_text="Bisa dicek di Kartu Keluarga")
    no_kk = models.PositiveIntegerField('Nomor Kartu Keluarga (KK)', null=True, help_text="Diisi Berdasarkan Kartu Keluarga")
    address_kk = models.TextField('Alamat Kartu Keluarga (KK)', null=True, help_text="Contoh: Jalan Radio Palasari")

    # Address
    city = models.CharField('Kota/Kabupaten', max_length=120, help_text="Contoh: Kabupaten Bandung")
    kecamatan = models.CharField(max_length=120, help_text="Contoh : Kecamatan Dayeuhkolot")
    kelurahan = models.CharField(max_length=120, help_text="Contoh : Desa Citeureup")
    dusun = models.CharField(max_length=120, help_text="Jika tidak tahu ada maka diisi dengan -")
    rt_rw = models.CharField('RT/RW', max_length=8, help_text="Contoh: 06/02")
    real_address = models.TextField('Alamat Sekarang', help_text="Contoh : Jalan Bojongsoang")
    resident = models.CharField('Tempat Tinggal', max_length=50, help_text="Contoh: Rumah Pribadi, Kost, Rumah Keluarga (Keluarga Besar).")
    transport = models.CharField('Alat Transportasi', max_length=50, help_text="Contoh: Jalan Kaki, Motor, Ojek Online, Sepeda, Mobil, Angkot.")

    # Previous School Information
    school_origin = models.CharField('Asal Sekolah', max_length=120, help_text="Isilah sesuai dengan asal sekolah Anda dan dituliskan seperti contoh berikut : SMP Telkom Bandung ")
    npsn_school_origin = models.PositiveIntegerField('Nomor NPSN Sekolah Asal', help_text="Bisa Cek <a href='https://referensi.data.kemdikbud.go.id/index11.php' target='_blank'><b>Disini</b></a>", null=True)

    # Medical Record
    medic_record = models.TextField('Riwayat Kesehatan', null=True, blank=True, help_text="Jika pernah mempunyai penyakit, silahkan ditulis disini")
    blood_type = models.CharField('Golongan Darah', choices=choices.BLOOD_TYPE, max_length=2)
    in_medicine = models.CharField('Dalam Pengobatan', max_length=120, null=True, blank=True)
    private_doctor = models.CharField('Nama Dokter Keluarga', max_length=120, null=True, blank=True, help_text="Jika kamu mempunyai dokter keluarga, silahkan input disini")
    phone_doctor = models.PositiveIntegerField('No Telepon Dokter', null=True, blank=True, help_text="Isi jika memiliki dokter keluarga dan atau dalam masa penyambuhan penyakit")

    def __str__(self):
        return f'{self.student} profile'

class ProfileParent(models.Model):
    """
    Creating abstract models, so this models (field) can be use multiple time (inheritance).
    https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
    """
    verified = models.BooleanField(default=False)
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name=f"Nama Lengkap", max_length=120)
    city_born = models.CharField('Kota/Kabupaten Kelahiran', max_length=120, help_text="Contoh pengisian tempat lahir: Kab bandung")
    date_born = models.DateField('Tanggal Lahir', null=True)
    nik = models.PositiveIntegerField('Nomor Induk Kependudukan (NIK)', null=True, help_text="Diisi berdasarkan Kartu Keluarga")
    education = models.CharField(f'Pendidikan Terakhir', max_length=4, choices=choices.EDUCATION_LEVEL)
    job = models.CharField(f'Pekerjaan', max_length=100, null=True, blank=True)
    salary = models.PositiveIntegerField(f'Penghasilan', null=True, blank=True, help_text="Diisi dengan angka")
    email = models.EmailField(f'Email', null=True, blank=True)
    phone = models.PositiveIntegerField(f'No. HP', null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        abstract = True

class FatherStudentProfile(ProfileParent):
    pass

class MotherStudentProfile(ProfileParent):
    pass

class StudentGuardianProfile(ProfileParent):
    pass

class MajorStudent(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    first_major = models.CharField('Pilihan Jurusan Pertama', choices=choices.MAJOR, max_length=4)
    second_major = models.CharField('Pilihan Jurusan Kedua', choices=choices.MAJOR, max_length=4)
    info = models.CharField('Info Primaseru (PPDB)', max_length=120, help_text="Tuliskan Darimana Kamu Mendapatkan Info Tentang Primaseru.")

    def __str__(self):
        return f'{self.student} - {self.first_major}'

