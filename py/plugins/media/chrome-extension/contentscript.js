(function($){

    var update_timeout = 0,
        $player = $('#player'),
        $player_song_info = $('#playerSongInfo'),
        $buttons = $('.player-middle:first'),
        $button_repeat = $buttons.children("[data-id=repeat]:first"),
        now_playing = {
            title: null,
            artist: null,
            album: null
        };

    $player.bind('DOMSubtreeModified', function(){
        clearTimeout(update_timeout)
        update_timeout = setTimeout(update_info, 50)
    })

    function update_info(){

        var title = null,
            artist = null,
            album = null,
            changed = false;

        if($player_song_info.children().length == 0){
             title = null;
             artist = null;
             album = null;
        } else {
            var $title = $player_song_info.find('#playerSongTitle'),
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
            info_changed()

        //console.debug($player_song_info)
    }

    function info_changed(){
        console.debug("changed")
        console.debug(now_playing)
    }

})(jQuery)
