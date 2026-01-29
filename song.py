from tinytag import TinyTag

class Song():
    def __init__(self, mp3_path, genre: str = 'n/a'):
        self.path = mp3_path
        self.paused = True
        self.tags = TinyTag.get(self.path)
        if self.tags.genre:
            self.token = self.tags.genre
        else:
            self.token = genre
        
        # Load metadata and cover using TinyTag
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
                self.cover = "test_cover.png"
                
        except Exception as e:
            print(f"Error loading song metadata: {e}")
            self.cover = "test_cover.png"
    
    def __str__(self):
        """String representation"""
        try:
            
            return f"{self.tags.title or 'Unknown'} - {self.tags.artist or 'Unknown Artist'}"
        except:
            return f"Song: {self.path}"