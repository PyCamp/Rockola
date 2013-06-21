var app = {}
window.app = app;

app.TrackModel = Backbone.Model.extend({
  defaults: {
    'artist': '',
    'title': '',
    'duration': '',
    'upvotes': 0
  },
});

app.TrackCollection = Backbone.Collection.extend({
  model: app.TrackModel
});


app.LatestView = Backbone.View.extend({
  initialize: function(options) {
    this.$el = $('#latests');
    this.collection = options.collection;
    this.getTracks();
  },
  render: function() {
    var tpls = "";
    this.collection.each(function(model) {
      tpls += _.template('<li><a href="#"><%= artist %> - <%= title %></a></li>', model.toJSON());
    });
    this.$el.html(tpls).listview('refresh');
  },
  getTracks: function() {
    var self = this;
    var source = new EventSource('/messages')
    source.addEventListener('latests', function(e) {
      var response = JSON.parse(e.data);
      _.each(response, function(model) {
        self.collection.add(model);
      });
    });
  },
});


app.SearchItemView = Backbone.View.extend({
  tagName: 'li',
  initialize: function(options) {
    this.model = options.model;
  },
  onClick: function(e) {
    // send add new song request
    e.preventDefault();
  },
  render: function() {
    this.$el.html(_.template('<a href="#"><%= artist %> - <%= title %></a>', this.model.toJSON()));
    this.$el.click(this.onClick);
    return this;
  }
});


app.SearchTracksView = Backbone.View.extend({
  initialize: function(options) {
    this.$el = $('#searchlist');
    this.collection = options.collection
    this.collection.on('add', this.render, this);
    this.collection.on('reset', this.render, this);
    this.getTracks();
  },
  render: function() {
    this.$el.empty();
    var self = this;
    this.collection.each(function(song) {
      var searchItemView = new app.SearchItemView({model: song});
      self.$el.append(searchItemView.render().el);
    });
    this.$el.listview('refresh');
  },
  getTracks: function() {
    // ajax call to retrive all songs.
  }
});

app.NowPlayingView = Backbone.View.extend({ });


app.init = function() {
  var songsCollection = new app.TrackCollection();
  var latestCollection = new app.TrackCollection();
  new app.SearchTracksView({collection: songsCollection});
  new app.LatestView({collection: latestCollection});
  songsCollection.add([
      {'id': 1,
      'title': 'Smoke on the Water',
      'artist': 'Deep Purple',
      },
      {'id': 2,
      'title': 'Faithful',
      'artist': 'Pearl Jam',
      },
      {'id': 3,
      'title': 'No Way',
      'artist': 'Pearl Jam',
      },
      {'id': 4,
      'title': 'Daughter',
      'artist': 'Pearl Jam',
      },
  ]);
}


$(document).ready(function() {
  app.init();
});
