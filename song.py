from tinytag import TinyTag

class Song:
    def __init__(self, mp3_path, genre=None):
        self.path = mp3_path
        self.paused = True
        
        # Load metadata from file
        try:
            self.tags = TinyTag.get(self.path)
            
            # Use genre from tags if available, otherwise use provided genre
            if self.tags.genre:
                self.token = self.tags.genre
            else:
                self.token = genre or 'Unknown'
                
        except Exception as e:
            print(f"Error loading tags for {mp3_path}: {e}")
            # Create minimal tags object
            class MinimalTags:
                title = "Unknown Title"
                artist = "Unknown Artist"
                album = "Unknown Album"
                genre = genre or "Unknown"
                duration = 0
            self.tags = MinimalTags()
            self.genre = genre or 'Unknown'
        
        # Load cover art
        self._load_cover_art()
    
    def _load_cover_art(self):
        # Attempt to load cover art from tags, otherwise use default
        try:
            tags_with_image = TinyTag.get(self.path, image=True)
            
            # Extract cover art bytes
            if hasattr(tags_with_image, 'get_image'):
                image_data = tags_with_image.get_image()
                if image_data:
                    self.cover = image_data  # Bytes
                else:
                    self.cover = "library/cover_if_none.png"  # Default fallback
            else:
                self.cover = "library/cover_if_none.png"
                
        except Exception as e:
            #print(f"Error loading cover art: {e}")
            self.cover = "library/cover_if_none.png"
    

    ### METADATA + UTILITIES ###

    @property
    def title(self):
        """Get song title"""
        return self.tags.title or "Unknown Title"
    
    @property
    def artist(self):
        """Get song artist"""
        return self.tags.artist or "Unknown Artist"
    
    @property
    def album(self):
        """Get album name"""
        return self.tags.album or "Unknown Album"
    
    @property
    def duration(self):
        """Get song duration in seconds"""
        return self.tags.duration or 0
    
    def __str__(self):
        """String representation of the song"""
        return f"{self.title} - {self.artist}"