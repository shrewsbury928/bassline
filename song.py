from tinytag import TinyTag

class Song():
    def __init__(self, mp3_path, genre: str = 'n/a'):
        self.path = mp3_path
        self.paused = True
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
                self.cover = "one.png"
                
        except Exception as e:
            print(f"Error loading song metadata: {e}")
            self.cover = "one.png"
    
    def __str__(self):
        """String representation"""
        try:
            tags = TinyTag.get(self.path)
            return f"{tags.title or 'Unknown'} - {tags.artist or 'Unknown Artist'}"
        except:
            return f"Song: {self.path}"