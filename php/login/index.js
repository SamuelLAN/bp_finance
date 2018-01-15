$('#confirm').bind('click', function() {
    var username = $('#username').val(),
        password = $('#password').val();

    if(username && password) {
        $.post('authentication.php', {username: username, password: password}, function(data) {
            if(data) {
                location.href = '../predict/index.php';
            } else {
                $('#notice').css('display', 'block');
                $('#mask').css('display', 'block');
            }
        });
    }
});

$('#cancel').bind('click', function() {
    $('#notice').css('display', 'none');
    $('#mask').css('display', 'none');
});