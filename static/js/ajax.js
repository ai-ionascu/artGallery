$(function() {
  
    $("#place_bid").submit(function(e) {
      e.preventDefault();
      var serializedData = $(this).serialize();
      $.ajax({
        type: 'POST',
        url: "bid/",
        data: serializedData,
        success: function(response){
          console.log(response);
          $('#form_err').hide();
            $("#alert").fadeIn();
            setTimeout(function() { $("#alert").fadeOut(); }, 3000);
            $("#place_bid").trigger('reset');
            $('#id_bid').focus();
            var current_price = JSON.parse(response['current_price'])
            $('#current_price').text(`Current Bid Price: ${current_price}`);
        },
        error: function(response){
          console.log(response);
          $("#form_err").text(`${response['responseJSON']['error']['__all__']}`);
          $("#form_err").fadeIn();
          $("#place_bid").trigger('reset');
          $('#id_bid').focus();
        }
      });
    });
});