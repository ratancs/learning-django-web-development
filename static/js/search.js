$('#search-form').submit(function(e){
    $.post('/search/', $(this).serialize(), function(data){
       $('.tweets').html(data);
    });
    e.preventDefault();
});