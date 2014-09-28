(function(){

    var cards = {};

    window.card_init_fn.media = function(card_id, $card){
        var $elems = {
                art:             $card.find('.art:first'),
                btn_toggle:      $card.find('.top .btn:first'),
                btn_toggle_icon: $card.find('.top .btn .control div:first'),
                info_title:      $card.find('.info .title:first'),
                info_artist:     $card.find('.info .artist:first'),
                info_album:      $card.find('.info .album:first'),
                device:          $card.find('.device:first'),
                btn_next:        $card.find('.btn.next'),
                btn_stop:        $card.find('.btn.stop'),
                btn_prev:        $card.find('.btn.prev'),
            },
            card_fn = {
                set_info: function(data){
                    $elems.info_title.text(data.title);
                    $elems.info_artist.text(data.artist);
                    $elems.info_album.text(data.album);
                },
                set_type: function(type){
                    $elems.device.text(type)
                },
                set_state: function(data){

                    if(data.toggle_enabled)
                        $elems.btn_toggle.removeClass('disabled')
                    else
                        $elems.btn_toggle.addClass('disabled')

                    if(data.state == 'playing')
                        $elems.btn_toggle_icon.removeClass('play').addClass('pause')
                    else
                        $elems.btn_toggle_icon.addClass('play').removeClass('pause')

                    if(data.stop_enabled)
                        $elems.btn_stop.removeClass('disabled')
                    else
                        $elems.btn_stop.addClass('disabled')

                    if(data.next_enabled)
                        $elems.btn_next.removeClass('disabled')
                    else
                        $elems.btn_next.addClass('disabled')

                    if(data.prev_enabled)
                        $elems.btn_prev.removeClass('disabled')
                    else
                        $elems.btn_prev.addClass('disabled')

                }
            };
        cards[card_id] = card_fn;

        // Setup Listeners
        $elems.btn_toggle.click(function(){
            send_to_plugin('media',
                           {
                               card_id: card_id,
                               action: 'toggle'
                           })
        });

        $elems.btn_next.click(function(){
            send_to_plugin('media',
                           {
                               card_id: card_id,
                               action: 'next'
                           })
        });

        $elems.btn_stop.click(function(){
            send_to_plugin('media',
                           {
                               card_id: card_id,
                               action: 'stop'
                           })
        });

        $elems.btn_prev.click(function(){
            send_to_plugin('media',
                           {
                               card_id: card_id,
                               action: 'prev'
                           })
        });
    }

    window.card_send_fn.media = function(card_id, $card, object){
        cards[card_id][object.fn](object.data)
    }

})()
