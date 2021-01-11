$(document).ready(() => {
    let answer = [];
    $(".card .answer").each(function() {
        answer.push($(this).attr('id'));
    });

    for (let a = 0; a < answer.length; a++) {
        let answerPk = answer[a].split('-')[1];
        $.ajax({
            url: `/exam/answer/${answerPk}/`,
            method: "GET",
            async: true,
            beforeSend: () => {
                $(`#${answer[a]}`).html(`<div class="m-auto"><span class="spinner-border spinner-border-lg text-danger" role="status" aria-hidden="true"></span></div>`)
            },
            success: (data) => {
                $(`#${answer[a]}`).empty();
                for (const {answer_text: answer_text} of data.answer) {
                    $(`#${answer[a]}`).append(`<li class="list-group-item py-1">${answer_text}</li>`);
                }
            },
        });
    }

    $("#add-question").one('click', () => {
        $.ajax({
            url: `/exam/question/add/`,
            method: "GET",
            async: true,
            beforeSend: () => {
                $(`#addQuestion .modal-body`).html(`<div class="m-auto"><span class="spinner-border spinner-border-lg text-danger" role="status" aria-hidden="true"></span></div>`)
            },
            success: (data) => {
                $(`#addQuestion .modal-body`).empty().html(data)
            },
        });
    });

});
