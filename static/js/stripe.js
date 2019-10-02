$(function() {
  
  var elements = stripe.elements();
  var card = elements.create('card',{hidePostalCode: true});
  card.mount('#card-element');

  $("#payment-form").submit(function(e) {
    e.preventDefault()
    var form = this;
    stripe.createToken(card).then(function(response) {
      if (response.token) {
        
        $("#card-errors").hide();
        $("#token").val(response.token.id);

        form.submit();

      } else {
          $("#card-errors").text(response.error.message);
          $("#card-errors").show();
        }
    });
    return false;
  });
});