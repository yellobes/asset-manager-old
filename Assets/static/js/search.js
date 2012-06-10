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
    $(indicator).show()
    $(content).load(
    "/assets/search?q="+query,
    function() {
        $(indicator).hide();
    });
}
