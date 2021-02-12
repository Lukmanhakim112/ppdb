$(document).ready(() => {
    let answer = [];
    $(".card .answer").each(function() {
        answer.push($(this).attr('id'));
    });

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
                navigator.sendBeacon(`/exam/${examPk}/times/up/`, data);
                let alert = `<div class="alert mt-2 alert-danger" role="alert">
                            Waktu Habis!
                            </div>`
                clearInterval(stopwatch);
                $(".container").prepend(alert);
            }
        }, 1000);
    }

    $.ajax({
        url: `/exam/${examPk}/timer/`,
        method: "GET",
        success: (response) => {
            startTimer(response.time, $("#timer"));
        },
    });

    $(window).on("unload", () => {
        let data = new FormData($("#timerExamForm").get(0));
        navigator.sendBeacon(`/exam/${examPk}/timer/`, data);
    });

});
