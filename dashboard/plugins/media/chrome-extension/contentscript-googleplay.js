(function($){

    MEDIA_TYPE = 'google_play';

    console.log("Inserted contentscript");

    var update_timeout = 0,
        $player = $('#player'),
        now_playing = {
            title: null,
            artist: null,
            album: null
        },
        state = {
            state: 'paused',
            toggle_enabled: false,
            stop_enabled: false,
            next_enabled: false,
            prev_enabled: false
        },
        album_art_url = null;

    // Connect to background script
    var port = chrome.runtime.connect();

    port.onMessage.addListener(function(msg){
        var c = control()
        if(msg.action in c)
            c[msg.action]()
    })

    port.postMessage({action: "new_tab", media_type: MEDIA_TYPE});

    // Listen for changes in DOM
    $player.bind('DOMSubtreeModified', function(){
        clearTimeout(update_timeout)
        update_timeout = setTimeout(update, 50)
    })
    update_timeout = setTimeout(update, 50);

    function update(){
        update_info();
        update_state();
    }

    function update_info(){

        console.log("update_info")

        var $player_song_info = $('#playerSongInfo'),
            title = null,
            artist = null,
            album = null,
            changed = false;

        if($player_song_info.children().length == 0){
             title = '';
             artist = '';
             album = '';
        } else {
            var $title = $player_song_info.find('#currently-playing-title'),
                $artist = $player_song_info.find('#player-artist'),
                $album = $player_song_info.find('.player-album:first');

            if($title)
                title = $title.text();

            if($artist)
                artist = $artist.text();

            if($album)
                album = $album.text();
        }

        if(title != now_playing.title){
            now_playing.title = title
            changed = true
        }

        if(artist != now_playing.artist){
            now_playing.artist = artist
            changed = true
        }

        if(album != now_playing.album){
            now_playing.album = album
            changed = true
        }

        if(changed)
            port.postMessage({key: "info", value: now_playing});

        // Album Art
        var new_album_art_url = $('#playerBarArt').attr('src');

        if(album_art_url != new_album_art_url)
            convertImgToBase64(new_album_art_url, function(base64){
                port.postMessage({key: "album_art", value: base64})
            }, "image/png")

        album_art_url = new_album_art_url
    }

    function control(){
        // Create closure (on demand) for functions requiring control access
        // (created on demand and disposed of as elems change over the lifetime
        // of page
        var changed = false,
            $buttons = $('.material-player-middle:first'),
            $play_pause = $buttons.children('[data-id=play-pause]:first'),
            $next = $buttons.children('[data-id=forward]:first'),
            $prev = $buttons.children('[data-id=rewind]:first');

        return {
            update_state: function(){
                var  new_state = {
                    state: $play_pause.hasClass('playing') ? 'playing' : 'paused',
                    toggle_enabled:
                        $play_pause.length > 0 && $play_pause.attr('disabled') === undefined,
                    stop_enabled: false,
                    next_enabled:
                        $next.length > 0 && $next.attr('disabled') === undefined,
                    prev_enabled:
                        $prev.length > 0 && $prev.attr('disabled') === undefined
                }

                for (var key in state)
                    if(state.hasOwnProperty(key) && state[key] != new_state[key]){
                        changed = true;
                        break;
                    }

                state = new_state

                if(changed)
                    send_state()
            },
            toggle: function(){
                $play_pause.click()
            },
            next: function(){
                $next.click()
            },
            prev: function(){
                $prev.click()
            }
        }
    }

    function update_state(){
        control().update_state()
    }

    function send_state(){
        console.debug("send_state")
        port.postMessage({key: "play_state", value: state});
    }

    function convertImgToBase64(url, callback, outputFormat){
        var canvas = document.createElement('canvas'),
        ctx = canvas.getContext('2d'),
        img = new Image;
        img.crossOrigin = 'Anonymous';
        img.onload = function(){
            var dataURL;
            canvas.height = Math.min(img.height, 62);
            canvas.width = Math.min(img.width, 62);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            dataURL = canvas.toDataURL(outputFormat);
            callback.call(this, dataURL);
            canvas = null;
        };
        img.src = url;
}

})(jQuery)
