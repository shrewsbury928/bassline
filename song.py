from tinytag import TinyTag

class Song():
    def __init__(self, mp3_path, genre: str = 'n/a'):
        self.path = mp3_path
        self.paused = True
        
        # Load metadata using TinyTag
        try:
            self.tags = TinyTag.get(self.path)
            
            # Store commonly used attributes directly
            self.title = self.tags.title or "Unknown Title"
            self.artist = self.tags.artist or "Unknown Artist"
            self.album = self.tags.album or "Unknown Album"
            self.duration = self.tags.duration or 0
            
            if self.tags.genre:
                self.token = self.tags.genre
            else:
                self.token = genre
        except Exception as e:
            print(f"Error loading song metadata: {e}")
            self.tags = None
            self.title = "Unknown Title"
            self.artist = "Unknown Artist"
            self.album = "Unknown Album"
            self.duration = 0
            self.token = genre
        
        # Load cover art
        try:
            # Get image data
            tags_with_image = TinyTag.get(self.path, image=True)
            
            # Extract cover art
            if hasattr(tags_with_image, 'get_image'):
                image_data = tags_with_image.get_image()
                if image_data:
                    self.cover = image_data  # This is bytes
                else:
                    self.cover = None
            else:
                self.cover = None
            
            # If no cover found, use default
            if not self.cover:
                self.cover = "library/cover_if_none.png"
                
        except Exception as e:
            print(f"Error loading song cover: {e}")
            self.cover = "library/cover_if_none.png"
    
    def __str__(self):
        """String representation"""
        return f"{self.title} - {self.artist}"
    
    def __repr__(self):
        """String representation for debugging"""
        return f"Song('{self.title}' by {self.artist})"