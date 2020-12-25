function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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

    $("#profile-form").submit(() => {
        $.ajax({
            url: profileStudent.url,
            type: "POST",
            data: $(this).serialize(),
            success: () => {
                if (!(data['success'])) {
                    $("#profile-form").replaceWith(data['form_s']);
                }
                else {
                    $("#profile-form").find('.success-message').show();
                }
            },
            error: () => {
                $("#profile-form").find('.error-message').show()
            },
        });
        return false;
    });

    $("#father-form").submit(() => {
        $.ajax({
            url: profileFather.url,
            type: "POST",
            data: $("#father-form").serialize(),
            dataType: 'json',
            success: () => {
                let alertSuccess = '<div class="alert alert-success" role="alert">Berhasil Simpan Data Ayah</div>'
                $("#father-form").prepend(alertSuccess)
            },
            error: (response) => {
                $("#father-form").replaceWith(response.responseJSON.form_s);
            },
        });
        return false;
    });

});
