$(() => {
    $(document).scroll(() => {
        let nav = $(".navbar");
        nav.toggleClass('scrolled', $(this).scrollTop() > nav.height());
    });
});
