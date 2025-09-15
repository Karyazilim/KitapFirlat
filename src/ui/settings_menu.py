"""
Settings Menu Screen for Classroom Chaos
"""
import pygame
from src.ui.components import Button, Label

class SettingsMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Colors
        self.primary_color = (238, 108, 43)  # #ee6c2b
        self.text_color = (24, 19, 17)  # #181311
        self.gray_color = (107, 114, 128)  # gray-500
        self.secondary_button_color = (244, 242, 240)  # #f4f2f0
        
        # Settings state
        self.settings = {
            'difficulty': 'Normal',
            'sound_enabled': True
        }
        
        # UI Components
        self.title = Label(width // 2, 80, "Settings", 36, self.text_color, center=True)
        
        # Difficulty setting
        self.difficulty_label = Label(40, 150, "Difficulty:", 20, self.text_color)
        self.difficulty_options = ["Easy", "Normal", "Hard"]
        self.difficulty_index = 1  # Default to Normal
        
        # Sound setting
        self.sound_label = Label(40, 230, "Sound:", 20, self.text_color)
        
        # Buttons
        button_width = 120
        button_height = 40
        
        # Difficulty buttons
        self.easy_btn = Button(40, 180, button_width, button_height, 
                              "Easy", self.secondary_button_color, self.text_color, 16)
        self.normal_btn = Button(170, 180, button_width, button_height, 
                                "Normal", self.primary_color, (255, 255, 255), 16)
        self.hard_btn = Button(300, 180, button_width, button_height, 
                              "Hard", self.secondary_button_color, self.text_color, 16)
        
        # Sound buttons
        self.sound_on_btn = Button(40, 260, button_width, button_height, 
                                  "On", self.primary_color, (255, 255, 255), 16)
        self.sound_off_btn = Button(170, 260, button_width, button_height, 
                                   "Off", self.secondary_button_color, self.text_color, 16)
        
        # Back button
        self.back_btn = Button(40, height - 120, width - 80, 50, 
                              "Back to Menu", self.secondary_button_color, self.text_color, 18)
        
        # Focus management
        self.focusable_items = [
            self.easy_btn, self.normal_btn, self.hard_btn,
            self.sound_on_btn, self.sound_off_btn,
            self.back_btn
        ]
        self.focused_index = 1  # Start with Normal difficulty focused
        self.update_focus()
        self.update_button_states()
    
    def update_focus(self):
        """Update focus state of UI elements"""
        for i, item in enumerate(self.focusable_items):
            item.is_focused = (i == self.focused_index)
    
    def update_button_states(self):
        """Update button colors based on current settings"""
        # Difficulty buttons
        difficulty_buttons = [self.easy_btn, self.normal_btn, self.hard_btn]
        for i, btn in enumerate(difficulty_buttons):
            if i == self.difficulty_index:
                btn.color = self.primary_color
                btn.text_color = (255, 255, 255)
            else:
                btn.color = self.secondary_button_color
                btn.text_color = self.text_color
        
        # Sound buttons
        if self.settings['sound_enabled']:
            self.sound_on_btn.color = self.primary_color
            self.sound_on_btn.text_color = (255, 255, 255)
            self.sound_off_btn.color = self.secondary_button_color
            self.sound_off_btn.text_color = self.text_color
        else:
            self.sound_on_btn.color = self.secondary_button_color
            self.sound_on_btn.text_color = self.text_color
            self.sound_off_btn.color = self.primary_color
            self.sound_off_btn.text_color = (255, 255, 255)
    
    def get_settings(self):
        """Return current settings"""
        return self.settings.copy()
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.focused_index >= 3:  # Sound buttons or back button
                    self.focused_index = min(2, self.focused_index - 3)
                else:  # Difficulty buttons
                    self.focused_index = 5  # Back button
                self.update_focus()
            elif event.key == pygame.K_DOWN:
                if self.focused_index <= 2:  # Difficulty buttons
                    self.focused_index = min(4, self.focused_index + 3)
                else:  # Sound buttons
                    self.focused_index = 5  # Back button
                self.update_focus()
            elif event.key == pygame.K_LEFT:
                if self.focused_index <= 2 and self.focused_index > 0:  # Difficulty buttons
                    self.focused_index -= 1
                elif self.focused_index == 4:  # Sound off button
                    self.focused_index = 3  # Sound on button
                self.update_focus()
            elif event.key == pygame.K_RIGHT:
                if self.focused_index <= 1:  # Difficulty buttons
                    self.focused_index += 1
                elif self.focused_index == 3:  # Sound on button
                    self.focused_index = 4  # Sound off button
                self.update_focus()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.handle_button_activation()
        
        # Handle button clicks
        for i, btn in enumerate(self.focusable_items):
            if btn.handle_event(event):
                self.focused_index = i
                self.update_focus()
                return self.handle_button_activation()
        
        return None
    
    def handle_button_activation(self):
        """Handle button activation (click or Enter/Space)"""
        if self.focused_index <= 2:  # Difficulty buttons
            self.difficulty_index = self.focused_index
            self.settings['difficulty'] = self.difficulty_options[self.difficulty_index]
            self.update_button_states()
            return "settings_changed"
        elif self.focused_index == 3:  # Sound on
            self.settings['sound_enabled'] = True
            self.update_button_states()
            return "settings_changed"
        elif self.focused_index == 4:  # Sound off
            self.settings['sound_enabled'] = False
            self.update_button_states()
            return "settings_changed"
        elif self.focused_index == 5:  # Back button
            return "back"
        
        return None
    
    def update(self):
        """Update animations and states"""
        for btn in self.focusable_items:
            btn.update()
    
    def draw(self):
        """Draw the settings menu"""
        # Clear screen
        self.screen.fill((255, 255, 255))
        
        # Draw title
        self.title.draw(self.screen)
        
        # Draw labels
        self.difficulty_label.draw(self.screen)
        self.sound_label.draw(self.screen)
        
        # Draw buttons
        for btn in self.focusable_items:
            btn.draw(self.screen)
        
        # Draw some decorative elements
        pygame.draw.line(self.screen, (229, 231, 235), (40, 130), (self.width - 40, 130), 2)
        pygame.draw.line(self.screen, (229, 231, 235), (40, 320), (self.width - 40, 320), 2)