function logMessage(text, css_class) {
    if (css_class === undefined) {
        css_class = 'row message';
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

function login(callback) {
    logMessage("> CONNECTING TO FACEBOOK...");
    FB.login(function(response) {
        if (response.authResponse) {
            FB.api('/me', function(response) {
                logMessage('> WELCOME ' + response.name.toUpperCase());
                if(callback !== undefined) {
                    callback();
                }
            });
        } else {
            logMessage("> FACEBOOK LOGIN CANCELED");
        }
    });
}

function facebook() {
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            show_images();
        } else if (response.status === 'not_authorized') {
            login(show_images);
        } else {
            login(show_images);
        }
    });
}

function choose_image(){
    $('.photos').slideUp(function(){
        $(this).remove();
    });
    logMessage("> PROCESSING FACEBOOK IMAGE...");
    process_image($(this).data().source);
}

function show_images(){
    logMessage('> RETRIEVING FACEBOOK IMAGES...');
    $("#input").hide();
    $("#console form input").val('');
    var photo_root = $('<div class="photos"></div>');
    photo_root.hide();
    FB.api('/me/photos/uploaded', function(response) {
        logMessage('> PLEASE CHOOSE AN IMAGE:');
        for (var i = 0; i < response.data.length; i++){
            var photo = response.data[i];
            var photo_element = $('<div class="photo" data-source="' + photo.source + '"></div>');
            photo_element.click(choose_image);
            photo_element.css("background-image", "url(" + photo.picture + ")");
            photo_root.append(photo_element);
        }
        $('#console').append(photo_root);
        photo_root.slideDown();
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
        if(command.toLowerCase() == "facebook") {
            facebook();
        } else if (command.toLowerCase() == 'clear') {
            $(input).val('');
            $('.message').remove();
            $('.ansi').remove();
        } else if (command.toLowerCase().indexOf('ls') != -1) {
            logMessage("&nbsp;&nbsp;This is some next level shit, for sure, but it's not THAT next level.");
            $(input).val('');
        } else {
            if(test_url(command)) {
                logMessage('> LOADING... ');
                $("#input").hide();
                process_image(command);
                $(input).val('');
                // Make call to start image processing.
            } else {
                $(input).val('');
                logMessage("ERR: INVALID URL. TRY AGAIN, PUNY HUMAN.");
            }
        }
        return false;
    });
});