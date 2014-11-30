(function(){

    var cards = {};

    window.card_init_fn.bluetooth_device = function(card_id, $card){
        var $elems = {
                status_icon: $card.find('.top .btn .control div:first'),
                info_name:   $card.find('.info .name:first'),
                info_status: $card.find('.info .status:first'),
            },
            state_fn = {
                info: function(data){
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
        cards[card_id] = state_fn;
    }

    window.card_state_fn.bluetooth_device = function(card_id, $card, key, value){
        cards[card_id][key](value)
    }

})()
