$(document).ready(() => {
    let answer = [];
    $(".card .answer").each(function() {
        answer.push($(this).attr('id'));
    });

    document.addEventListener("contextmenu", function(evt){
        evt.preventDefault();
    }, false);

    function startTimer(duration, display) {
        var timer = duration, minutes, seconds;
        var stopwatch = setInterval(function () {
            minutes = parseInt(timer / 60, 10)
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.text(minutes + ":" + seconds);

            $("#id_timerExam").val(timer)

            if (--timer < 0) {

                let data = new FormData($("#timerExamForm").get(0));
                navigator.sendBeacon(`/exam/${answer[0].split('-')[0]}/times/up/`, data);
                // window.location.replace(`/exam/${answer[0].split('-')[0]}/taken/submit/`);
                let alert = `<div class="alert alert-danger mt-2" role="alert">
                            Waktu Habis!
                            </div>`
                clearInterval(stopwatch);
                $(".container").prepend(alert);
            }
        }, 1000);
    }

    $.ajax({
        url: `/exam/${answer[0].split('-')[0]}/timer/`,
        method: "GET",
        success: (response) => {
            startTimer(response.time, $("#timer"));
        },
    });

    $(window).on("unload", () => {
        let examPk = answer[0].split('-')[0];
        let data = new FormData($("#timerExamForm").get(0));
        navigator.sendBeacon(`/exam/${examPk}/timer/`, data);
    });

    for (let a = 0; a < answer.length; a++) {
        let examPk = answer[a].split('-')[0];
        let answerPk = answer[a].split('-')[2];
        $.ajax({
            url: `/exam/${examPk}/taken/${answerPk}/`,
            method: "GET",
            async: true,
            beforeSend: () => {
                $(`#${answer[a]}`).html(`<div class="m-auto"><span class="spinner-border spinner-border-lg text-danger" role="status" aria-hidden="true"></span></div>`)
            },
            success: (data) => {
                $(`#${answer[a]}`).html(data);

                $("#answer-form").change(() => {
                    $.ajax({
                        url: `/exam/${examPk}/taken/${answerPk}/`,
                        type: "POST",
                        data: $("#answer-form").serialize(),
                        dataType: 'json',
                        success: () => {
                            console.log('Success');
                        },
                    });
                    return false;
                });
            },
        });
    }


});
