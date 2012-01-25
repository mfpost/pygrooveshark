# -*- coding:utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class Song(object):
    '''
    Represents a song.
    Do not use this class directly.
        
    :param id: internal song id
    :param name: name
    :param artist_id: artist's id to generate an :py:class:`Artist` object
    :param artist_name: artist's name to generate an :py:class:`Artist` object
    :param album_id: album's id to generate an :class:`Album` object
    :param album_name: album's name to generate an :class:`Album` object
    :param cover_url: album's cover to generate an :class:`Album` object
    :param track: track number
    :param duration: estimate song duration
    :param popularity: populaity
    :param connection: underlying :class:`Connection` object
    '''
    def __init__(self, id, name, artist_id, artist_name, album_id, album_name, cover_url, track, duration, popularity, connection):
        self._connection = connection
        self._id = id
        self._name = name
        self._artist_id = artist_id
        self._artist_name = artist_name
        self._album_id = album_id
        self._album_name = album_name
        self._album_id = album_id
        self._album_name = album_name
        self._cover_url = cover_url
        self._track = track
        self._duration = duration
        self._popularity = popularity
        self._artist = None
        self._album = None
        
    def __str__(self):
        return '%s - %s - %s' % (self.name, self.artist.name, self.album.name)
    
    @classmethod
    def from_response(cls, song, connection):
        return cls(song['SongID'], song['Name'] if 'Name' in song else song['SongName'], song['ArtistID'], song['ArtistName'], song['AlbumID'], song['AlbumName'],
                   song['CoverArtFilename'], song['TrackNum'], song['EstimateDuration'], song['Popularity'], connection)
    
    @property
    def id(self):
        '''
        internal song id
        '''
        return self._id
    
    @property
    def name(self):
        '''
        name
        '''
        return self._name
    
    @property
    def artist(self):
        '''
        artist as :class:`Artist` object
        '''
        if not self._artist:
            self._artist = Artist(self._artist_id, self._artist_name, self._connection)
        return self._artist
    
    @property
    def album(self):
        '''
        album as :class:`Album` object
        '''
        if not self._album:
            self._album = Album(self._album_id, self._album_name, self._artist_id, self._artist_name, self._cover_url, self._connection)
        return self._album
    
    @property
    def track(self):
        '''
        track number
        '''
        return self._track
    
    @property
    def duration(self):
        '''
        estimate song duration
        '''
        return self._duration
    
    @property
    def popularity(self):
        '''
        populaity
        '''
        return self._popularity
    
    @property
    def stream(self):
        '''
        :class:`Stream` object for playing
        '''
        stream_info = self._connection.request('getStreamKeyFromSongIDEx', {'songID' : self.id, 'country' : self._connection.country,
                                                                            'prefetch' : False, 'mobile' : False},
                                               self._connection.header('getStreamKeyFromSongIDEx', 'jsqueue'))[1]
        return Stream(stream_info['ip'], stream_info['streamKey'], self._connection)
        
from grooveshark.classes.artist import Artist
from grooveshark.classes.album import Album
from grooveshark.classes.stream import Stream