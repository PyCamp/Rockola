var app = {}

app.TrackModel = Backbone.Model.extend({
  defaults: {
    'artist': ''
    'track': ''
    'duration': ''
  },
});

app.TrackCollection = Backbone.Collection.extend({
  model: app.TrackModel
});
