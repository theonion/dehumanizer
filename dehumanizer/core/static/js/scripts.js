(function( $ ) {
  $.fn.ansiAnimate = function() {
    if(this.find('.frame').length === 1) {
        return;
    }

    var duration = this.attr('data-duration');
    if(duration === undefined || duration == '0') {
        duration = 60;
    } else {
        duration = parseInt(duration);
    }

    this.find('.frame').hide();
    this.find('.frame').first().show();

    var ansi = this;

    setInterval(function(){
        var this_frame = ansi.find('.frame:visible');
        var next_frame = $(this_frame).next();
        if(next_frame.length === 0) {
            next_frame = ansi.find('.frame').first();
        }
        this_frame.hide();
        next_frame.show();
    }, duration);
  };
})( jQuery );


function getEmbed() {
    var ansi = $('.ansi');
    var width = 530;
    var height = Math.floor(((ansi.height() + 48) * width) / ansi.width());
    prompt("Copy and paste this HTML to embed:", '<iframe src="http://dehumanizer.theonion.com/embed?url=' + ansi.attr('data-url') + '" height="' + height + '" width="' + width + '" scrolling="no" />');
    return false;
}

function getShareURL(url) {
    prompt("COPY AND PASTE THIS TO ALL YOUR FRIENDS AND FAMILY", url);
    return false;
}

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
            $("#input").before(data.html);
            $('.ansi').ansiAnimate();
            window.history.pushState(url, "IMAGE DEHUMANIZATION COMPLETE", "/image?url=" + url);
            var history = localStorage.getItem('history');
            if (history !== null) {
                history = JSON.parse(history);
            } else {
                history = [];
            }
            history.push(url);
            localStorage['history'] = JSON.stringify(history);
        } else if (data.status == 'Pending') {
            setTimeout(function(){process_image(url);}, 2500);
        } else {
            $("#input").show();
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
    }, {'perms': 'user_photos'});
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

function show_images(graph_url){
    if(graph_url === undefined) {
        graph_url = '/me/photos/uploaded';
        logMessage('> RETRIEVING FACEBOOK IMAGES...');
    }
    $("#input").hide();
    $("#console form input").val('');
    var photo_root = $('.photos').first();
    if(photo_root.length === 0) {
        photo_root = $('<div class="photos"></div>');
    } else {
        photo_root.addClass('loading');
    }
    FB.api(graph_url, function(response) {
        if(photo_root.hasClass('loading')) {
            photo_root.empty();
        } else {
            logMessage('> PLEASE CHOOSE AN IMAGE:');
        }
        for (var i = 0; i < response.data.length; i++){
            var photo = response.data[i];
            var photo_element = $('<div class="photo" data-source="' + photo.source + '"></div>');
            photo_element.click(choose_image);
            photo_element.css("background-image", "url(" + photo.picture + ")");
            photo_root.append(photo_element);
        }
        if('paging' in response) {
            console.log('Has paging');
            if('previous' in response.paging) {
                console.log('Has prev');
                var previous_element = $('<div class="photo previous"><</div>');
                previous_element.click(function(){show_images(response.paging.previous);});
                photo_root.prepend(previous_element);
            }
            if('next' in response.paging) {
                console.log('Has next');
                var next_element = $('<div class="photo next">></div>');
                next_element.click(function(){show_images(response.paging.next);});
                photo_root.append(next_element);
            }
        }
        if(photo_root.hasClass('loading')) {
            photo_root.removeClass('loading');
        } else {
            photo_root.hide();
            $('#console').append(photo_root);
            photo_root.slideDown();
        }
    });
    
}

$(document).ready(function() {
    var form = $("#console form");
    var input = $("#console form input");

    var history;

    $('.ansi').ansiAnimate();

    $('.logo').click(function(){
        console.log("Home");
    });

    key('ctrl+c', function() {
        var command = $('input').val();
        logMessage('><span class="command">' + command + '^C</span>');
        $(input).val('');
    });

    form.submit(function(){
        var command = $(this).find('input').val();
        logMessage('><span class="command">' + command + '</span>');
        if(command === "") {
            return false;
        }
        if(command.toLowerCase() == "facebook") {
            facebook();
        } else if (command.toLowerCase() == 'clear') {
            $(input).val('');
            $('.message').remove();
            $('.ansi').remove();
        } else if (command.toLowerCase() == 'ls' || command.toLowerCase().indexOf('ls ') === 0 ) {
            logMessage("ERR: THIS IS SOME NEXT LEVEL SHIT FOR SURE, BUT IT'S NOT <b>THAT</b> NEXT LEVEL.");
            $(input).val('');
        } else if(command.toLowerCase() == 'history') {
            var history = localStorage.getItem('history');
            if (history !== null) {
                history = JSON.parse(history);
                for (var i = 0; i < history.length; i++) {
                    logMessage(i + '&nbsp;<a href="/image?url=' + history[i] + '">' + history[i] + '</a>');
                }
                $(input).val('');
            } else {
                logMessage("YOU HAVEN'T DEHUMANIZED ANYTHING.");
            }
        } else if (command.toLowerCase() == 'help' || command.toLowerCase().indexOf('help ') === 0) {
            $.get('/json/help.json', function(data) {
                for (var i = 0; i < data.message.length; i++) {
                    logMessage(data.message[i]);
                }
                $(input).val('');
            });
        } else if (command.toLowerCase() == 'man' || command.toLowerCase().indexOf('man ') === 0) {
            $.get('/json/man.json', function(data) {
                for (var i = 0; i < data.message.length; i++) {
                    logMessage(data.message[i]);
                }
                $(input).val('');
            });
        } else {
            if(test_url(command)) {
                $("#input").hide();
                process_image(command);
                $(input).val('');
                // Make call to start image processing.
            } else {
                $(input).val('');
                logMessage("ERR: INVALID URL. TRY AGAIN, PUNY HUMAN. FOR ASSISTANCE, TYPE \"HELP\"");
            }
        }
        return false;
    });
});