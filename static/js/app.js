var app = {}
window.app = app;

app.TrackModel = Backbone.Model.extend({
  defaults: {
    'artist': '',
    'track': '',
    'duration': '',
    'upvotes': 0
  },
});

app.TrackCollection = Backbone.Collection.extend({
  model: app.TrackModel
});

app.SearchTracksView = Backbone.View.extend({
  initialize: function(options) {
    this.$el = $('#searchlist');
    this.collection = options.collection
    this.collection.on('add', this.render, this);
    this.collection.on('reset', this.render, this);
    this.getTracks();
  },
  getTracks: function() {
    var self = this;
    $.getJSON('/get_tracks', function(response){
      _.each(response, function(model) {
        self.collection.add(model);
      });
    });
  },
  render: function() {
    var tpls = "";
    this.collection.each(function(model) {
      tpls += _.template('<li><a href="docs/api/themes.html"><%= artist %> - <%= track %></a></li>', model.toJSON());
    });
    this.$el.html(tpls); 
  }
});

app.NowPlayingView = Backbone.View.extend({ });

app.init = function() {
  var trackCollection = new app.TrackCollection();
  new app.SearchTracksView({collection: trackCollection});
}


$(document).ready(function() {
  app.init();
});
