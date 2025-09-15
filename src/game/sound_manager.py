"""
Simple sound system for Classroom Chaos
"""
import pygame
import os

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self.init_mixer()
        self.create_simple_sounds()
    
    def init_mixer(self):
        """Initialize pygame mixer"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except pygame.error:
            print("Warning: Could not initialize audio mixer")
    
    def create_simple_sounds(self):
        """Create simple procedural sounds"""
        try:
            # Try to create sounds with pygame.sndarray if available
            self.create_beep_sounds()
        except Exception as e:
            print(f"Info: Sound effects not available: {e}")
            # Create dummy sound entries for testing
            self.sounds['throw'] = None
            self.sounds['hit'] = None
    
    def create_beep_sounds(self):
        """Create beep sounds (requires numpy/sndarray)"""
        # Create simple throw sound (short beep)
        throw_sound = self.create_beep_sound(0.1, 800)  # 100ms, 800Hz
        self.sounds['throw'] = throw_sound
        
        # Create hit sound (higher pitch beep)
        hit_sound = self.create_beep_sound(0.05, 1200)  # 50ms, 1200Hz
        self.sounds['hit'] = hit_sound
    
    def create_beep_sound(self, duration, frequency):
        """Create a simple beep sound"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = 4096 * (0.5 * (1 + (-1) ** int(2 * frequency * time)))
            arr.append([int(wave), int(wave)])
        
        sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
        return sound
    
    def set_enabled(self, enabled):
        """Enable or disable sound"""
        self.enabled = enabled
    
    def play(self, sound_name):
        """Play a sound if enabled"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        sound = self.sounds[sound_name]
        if sound is None:
            return  # Sound not available
        
        try:
            sound.play()
        except pygame.error:
            pass  # Ignore audio errors in headless environments