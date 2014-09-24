(function($){

    $(document).ready(function(){

        var msg_id = 0,
            $window = $(window),
            $cards_top = $('.cards.top:first'),
            $cards_bottom = $('.cards.bottom:first');

        // Cards Overflow / Scroll

        function update_top_cards_scroll_indicators($cards){
            console.log(msg_id++)
        }

        $('.cards').scroll(function(){
            update_top_cards_scroll_indicators($(this))
        })


        function resize_top_cards() {
            var new_h = $window.height() - $cards_bottom.height() - 20;
            $cards_top.height(new_h);
            update_top_cards_scroll_indicators($cards_top)
        }

        $(window).resize(resize_top_cards)



        // Card Manipulation
        function hide_card($card){
            $card.css({height: 0, opacity: 0})
        }

        function open_card($card){
            var $inner = $card.children(".inner.active:first")
            $card.animate({height: $inner.outerHeight(true)},
                          {step: resize_top_cards,
                           complete: function(){
                               $card.css("height", "auto")
                               $card.animate({opacity: 1})
                           }})
        }

        function close_card($card){
            $card.animate({opacity: 0}, function(){
                $card.animate({height: 0},
                              {step: resize_top_cards})
            })
        }



        $(".card.closed").each(function(){
            hide_card($(this))
            open_card($(this))
        })

        setTimeout(function(){
            $(".card.closer").each(function(){
                close_card($(this))
            })
                }, 1000)




        console.debug($(document).width())
    })

})(jQuery);
