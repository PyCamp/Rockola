
import json
from subprocess import Popen
from urllib import urlencode
from urllib2 import urlopen



class VLCController(object):

    PORT = '10333'

    def __init__(self):
        '''
            start the VLC process
        '''
        self.p = Popen(['vlc',
                        '-I http',
                        '--http-host', '0.0.0.0',
                        '--http-port', self.PORT])
        self.base_url = 'http://localhost:%s/requests/status.xml' % self.PORT

    def add_song(self, path, play_it_now=False):
        '''
            Add a new song to the playlist and play it
        '''
        data = {'command': 'in_play',
                'input': 'file://' + path}
        s = '%s?%s' % (self.base_url, urlencode(data))
        urlopen(s)

    def get_player_status(self):
        pass


class ShivaClient(object):

    PORT = '9002'
    URL = 'localhost'
    def __init__(self):
        self.base_url =  'http://%s:%s/' %(self.URL,self.PORT)
        self.artists = {}
        for artist in self.get_artists():
            artist_id, name = artist['id'], artist['name']
            self.artists[artist_id] = name

    def _request(self, command):
        r = urlopen(self.base_url + command)
        data = r.read()
        return json.loads(data)

    def get_tracks(self):
        tracks = self._request('tracks')
        response = []
        for track in tracks:
            track_id = track['id']
            track_title = track['name']
            artist_id = track['artist']['id']
            artist = self.artist_id[artist_id]
            response.append({'id': track_id,
                             'title': track_title,
                             'artist': artist})
        return json.dumps(response)

    def get_artists(self):
        return self._request('artists')

if __name__ == '__main__':
    pass

