//$(function(){
    //var source = new EventSource("{{ url_for('sse.messages', channel='rockola') }}");
    //source.addEventListener('list_songs', function(e) {
      //alert(e.data);
      //var data = JSON.parse(e.data);
      ////document.body.innerHTML += "New Message: " + data.message + '<br />';
    //}, false);
//});

function votar(track_id, positivo, lielem) {
    if (positivo)
    {
        action = 'votarpositivo'
    }else{
        action = 'votarnegativo'
    }
    url = '/vote?track_id=' + track_id + '&operation=' + action;
    console.log(url);
    console.log(lielem);
    $(lielem).attr('data-theme', 'e');
    $.ajax({url: url});
}

