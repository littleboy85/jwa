$(function() {
  var $porfolio = $('#showporfolio_container');
  var $adnav = $('#porfolio_nav_container .ad-nav');

  $('#nav').spasticNav({select: '.porfolio'});

  $('.ad-thumb-list>li.picture').each(function(){
    var $this = $(this);
    $this.find('img').data('ad-desc', $this.find('.picture_data').html());
  });

  var images = $('ul.ad-thumb-list>li.picture>a.image');
  var cur = images.filter('.current');
  var hash = '#ad-image-' + images.index(cur);
  console.log(hash);
  location.hash = hash;
    
  var galleries = $('.ad-gallery').adGallery({
    callbacks: {
      afterImageVisible: function(){
        // preload next image
        var context = this;
        this.preloadImage(this.current_index + 1);
        $('.ad-image>img').click(function(){
          window.location.href = $(this).attr('src');
        });
      }
    },
    hooks: {
      displayDescription: function(image) {
        $('.ad-image-description').html(image.desc);
        $('.ad-title').text(image.title || '');
        $adnav.height($porfolio.height());
      }
    }
  });

  $adnav.height($porfolio.height());
});

