$(function() {
  
    $("#place_bid").submit(function(e) {
      e.preventDefault();
      var serializedData = $(this).serialize();
      $.ajax({
        type: 'POST',
        url: "bid/",
        data: serializedData,
        success: function(response){
            alert('You have successfully placed a bid.');
            $("#place_bid").trigger('reset');
            $('#id_bid').focus();
            var current_price = JSON.parse(response['current_price'])
            $('#current_price').text(`Current Bid Price: ${current_price}`);
        },
        error: function(response){
          alert(response['responseJSON']['error']['__all__']);
          $("#place_bid").trigger('reset');
          $('#id_bid').focus();
        }
      })
    })
})