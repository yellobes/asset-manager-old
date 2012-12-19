  var $search_filters = $('#search-filters');

  if ( $search_filters.children('li').length < 1 ) {
    $search_filters.hide();
    $('#add-search-filter').hide();
  }

  $('.sticky-tab-header').click(function() {
    if ( $search_filters.children('li').length > 0 ) {
      y = $('.search-filter');
      y.each(function() {
        if( $(this).val() == '' ) {
          $(this).parent('li').remove();
        }
      });
    }

    if ( $('.search-filter').length == 0 ) {
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