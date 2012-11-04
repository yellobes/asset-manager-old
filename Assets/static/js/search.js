function search(field){
    ajax($(field).val());
    console.log('search')
}

function ajax(query){
    var query0 = encodeURI(query)
    query = query0
    query0 = null
    var domain = document.domain;
    var content = "#content"
    var indicator = "#search-running"
    var indicator_padding_top = $(indicator).data('orig_padding_top');

    if ( !$(indicator).is(':animated') ) {
        $(indicator).animate({
            width: 'toggle',
            paddingTop: '0px'
        }, 100, 'linear' );
    }

    $(content).load(
    "/assets/search?q="+query,
    function() {
        var wait = setInterval(function() {  
  
            if ( !$(indicator).is(':animated')) {  
                clearInterval(wait);
                $(indicator).animate({
                    width: 'toggle',
                    paddingTop: indicator_padding_top
                }, 100, 'linear');
            } 
        }, 10);    
    });
}
