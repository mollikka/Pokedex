$(document).ready(function(){
  var template;
  var searcherror;

  $.ajax({
    url: "pokeresult.html",
    success: function(html) {template = Handlebars.compile(html);},
  });
  
  $.ajax({
    url: "searcherror.html",
    success: function(html) {searcherror = html;},
  });

  Handlebars.registerHelper('list', function(items, options) {
    var out = "<ul>";

    for(var i=0, l=items.length; i<l; i++) {
      out = out + "<li>" + options.fn(items[i]) + "</li>";
    }

    return out + "</ul>";
  });

  $('form').on('submit',function(e){
    e.preventDefault();
    $.ajax({
      type: 'GET',
      url: "pokemon/"+$('#pokesearch').val(),
      success: function(response) {add_result(response);},
      error: function() {$('#pokeresults').prepend(searcherror);},
    });
  });

  function add_result(json){
    $('#pokeresults').prepend(template(json));
  }
});
