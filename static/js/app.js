var app = {}
window.app = app;

app.TrackModel = Backbone.Model.extend({
  defaults: {
    'artist': '',
    'title': '',
    'duration': '',
    'upvotes': 0,
    'downvotes': 0
  },
});

app.TrackCollection = Backbone.Collection.extend({
  model: app.TrackModel
});


app.NowPlayingView = Backbone.View.extend({
  initialize: function(options) {
    this.$el = $('#latests');
    this.collection = options.collection;
    //this.getTracks();
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
    source.addEventListener('nowplaying', function(e) {
      var response = JSON.parse(e.data);
      _.each(response, function(model) {
        self.collection.add(model);
      });
    });
  },
});


app.LatestItemView = Backbone.View.extend({
  tagName: 'li',
  initialize: function(options) {
    this.model = options.model;
    //_.bindAll(this, this.render);
    
  },
  addVote: function(e) {
    // send add new song request
    alert('Nuevo voto para ' + this.model.get('artist'));
    e.preventDefault();
  },
  render: function() {
    this.$el.html(_.template('<a href="#"><%= artist %> - <%= title %><span class="ui-li-count"><%= upvotes %></span></a> <a href="#" class="add-vote" data-icon="plus" data-theme="a">plus</a>', this.model.toJSON()));
    this.$el.find('.add-vote').click($.proxy(this.addVote, this));
    return this;
  }
});


app.LatestView = Backbone.View.extend({
  initialize: function(options) {
    this.$el = $('#latestlistview');
    this.collection = options.collection;
    this.collection.on('add', this.render, this);
    this.collection.on('reset', this.render, this);
    //this.getTracks();
  },
  render: function() {
    this.$el.empty();
    var self = this;
    this.collection.each(function(song) {
      var latestItemView = new app.LatestItemView({model: song});
      self.$el.append(latestItemView.render().el);
    });
    this.$el.listview('refresh');
  },
  getTracks: function() {
    var self = this;
    var source = new EventSource('http://192.168.10.63:8888/')
    source.addEventListener('base', function(e) {
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
    alert('New song request ' + this.model.get('artist'));
    e.preventDefault();
  },
  render: function() {
    this.$el.html(_.template('<a href="#"><%= artist %> - <%= title %></a>', this.model.toJSON()));
    this.$el.click($.proxy(this.onClick, this));
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


app.init = function() {
  var songsCollection = new app.TrackCollection();
  var latestCollection = new app.TrackCollection();
  var nowPlayingCollection = new app.TrackCollection();
  new app.SearchTracksView({collection: songsCollection});
  new app.LatestView({collection: latestCollection});
  new app.NowPlayingView({collection: nowPlayingCollection});
  latestCollection.add([
      {'id': 6,
      'title': 'Smoke on the Waterrrrr',
      'artist': 'Deep Thought',
      'upvotes': '42'
      },
  ]);
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
