import os
from song import Song

class SongLibrary:
    """Global song library manager - loads and manages all songs"""
    
    def __init__(self, songs_folder="library"):
        self.songs_folder = songs_folder
        self.all_songs = []
        self._loaded = False
    
    def load_songs(self, force_reload=False):
        """Load all MP3 files from the songs folder"""
        if self._loaded and not force_reload:
            return self.all_songs
        
        self.all_songs = []
        
        if not os.path.exists(self.songs_folder):
            #print(f"Songs folder '{self.songs_folder}' not found! Creating it...")
            os.makedirs(self.songs_folder)
            return self.all_songs
        
        # Find all MP3 files
        for filename in os.listdir(self.songs_folder):
            if filename.lower().endswith('.mp3'):
                file_path = os.path.join(self.songs_folder, filename)
                try:
                    song = Song(file_path)
                    self.all_songs.append(song)
                    print(f"Loaded: {song}")
                except Exception as e:
                    print(f"Could not load {filename}: {e}")
        
        self._loaded = True
        print(f"\nTotal songs loaded: {len(self.all_songs)}")
        return self.all_songs
    
    def get_all_songs(self):
        """Get all available songs (loads if not already loaded)"""
        if not self._loaded:
            self.load_songs()
        return self.all_songs
    
    def search_songs(self, query):
        """Search songs by title or artist"""
        if not self._loaded:
            self.load_songs()
        
        query = query.lower()
        results = []
        
        for song in self.all_songs:
            try:
                from tinytag import TinyTag
                tags = TinyTag.get(song.path)
                title = (tags.title or "").lower()
                artist = (tags.artist or "").lower()
                album = (tags.album or "").lower()
                
                if query in title or query in artist or query in album:
                    results.append(song)
            except:
                pass
        
        return results
    
    def get_songs_by_genre(self, genre):
        """Get songs filtered by genre"""
        if not self._loaded:
            self.load_songs()
        
        matching_songs = []
        for song in self.all_songs:
            try:
                from tinytag import TinyTag
                tags = TinyTag.get(song.path)
                if tags.genre and genre.lower() in tags.genre.lower():
                    matching_songs.append(song)
            except:
                pass
        return matching_songs
    
    def get_songs_by_artist(self, artist):
        """Get all songs by a specific artist"""
        if not self._loaded:
            self.load_songs()
        
        matching_songs = []
        artist_lower = artist.lower()
        
        for song in self.all_songs:
            try:
                from tinytag import TinyTag
                tags = TinyTag.get(song.path)
                if tags.artist and artist_lower in tags.artist.lower():
                    matching_songs.append(song)
            except:
                pass
        return matching_songs
    
    def reload(self):
        """Force reload all songs from folder"""
        return self.load_songs(force_reload=True)


# Create a global instance that can be imported anywhere
library = SongLibrary()