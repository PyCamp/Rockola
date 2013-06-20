$(function(){
    var source = new EventSource("{{ url_for('sse.messages', channel='rockola') }}");
    source.addEventListener('list_songs', function(e) {
      alert(e.data);
      var data = JSON.parse(e.data);
      //document.body.innerHTML += "New Message: " + data.message + '<br />';
    }, false);
});
