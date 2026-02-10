import random
from playlist import Playlist
from library_manager import library

class RecommendationEngine:
    """Provides song recommendations based on the library"""
    
    def __init__(self):
        self.songs = library.get_all_songs()
    
    def get_random_recommendations(self, count=4):
        #random songs for sample testing
        all_songs = library.get_all_songs()
        
        if len(all_songs) == 0:
            return []
        
        # Return up to 'count' random songs
        num_songs = min(count, len(all_songs))
        return random.sample(all_songs, num_songs)
    
    def create_playlist_from_songs(self, songs, title="Recommended", description="Auto-generated playlist"):
        #random playlist creation from songs
        playlist = Playlist(title, description)
        for song in songs:
            playlist.add_song(song)
        playlist.save()
        return playlist
    
    def get_genre_recommendations(self, genre, count=4):
        """Get recommendations for a specific genre"""
        genre_songs = library.get_songs_by_genre(genre)
        
        if len(genre_songs) == 0:
            return []
        
        num_songs = min(count, len(genre_songs))
        return random.sample(genre_songs, num_songs)
    
    def get_artist_recommendations(self, artist, count=4):
        """Get songs from a specific artist"""
        artist_songs = library.get_songs_by_artist(artist)
        
        if len(artist_songs) == 0:
            return []
        
        num_songs = min(count, len(artist_songs))
        return random.sample(artist_songs, num_songs)
