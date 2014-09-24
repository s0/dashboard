(function($){

    $(document).ready(function(){


        // Card Manipulation
        function hide_card($card){
            $card.css({height: 0, opacity: 0})
        }

        function open_card($card){
            var $inner = $card.children(".inner.active:first")
            $card.animate({height: $inner.outerHeight(true)}, function(){
                $card.css("height", "auto")
                $card.animate({opacity: 1})
            })
        }



        $(".card.closed").each(function(){
            hide_card($(this))
            open_card($(this))
        })




        console.debug($(document).width())
    })

})(jQuery);
