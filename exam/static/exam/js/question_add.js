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
        if (total > 1){
            var forms = $('.formset tbody tr');
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            for (let i=0, formCount=forms.length; i<formCount; i++) {
                $(forms.get(i)).find(':input').each(function() {
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
});
