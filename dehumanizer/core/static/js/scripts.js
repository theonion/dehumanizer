function logMessage(text, css_class) {
    if (css_class === undefined) {
        css_class = 'row';
    }
    var line = '<div class="' + css_class + '">' + text + '</div>';
    $("#input").before(line);
}

function test_url(url){
    var url_regex = new RegExp(/[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi);
    return url.match(url_regex);
}

function process_image(url){
    $.get("/image.json", {url: url}, function(data){
        for (var i = 0; i < data.message.length; i++) {
            logMessage(data.message[i]);
        }
        if(data.status == 'Completed') {
            logMessage(data.ansi, 'ansi');
            window.history.pushState(data.url, "IMAGE DEHUMANIZATION COMPLETE", data.url);
            $("#input").show();
        } else {
            setTimeout(function(){process_image(url);}, 1000);
        }
    });
}

$(document).ready(function() {
    var form = $("#console form");
    var input = $("#console form input");

    input.focus();
    setInterval(function(){
        if($("#input").is(":visible")) {
            input.focus();
        }
    }, 1000);

    form.submit(function(){
        var command = $(this).find('input').val();
        logMessage('><span class="command">' + command + '</span>');
        if(command == "facebook") {
            // Load facebook iframe, etc.
        } else {
            if(test_url(command)) {
                logMessage('> LOADING... ');
                $("#input").hide();
                process_image(command);
                $(input).val('');
                // Make call to start image processing.
            } else {
                logMessage("ERR: INVALID URL. TRY AGAIN, PUNY HUMAN.");
            }
        }
        return false;
    });
});