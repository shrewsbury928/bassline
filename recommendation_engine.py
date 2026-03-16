import random
from playlist import Playlist
from song_library_manager import SongLibraryManager as song_lib


class RecommendationEngine:
    """Provides song recommendations based on the library"""
    
    def __init__(self):
        self.manager = song_lib()
        self.songs = self.manager.get_all_songs()
    
    def get_random_recommendations(self, count=4):
        #random songs for sample testing
        all_songs = self.manager.get_all_songs()
        
        if len(all_songs) == 0:
            return []
        
        # Return up to 'count' random songs
        num_songs = min(count, len(all_songs)) #pick the smaller number
        return random.sample(all_songs, num_songs) #return random selection from list
    
    def create_playlist_from_songs(self, title="Recommended", description="Auto-generated playlist"):
        #random playlist creation from songs
        playlist = Playlist(title, description)
        songs = self.get_random_recommendations(count=10)
        for song in songs:
            playlist.add_song(song)
        playlist.save()
        return playlist
    
    def get_genre_recommendations(self, genre, count=4):
        """Get recommendations for a specific genre"""
        genre_songs = song_lib.get_songs_by_genre(genre)
        
        if len(genre_songs) == 0:
            return []
        
        num_songs = min(count, len(genre_songs))
        return random.sample(genre_songs, num_songs)
    
    def get_artist_recommendations(self, artist, count=4):
        """Get songs from a specific artist"""
        artist_songs = song_lib.get_songs_by_artist(artist)
        
        if len(artist_songs) == 0:
            return []
        
        num_songs = min(count, len(artist_songs))
        return random.sample(artist_songs, num_songs)
