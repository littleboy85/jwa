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
		
		 	var nav = $(this),
		 		blob,
		 		reset;
		 		
		 	$('<li id="blob"></li>').css({
		 		left : $('.selected', nav).position().left,
		 		top : $('.selected', nav).position().top - options.overlap / 2		 		
		 	}).appendTo(this);
		 	
		 	blob = $('#blob', nav);		 	
		 	
			$('li:not(#blob)', nav).hover(function() {
				// mouse over
				clearTimeout(reset);
				blob.animate(
					{
						left : $(this).position().left,
						
					},
					{
						duration : options.speed,
						easing : options.easing,
						queue : false
					}
				);
			}, function() {
				// mouse out	
				reset = setTimeout(function() {
					blob.animate({
						width : $('.selected', nav).outerWidth(),
						left : $('.selected', nav).position().left
					}, options.speed)
				}, options.reset);
	
			});
		
		}); // end each
	
	};

})(jQuery);