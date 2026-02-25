import random

class Playlist:
    """Represents a collection of songs"""
    
    def __init__(self, title, description=""):
        
        self.title = title
        self.id = self._generate_id()
        self.description = description
        self.cover = "library/cover_if_none.png"   # Default cover
        self.songs = []
        self._queue = []  # Playback queue (for shuffle)
        self.current_index = 0
    
    def add_song(self, song):
        #add song
        if song not in self.songs:
            self.songs.append(song)
    
    def remove_song(self, song):
        #remove song
        if song in self.songs:
            self.songs.remove(song)
    
    def shuffle(self):
        #create a copy of songs that is shuffled -> maintains original order
        self._queue = self.songs.copy()
        random.shuffle(self._queue)
        return self._queue
    
    def reset_queue(self):
        #use original order
        self._queue = self.songs.copy()
    
    def set_description(self, description):
        #set playlist description
        self.description = description
    
    def get_duration(self):
        #calc total duration
        total_seconds = sum(song.duration for song in self.songs if hasattr(song, 'duration'))
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"{minutes}m {seconds}s"
    
    def save(self, description=""):
        if description:
            self.set_description(description)
        self.reset_queue()

        # save to folder

    
    def get_song_at(self, index):
        #get song at index
        if 0 <= index < len(self.songs):
            return self.songs[index]
        return None
    
    def _generate_id(self):
        #generate unique id
        return f"{self.title}_{random.randint(1000, 9999)}"
    
    ### Utility methods ###

    def __len__(self):
        """Return number of songs"""
        return len(self.songs)
    
    def __str__(self):
        """String representation"""
        return f"Playlist: {self.title} ({self.get_song_count()} songs, {self.get_duration()})"
    