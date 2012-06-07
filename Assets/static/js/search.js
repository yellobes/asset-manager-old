function search(field){
    ajax($(field).val());
    console.log('search')
}

function ajax(query){
    var query0 = encodeURI(query)
    query = query0
    query0 = null
    var domain = document.domain;
    $("#content").load(
    "/assets/search/"+query);
}
