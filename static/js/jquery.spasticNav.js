(function($) {

  $.fn.spasticNav = function(options) {
    options = $.extend({
      overlap : 20,
      speed : 500,
      reset : 100,
      color : '#0b2b61',
      easing : 'easeOutExpo'
    }, options);

    return this.each(function() {

      var reset, cur;
      var nav = $(this);
      var blob = $('#blob');
      if (blob.length == 0) {
        blob = $('<li id="blob"></li>').appendTo(this);
        $('li:not(#blob)', nav).hover(function() {
          // mouse over
          clearTimeout(reset);
          blob.animate({
            left : $(this).position().left,
          }, {
            duration : options.speed,
            easing : options.easing,
            queue : false
          });
        }, function() {
          // mouse out	
          reset = setTimeout(function() {
            blob.animate({
              width : $('.selected', nav).outerWidth(),
              left : $('.selected', nav).position().left
            }, options.speed)
          }, options.reset);

        });
      }

      if (options.select) {
        nav.find('.selected').removeClass('selected');
        nav.find(options.select).addClass('selected');
      }
      cur = nav.find('.selected');

      blob.css({
        left : cur.position().left,
        top : cur.position().top - options.overlap / 2
      });

      var imgs = nav.find('img');
      var count = imgs.length;
      
      imgs.load(function(){
        count --;
        if (count == 0){
          blob.css({
            left : cur.position().left,
            top : cur.position().top - options.overlap / 2
          });
        }
      });
    }); // end each

  };

})(jQuery);
