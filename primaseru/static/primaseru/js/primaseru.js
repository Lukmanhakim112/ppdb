$(document).ready( () => {
    let textbox = [
        $('#id_address_kk'),
        $('#id_real_address'),
        $('#id_medic_record')
    ];
    for (let x = 0; x < textbox.length; x++) {
        textbox[x].autoresize(1, 5);
    }
    $("#photo-profile-form").change(() => {
        document.forms["photo-profile-form"].submit();
    });

    // TODO Add more name to :
    // full name (done), city_born, education, salary, email, phone
    let tabs = $(".tab-profile");
    for (let i = 0; i < tabs.length; i++) {
        $(tabs[i]).click(() => {
            let text = tabs[i].innerHTML.split(" ")[1]; // Get name of the parent from side bar
            let full_name = `Nama Lengkap ${text} <span class="asteriskField">*</span>`;
            setTimeout(() => {
                $("#div_id_full_name label").html(full_name);
            }, 200);
        });
    }

    let formList = [
        [$("#profile-form"), "Calon Siswa", "profile"],
        [$("#father-form"), "Ayah Calon Siswa", "father"],
        [$("#mother-form"), "Ibu Calon Siswa", "mother"],
        [$("#guardian-form"), "Wali Calon Siswa", "guardian"]
    ];
    for (let i = 0; i < formList.length; i++){
        $(formList[i][0]).submit(() => {
            $.ajax({
                url: `/profile/save/${formList[i][2]}/`,
                type: "POST",
                data: $(formList[i][0]).serialize(),
                dataType: 'json',
                success: (response) => {
                    $(formList[i][0]).empty().html(response.form_s);
                    let alertSuccess = `<div class="alert alert-success alert-dismissible fade show" role="alert">Berhasil Menyimpan Data ${formList[i][1]} \
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">\
                                    &times;</span></button></div>`;
                    $(formList[i][0]).prepend(alertSuccess);
                },
                error: (response) => {
                    $(formList[i][0]).empty().html(response.responseJSON.form_s);
                },
            });
            return false;
        });
    }

    let selectedFirst = $("#id_first_major").val();
    if (!!(selectedFirst)) {
        $("#id_first_major").prop('disabled', true);
    }
    let selectedSecond = $("#id_second_major").val();
    if (!!(selectedSecond)) {
        $("#id_second_major").prop('disabled', true);
    }

    let majorForm = $("#major-form");
    $("#major-form").submit((e) => {
        if ($("#id_first_major").is(":disabled") && $("#id_second_major").is(":disabled")) {
            let alertDanger = `<div class="alert alert-danger alert-dismissible fade show" role="alert">Jurusan Sudah Dipilih, Tidak Bisa Diubah.... \
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">\
                                    &times;</span></button></div>`;
            $(majorForm).prepend(alertDanger);
            e.preventDefault();
            e.stopPropagation();
        } else {
            $.ajax({
                url: "/profile/save/major/",
                type: "POST",
                data: $(majorForm).serialize(),
                dataType: 'json',
                beforeSend: () => {
                    let alertDanger = `<div class="alert alert-danger alert-dismissible fade show" role="alert">Kedua juruan pilihan tidak boleh sama! \
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">\
                                    &times;</span></button></div>`;
                    if (selectedFirst == selectedSecond) {
                        $(majorForm).prepend(alertDanger);
                        return false;
                    }
                },
                success: (response) => {
                    $(majorForm).empty().html(response.form_s);
                    console.log(response.form_s);
                    let alertSuccess = `<div class="alert alert-success alert-dismissible fade show" role="alert">Berhasil Menyimpan Jurusan Pilihan \
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">\
                                    &times;</span></button></div>`;
                    $(majorForm).prepend(alertSuccess);
                },
                error: () => {
                    let alertDanger = `<div class="alert alert-danger alert-dismissible fade show" role="alert">Data Tidak Valid, Silahkan Cek Kembali... \
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">\
                                    &times;</span></button></div>`;
                    $(majorForm).prepend(alertDanger);
                },
            });
            return false;
        }
    });

});
