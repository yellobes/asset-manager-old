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
