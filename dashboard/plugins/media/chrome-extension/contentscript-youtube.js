(function($){

    MEDIA_TYPE = 'youtube';

    console.log("Inserted contentscript");

    var update_timeout = 0,
        $player = $('#player-api'),
        $title = $('#eow-title'),
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
    port.postMessage({key: "album_art", value: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD4AAAAsCAYAAAA93wvUAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3wIYFic3ugLg4gAABSpJREFUaN7lmstvG1UUxn93fMcPkpSUgvIgcYWqRpRE5bEpgTwKYoMQXYJEu2DBBgkhlvwJqDskxBIkQJUqQYESuaoKNE1Lk9CK1mlaOU4lGjtPQtrEj9iOnTksZkwc2kJaPAnYn3Q0C3vu3O8+zjn33E8BxDvaaB2NAjDV8TiCACgUNcBuoBl4CKgHtimoA2qBGiAAPAD4AZ9jXsdMQDvmcZ6GY6WwHFt1LA8UnGceyAErQNaxjGNpICWQBBLAInATmAauI6QASwGPjo5RylXH2tdIAwgSAF4F3kPoRHEbhP8B7E5eAD4S+BJYBmgdjRJrb1ujFW9vA0UL8Cmol6goyHngEMKN1qtRZzkDsY42EBqA0yj2UIkQJoBuFPHgaNTeayKYAh8AexBnmVSawU6BD0XwAqgbT7ThOLCoUlQ0xB6AZ4BLWuzl/qZa+6GyycNbwDvq1z27DWAERTvVAGESeEyLHZvbEaoFLUCLFuFJFNUF4WktsFNJtfFmpxaRZlx052JZYFkojwf+I2FDRJq0QINb7lwsC7OlBTya/GQcCgWUYWz5AAg0aISHxaV+WLkctS+/gr+zk0Tfd2QuXmQ1NgGrxRWwZcwf0QLb3fLogsLK5ah5tpOarm6W+k+T+PoYuXAYKx4HpewB2Hxs1yLUuzXy4mwhyeUwtKZ+/wsEurpJhEKkQn0Url5ldXLSJr+ZAyDUa0Hq3PTqf23apzU7DhzA39ND8kSIzKlTrF67hjU9Baa5KStAoE6LEHBvxu98eDeAuvp6vK+9znLvfpInQuTPnqUwOoo1NwteH8pjuJmzB7SAz709/vdFC5/Hg9nYiPnGQTLdPSx/f4r8+UEKV0awFhbA57OjQPn75dWAayt9I1HSMAxqAwF0MIh58BCZ555n5cwZVoYGyYfDWIkk+H2o8oZAQ4ur+/uf5nwNfr8fU2v0rl1km5vR+/aRHxwkf/EC+ZErWMtplCrf7GvLReYi93bU9WhNbV0dpmli7t1LtqkJSaXIjYwgIsUiaHmIu+w97ws+n4/lkydJ9vWxcvkykl4GVd697upSR+6dfHJggKVQiPTQMNnr406M12Uv7Wpx8SAuReYb+ER6+GduHf+W1PAw2UjEzuq8XufV8vdRi4vMZQONL4fD3PzqGKmhIbKRCGJZKNO74ahwv13TYt9QuJar323Cs2NRFo4eJTk4SCYSQfJ5lNbg8WxGMSinRewbBldOZ3K7m8tNxPj9yBGSZ8+RGRvDymZtwtq0/7U5RZGMxr53ci+eGQpPbS2F+Xl+++xzEqf7yYxHsVJplNYo09yK01lSi8iia80rg/zCTaYOHyZ57icy4+OsJpK2p9bameEtqXstaoFbrjXvNVn84UcoFFhNJu3KS5Hw1uKWFmHevfYVhcUlJzv2/LuspryY1wJzrn7iv3kvNadFZIbqw4wWuFGFxCc0wkgVEv9Fi60bGQU6qoR0XMFkMVf/poqIHxew1LnmIMAu4HqVEH8KCBtd0zFEmBDhk2LFpILtmAjXuqZjdgVGbE3Z+0AnVKj4ByaAd7F1cxgDTUF6ZmIgzCO8iHCiAsU/wwg9CFM9MzEGmoL2VcJAY5Ce2RgA/Y0tHmXr3N4GeoFtzutqXS66kXx188p3d/v9EvAx8EXvbHyllOu6zp1pbKV3Nr7uzf6G1lbH+QWBHcCD2JLOGmwpZ4D1ck4ftpTzTrLOUnln6V1RqZyzwJqcc6XkmcWWdhYlnekSSwJLji0AM0Bk/1w8UcoN+JPfH5+8DaD4j7bGAAAAAElFTkSuQmCC"})
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

        var $video_title = $('#eow-title'),
            title = null,
            artist = null,
            album = null,
            changed = false;

        if($video_title.length == 0){
            title = '';
            artist = '';
            album = '';
        } else {
            var titleText = $video_title.text().trim(),
                split = titleText.split("-");

            if(split.length == 2){
                title = split[1].trim();
                artist = split[0].trim();
            } else {
                title = titleText;
                artist = '';
            }
            album = '';
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
    }

    function control(){
        // Create closure (on demand) for functions requiring control access
        // (created on demand and disposed of as elems change over the lifetime
        // of page
        var changed = false,
            $buttons = $('#player-api .ytp-chrome-controls:first'),
            $play_pause = $buttons.children('.ytp-play-button'),
            $next = $('.ytp-next-button'),
            $prev = $('.ytp-prev-button');

            console.debug($play_pause, $next, $prev);

        return {
            update_state: function(){
                var  new_state = {
                    state: $play_pause.attr('aria-label') === 'Play' ? 'paused' : 'playing',
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
                update_timeout = setTimeout(update, 50);
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
        port.postMessage({key: "play_state", value: state});
    }

    function convertImgToBase64(url, callback, outputFormat){
        var canvas = document.createElement('canvas'),
        ctx = canvas.getContext('2d'),
        img = new Image;
        img.crossOrigin = 'Anonymous';
        img.onload = function(){
            var dataURL;
            canvas.width = Math.min(img.width, 62);
            canvas.height = canvas.width / img.width * img.height
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            dataURL = canvas.toDataURL(outputFormat);
            callback.call(this, dataURL);
            canvas = null;
        };
        img.src = url;

    }

})(jQuery)
