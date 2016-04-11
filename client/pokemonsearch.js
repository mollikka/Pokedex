$(document).ready(function(){
  $('form').on('submit',function(e){
    e.preventDefault();
    $.ajax({
      type: 'GET',
      url: "pokemon/"+$('#pokesearch').val(),
      success: function(response) {alert(response.name);},
      error: function() {alert("Pokemon not found");},
    });
  });
});
