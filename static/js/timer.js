var x = setInterval(function(){

    var now = new Date().getTime();
    for (i=0; i<auctions.length; i++) {
      var start_date = new Date(auctions[i].start_date).getTime();
      var duration = auctions[i].duration;
      var end_date = new Date(parseInt(start_date) + parseInt(duration));
      var time_left = end_date - now;
        console.log(time_left);
        var days = Math.floor(time_left / (1000 * 60 * 60 * 24));
        var hours = Math.floor((time_left % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((time_left % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((time_left % (1000 * 60)) / 1000);

        $(`#time_left_${auctions[i].pk}`).text(`Time left: ${days} days ${hours} hours ${minutes} minutes ${seconds} seconds`);      
        if (time_left < 0) {
            $(`#time_left_${auctions[i].pk}`).text("AUCTION EXPIRED");
            auctions.splice(i,1);     
        }
      if (auctions.length === 0){
        clearInterval(x);
      };
    }
}, 1000);