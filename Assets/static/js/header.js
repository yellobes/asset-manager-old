// Peter Novotnak :: Flexion, 2012

jQuery.fn.keyupQueue = function(callback, delay) {
    return this.each(function(){
        var timer = null;
        $(this).keyup(function() {
            if (timer)
                window.clearTimeout(timer);
            timer = window.setTimeout( function() {
                timer = null;
                callback();
            }, delay || 200);
        });
    });
};


/* Search
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 */

var filter_element = '<li><input class="search-filter" type="text" placeholder="&nbsp;filter" style="width:95%;"><a href="#" class="remove-filter">-</a></li>';

$(document).ready(function() {
  $('#search-wrapper').css({'width': $('#search-wrapper').width()});
  var $search_filters = $('#search-filters');
  var $search_type = $('#type');

  if ( $search_filters.children('li').length < 1 ) {
    $search_filters.hide();
    $('#add-search-filter').hide();
  }

  $('.sticky-tab-header').click(function() {
    if ( $search_filters.children('li').length > 0 ) {
      y = $('.search-filter');
      y.each(function() {
        if( $(this).val() === '' ) {
          $(this).parent('li').remove();
        }
      });
    }

    if ( $('.search-filter').length === 0 ) {
      $search_filters.append(filter_element);
      $search_filters.toggle(300);
      $('#add-search-filter').toggle(400);
    }
  });

  $('#add-search-filter').click(function(){
    $search_filters.show(200, function() {
      $search_filters.append(filter_element);
      $search_filters.children('li').last().toggle();
      $search_filters.children('li').last().toggle(400);
      $search_filters.children('li').last().keyupQueue(function(){
        search();
      });
    });
  });

  $('.remove-filter').live('click', function(){
    x = $(this).parent();
    x.toggle(200, function(){
      x.remove();
      if ( $search_filters.children('li').length < 1 ) {
        $search_filters.hide(1000);
        $('#add-search-filter').toggle(400);
      }

    });
  });

  $('#search').keyupQueue(function(){
    search($search_type.val());
  });

  function search(type){
    filters = '';
    exclude = '';
    $('.search-filter').each(function(){
      filters += ( $(this).val() + ',' );
      });
    exclude = $('#exclude').val();
    $.get('/assets/'+type,
      { 'q': $('#search').val(),
        '!': exclude,
        '|': filters },
      function(responseText){
        $("#content").html(responseText);
      }
    );
  }
  search($search_type.val());
});


/* Header links
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////////////////////////////////////////////
 **/

$(document).ready(function() {
  var $menu = $('#menu');
  var $menu_header = $('.menu-header');
  var $page_header = $('#page-header');
  var $search_wrapper = $('#search-wrapper');
  var menu_margin = $page_header.width() - $menu.width() - $search_wrapper.width() - 50;


  $('.menu-header').mouseenter(function() {
    $(this).children('ul').show(100);
  }).mouseleave(function() {
    $(this).children('ul').hide(100);
  });

  $('.menu-header').each(function() {
    $(this).width( $(this).children('ul').width() );
    $(this).children('ul').hide();
  });

  var height = '';

  $('.menu-header').each(function(){
    $(this).height($(this).height());
    if( height < $(this).height() ){
      height = $(this).height();
    }
    $menu.height(height);
  });
  $menu.css({'margin-left' : menu_margin + 'px' });
  $menu.css({'margin-top' : ( ( $page_header.height() - height ) - 2) + 'px' });
});

$(window).resize(function(){
  var $menu = $('#menu');
  var $page_header = $('#page-header');
  var $search_wrapper = $('#search-wrapper');
  var menu_margin = $page_header.width() - $menu.width() - $search_wrapper.width() - 50;

  console.log($page_header.width() + ' - ' + $menu.width() + ' - ' + $search_wrapper.width());
  console.log(menu_margin);
  if( 1 < menu_margin ){
    $menu.css({'margin-left' :  menu_margin + 'px' });
  } else {
    $menu.css({'margin-left' : '5px' });
    $menu.css({'margin-top' : '0px' });
  }
});
