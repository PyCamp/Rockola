var app = {}
window.app = app;


app.TrackModel = Backbone.Model.extend({
  defaults: {
    'artist': '',
    'title': '',
    'duration': '',
    'votes': 0,
    'downvotes': 0
  },
});


app.TrackCollection = Backbone.Collection.extend({
  model: app.TrackModel
});


app.CurrentSongView = Backbone.View.extend({
  el: '#nowplayingsong',
  initialize: function(options) {
    this.model = options.model;
    this.model.bind('change', this.render, this);
  },
  addVote: function(e) {
    // send add vote request
    alert('Nuevo voto negativo para ' + this.model.get('artist'));
    e.preventDefault();
  },
  render: function() {
    var tpl = $('#currentsongtpl').html();
    this.$el.html(_.template(tpl, this.model.toJSON()));
    this.$el.hasClass('ui-listview') && this.$el.listview('refresh');
    this.$el.find('.vote-down').click($.proxy(this.addVote, this));
    return this;
  }
});


app.NowPlayingView = Backbone.View.extend({
  initialize: function(options) {
    this.$el = $('#nowplayinglist');
    this.collection = options.collection;
    this.collection.on('add', this.render, this);
    this.collection.on('reset', this.render, this);
    //this.getTracks();
  },
  addVote: function(e) {
    // send add vote request
    alert('Nuevo voto para ' + this.model.get('artist'));
    $.post('/vote', {track_id: this.model.get('id'), operation: 'votonegativo'});
    e.preventDefault();
  },
  render: function() {
    this.$el.empty();
    var self = this;
    this.collection.each(function(song) {
      var latestItemView = new app.LatestItemView({model: song});
      self.$el.append(latestItemView.render().el);
    });
    this.$el.hasClass('ui-listview') && this.$el.listview('refresh');
  }
});


app.LatestItemView = Backbone.View.extend({
  tagName: 'li',
  initialize: function(options) {
    this.model = options.model;
  },
  addVote: function(e) {
    // send add vote request
    alert('Nuevo voto para ' + this.model.get('artist'));
    $.post('/vote', {track_id: this.model.get('id'), operation: 'votopositivo'});
    e.preventDefault();
  },
  render: function() {
    this.$el.html(_.template('<a href="#"><%= artist %> - <%= title %><span class="ui-li-count"><%= votes %></span></a> <a href="#" class="add-vote" data-icon="plus" data-theme="a">plus</a>', this.model.toJSON()));
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
  },
  render: function() {
    this.$el.empty();
    var self = this;
    this.collection.each(function(song) {
      var latestItemView = new app.LatestItemView({model: song});
      self.$el.append(latestItemView.render().el);
    });
    this.$el.hasClass('ui-listview') && this.$el.listview('refresh');
  },
  parseMessage: function(data) {
    _.each(response, function(model) {
      self.collection.add(model);
    });
  }
});


app.SearchItemView = Backbone.View.extend({
  tagName: 'li',
  initialize: function(options) {
    this.model = options.model;
  },
  onClick: function(e) {
    // send add new song request
    alert('New song request ' + this.model.get('artist'));
    //$.post('/newsong', {track_id: this.model.get('id'), operation: 'votopositivo'});
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
    this.$el.hasClass('ui-listview') && this.$el.listview('refresh');
  },
  getTracks: function() {
    // ajax call to retrive all songs.
  }
});

app.parseMessages = function(data){
    var jsondata = JSON.parse(data);
    app.currentSong.set(jsondata.top[0]);
    jsondata.top.shift();
    app.nowPlayingCollection.reset(jsondata.top);
    app.latestCollection.reset(jsondata.latest);
    console.log(jsondata.latest);
};

app.init = function() {
  app.songsCollection = new app.TrackCollection();
  app.latestCollection = new app.TrackCollection();
  app.nowPlayingCollection = new app.TrackCollection();
  app.currentSong = new app.TrackModel({});

  new app.SearchTracksView({collection: app.songsCollection});
  new app.LatestView({collection: app.latestCollection});
  new app.NowPlayingView({collection: app.nowPlayingCollection});
  new app.CurrentSongView({model: app.currentSong});

  $.eventsource({label: 'base', url: 'http://192.168.10.58:8888/?channels=base', message: app.parseMessages});


$(document).ready(function() {
  app.init();
});
