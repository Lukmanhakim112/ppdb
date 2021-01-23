$(document).ready(() => {
    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+)');
        var replacement = prefix + '-' + ndx;
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }
    function cloneMore(selector, prefix) {
        var newElement = $(selector).clone(true);
        var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
        newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
            var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });
        newElement.find('td').each(function() {
            var name = $(this).attr('id').replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'id': id}).val('').removeAttr('checked');
        });
        total++;
        $('#id_' + prefix + '-TOTAL_FORMS').val(total);
        $(selector).after(newElement);
        return false;
    }

    function deleteForm(prefix) {
        var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        $(".formset tbody tr:last").remove();
        if (total > 1){
            var forms = $('.formset tbody tr');
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            for (var i=0, formCount=forms.length; i<formCount; i++) {
                $(forms.get(i)).find('td').each(function() {
                    updateElementIndex(this, prefix, i);
                });
            }
        }
        return false;
    }

    $(document).on("click", "#add-answer", (e) => {
        e.preventDefault();
        cloneMore(".formset tbody tr:last", 'form');
        return false;
    });

    $(document).on("click", "#remove-answer", (e) => {
        e.preventDefault();
        deleteForm('form');
        return false;
    });

    let formQuestion = $('#form-container');
    $("#id_question_text").focus(() => {
        $('.alert').alert('close')
    });

    $(formQuestion).submit(() => {
        let filesData = new FormData($(formQuestion).get(0));
        $.ajax({
            url: endPoint,
            type: "POST",
            data: filesData,
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            success: (response) => {
                let alertSuccess = `<div class="alert alert-success alert-dismissible fade show" role="alert">Berhasil Menambahkan Pertanyaan! \
                                <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">\
                                &times;</span></button></div>`;
                $(formQuestion)[0].reset();
                $(formQuestion).prepend(alertSuccess);
                $("#question-count").html(response.question_count);
            },
            error: (response) => {
                let alertDanger = `<div class="alert alert-danger alert-dismissible fade show" role="alert">Data Tidak Valid, Silahkan Cek Kembali... \
                                <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">\
                                &times;</span></button></div>`;
                $(formQuestion).empty()
                               .html(response.responseJSON.form_q)
                               .append(response.responseJSON.form_a)
                               .prepend(alertDanger);
            },
        });
        return false;
    });



});
