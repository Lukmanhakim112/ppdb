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
                console.log(data.answer)
                for (const {answer_text: answer_text, is_right: is_right, answer_image: answer_image} of data.answer) {
                    if (is_right && answer_image) {
                        $(`#${answer[a]}`).append(`<li class="list-group-item py-1 list-group-item-success">${answer_text} <br/> \
                                                    <img src='/media/${answer_image}' class="img-fluid w-25" alt="answer image" /></li>`);
                    } else if (is_right) {
                        $(`#${answer[a]}`).append(`<li class="list-group-item py-1 list-group-item-success">${answer_text}</li>`);
                    } else if (answer_image) {
                         $(`#${answer[a]}`).append(`<li class="list-group-item py-1 list-group-item">${answer_text} <br/> \
                                                    <img src='/media/${answer_image}' class="img-fluid w-25" alt="answer image" /></li>`);
                    } else {
                        $(`#${answer[a]}`).append(`<li class="list-group-item py-1">${answer_text}</li>`);
                    }
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
