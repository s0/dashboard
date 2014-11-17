(function(){

    var cards = {};

    window.card_init_fn.bluetooth_device = function(card_id, $card){
        var $elems = {
                status_icon: $card.find('.top .btn .control div:first'),
                info_name:   $card.find('.info .name:first'),
                info_status: $card.find('.info .status:first'),
            },
            card_fn = {
                set_info: function(data){
                    $elems.info_name.text(data.name);

                    if(data.status == 'connected'){
                        $elems.status_icon.addClass('connected')
                        $elems.info_status.addClass('connected')
                    } else {
                        $elems.status_icon.removeClass('connected')
                        $elems.info_status.removeClass('connected')
                    }
                    $elems.info_status.text(data.status)
                }
            };
        cards[card_id] = card_fn;
    }

    window.card_send_fn.bluetooth_device = function(card_id, $card, object){
        cards[card_id][object.fn](object.data)
    }

})()
