// Setup global properties
window.card_init_fn = {};
window.card_send_fn = {};

(function($){

    $(document).ready(function(){

        var msg_id = 0,
            $window = $(window),
            $cards_top = $('.cards.top:first'),
            $cards_top_contents = $cards_top.children('.contents:first'),
            $cards_bottom = $('.cards.bottom:first'),
            $cards_bottom_contents = $cards_bottom.children('.contents:first'),
            templates = [];

        // Setup global functions

        // JS --> Python
        window.send_to_plugin = function(plugin, obj){
            i = msg_id++;
            document.title = i + ":::" + plugin + ":::" + JSON.stringify(obj)
        }

        // Python --> JS
        window.new_card = function(card_id, card_type, position){
            $card = templates[card_type].clone().attr('card_id', card_id);
            hide_card($card)

            // Place in position
            if(position == 'default')
                position = 'top_first';

            switch(position){
            case 'top_first':
                $cards_top_contents.prepend($card);
                break;
            case 'top_last':
                $cards_top_contents.append($card);
                break;
            case 'bottom_first':
                $cards_bottom_contents.prepend($card);
                break;
            case 'bottom_last':
            default:
                $cards_bottom_contents.append($card);
                break;
            }

            // Setup
            var hide = false;
            if(card_type in window.card_init_fn)
                hide = window.card_init_fn[card_type](card_id, $card) === true;

            // Show
            if(!hide)
                open_card($card);
        }

        window.send_to_card = function(card_id, object){
            var $card = get_card(card_id);
            card_send_fn[$card.attr('card_type')](card_id, $card, object)
        }

        window.del_card = function(card_id){
            var $card = get_card(card_id);
            close_card($card, function(){$card.remove()})
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
        function get_card(card_id){
            return $('.card[card_id="' + card_id + '"]:first')
        }

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

        function close_card($card, complete){
            $card.animate({opacity: 0}, function(){
                $card.animate({height: 0},
                              {step: resize_top_cards, complete: complete})
            })
        }

        // Setup Card Templates
        $('.card-templates:first').children().each(function(){
            var $template = $(this);
            templates[$template.attr('card_type')] = $template;
        })
    })

})(jQuery);
