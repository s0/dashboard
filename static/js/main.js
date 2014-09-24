(function($){

    $(document).ready(function(){

        var msg_id = 0,
            $window = $(window),
            $cards_top = $('.cards.top:first'),
            $cards_top_contents = $cards_top.children('.contents:first'),
            $cards_bottom = $('.cards.bottom:first'),
            $cards_bottom_contents = $cards_bottom.children('.contents:first')

        // Setup global function

        window.send_to_plugin = function(plugin, obj){
            i = msg_id++;
            document.title = i + ":::" + plugin + ":::" + JSON.stringify(obj)
        }

        // Cards Overflow / Scroll

        function update_top_cards_scroll_indicators(){
            var $contents         = $(this),
                height            = $contents.height(),
                scrollHeight      = $contents.get(0).scrollHeight,
                scrollTop         = $contents.scrollTop(),
                $top_indicator    = $contents.parent()
                                    .children('.overflow-indicator.top')
                                    .first(),
                $bottom_indicator = $contents.parent()
                                    .children('.overflow-indicator.bottom')
                                    .first();

            if(scrollTop == 0){
                $top_indicator.hide();
            } else {
                $top_indicator.show();
            }

            if(height >= scrollHeight - scrollTop){
                $bottom_indicator.hide();
            } else {
                $bottom_indicator.show();
            }

        }

        $('.cards .contents').scroll(update_top_cards_scroll_indicators)

        function resize_top_cards() {
            var new_h = $window.height() - $cards_bottom.height() - 30;
            $cards_top.height(new_h);

            $('.cards .contents').each(update_top_cards_scroll_indicators)
        }

        $window.resize(function(){
            $cards_bottom_contents.css('max-height', $window.height() / 2)
            resize_top_cards()
        })

         $window.trigger('resize')


        // Card Manipulation
        function hide_card($card){
            $card.css({height: 0, opacity: 0})
        }

        function open_card($card){
            var $inner = $card.children(".inner.active:first")
            $card.animate({height: $inner.outerHeight(true)},
                          {step: resize_top_cards,
                           complete: function(){
                               send_to_plugin("media", {a: 123, b: [2,3,4]})
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
