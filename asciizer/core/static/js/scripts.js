function logMessage(text) {
    var line = '<div class="row">' + text + '</div>';
    $("#input").before(line);
}

function test_url(url){
    var url_regex = new RegExp(/[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi);
    return url.match(url_regex);
}

function process_image(url) {
    $.get({
        url: "/process.json",
        data: {url: command},
        success: function(data) {
            console.log(data);
        }
    });
}

$(document).ready(function() {
    var form = $("#console form");
    var input = $("#console form input");

    input.focus();

    form.submit(function(){
        var command = $(this).find('input').val();
        logMessage('><span class="command">' + command + '</span>');
        $(input).val('');
        if(command == "facebook") {
            // Load facebook iframe, etc.
        } else {
            if(test_url(command)) {
                input.unfocus();
                logMessage('LOADING... ');
                $("#input").hide();
                $.get({
                    url: "/process.json",
                    data: {url: command}
                });
                // Make call to start image processing.
            } else {
                logMessage("ERR: INVALID URL. TRY AGAIN, PUNY HUMAN.");
            }
        }

        return false;
    });
});