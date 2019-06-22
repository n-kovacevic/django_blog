$('#profile_dropdown').dropdown();

$('#hamburger').click(function () {
    $('#sidebar').sidebar('toggle');
});

$('.reply').click(function (e) {
    let comment_id = e.target.id.replace('reply-', '');
    if ($(e.target).hasClass("active")){
        $(e.target).removeClass("active");
    } else {
        $(e.target).addClass("active");
    }
    $('#reply-form-'+comment_id).slideToggle();
});

$('#tags select').addClass('search').dropdown({
    allowAdditions: true
});

