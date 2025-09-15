"""
Game Over Screen for Classroom Chaos
"""
import pygame
from src.ui.components import Button, Label

class GameOverScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Colors
        self.primary_color = (238, 108, 43)  # #ee6c2b
        self.text_color = (24, 19, 17)  # #181311
        self.secondary_button_color = (244, 242, 240)  # #f4f2f0
        
        # Game state
        self.score = 0
        
        # UI Components
        self.title = Label(width // 2, 120, "Game Over!", 48, self.text_color, center=True)
        self.score_label = Label(width // 2, 180, f"Final Score: {self.score}", 32, self.text_color, center=True)
        self.message_label = Label(width // 2, 220, "Great job in the classroom chaos!", 18, (107, 114, 128), center=True)
        
        # Buttons
        button_width = width - 80
        button_height = 56
        button_x = 40
        
        self.play_again_btn = Button(button_x, 300, button_width, button_height, 
                                    "Play Again", self.primary_color, (255, 255, 255), 20)
        self.main_menu_btn = Button(button_x, 370, button_width, button_height, 
                                   "Main Menu", self.secondary_button_color, self.text_color, 20)
        
        # Focus management
        self.focusable_items = [self.play_again_btn, self.main_menu_btn]
        self.focused_index = 0
        self.update_focus()
    
    def set_score(self, score):
        """Set the final score to display"""
        self.score = score
        self.score_label.set_text(f"Final Score: {score}")
        
        # Update message based on score
        if score >= 200:
            message = "Excellent! You're a classroom legend!"
        elif score >= 100:
            message = "Great job! The class is impressed!"
        elif score >= 50:
            message = "Not bad! Keep practicing your aim!"
        else:
            message = "Better luck next time!"
        
        self.message_label.set_text(message)
    
    def update_focus(self):
        """Update focus state of UI elements"""
        for i, item in enumerate(self.focusable_items):
            item.is_focused = (i == self.focused_index)
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.focused_index = (self.focused_index - 1) % len(self.focusable_items)
                self.update_focus()
            elif event.key == pygame.K_DOWN:
                self.focused_index = (self.focused_index + 1) % len(self.focusable_items)
                self.update_focus()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.focused_index == 0:
                    return "play_again"
                elif self.focused_index == 1:
                    return "main_menu"
        
        # Handle button clicks
        if self.play_again_btn.handle_event(event):
            return "play_again"
        elif self.main_menu_btn.handle_event(event):
            return "main_menu"
        
        return None
    
    def update(self):
        """Update animations and states"""
        for btn in self.focusable_items:
            btn.update()
    
    def draw(self):
        """Draw the game over screen"""
        # Clear screen with gradient background
        self.screen.fill((240, 248, 255))  # Light background
        
        # Draw decorative elements
        self.draw_background_decoration()
        
        # Draw main content
        self.title.draw(self.screen)
        self.score_label.draw(self.screen)
        self.message_label.draw(self.screen)
        
        # Draw buttons
        for btn in self.focusable_items:
            btn.draw(self.screen)
        
        # Draw some stats if desired
        self.draw_additional_info()
    
    def draw_background_decoration(self):
        """Draw decorative background elements"""
        # Draw some floating books and pens
        import math
        import time
        
        current_time = time.time()
        
        for i in range(5):
            # Floating books
            x = 50 + i * 80
            y = 50 + math.sin(current_time + i) * 10
            book_rect = pygame.Rect(x, y, 20, 15)
            pygame.draw.rect(self.screen, (200, 100, 50), book_rect, border_radius=2)
            
            # Floating pens
            pen_x = 70 + i * 80
            pen_y = 500 + math.cos(current_time + i * 0.5) * 15
            pygame.draw.circle(self.screen, (50, 50, 200), (int(pen_x), int(pen_y)), 4)
    
    def draw_additional_info(self):
        """Draw additional score information"""
        # Draw a semi-transparent info box
        info_rect = pygame.Rect(40, 450, self.width - 80, 80)
        info_surface = pygame.Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
        info_surface.fill((255, 255, 255, 200))
        pygame.draw.rect(info_surface, (238, 108, 43), info_surface.get_rect(), width=2, border_radius=8)
        self.screen.blit(info_surface, info_rect)
        
        # Draw score breakdown
        font = pygame.font.Font(None, 18)
        tips = [
            "💡 Tip: Books give more points than pens!",
            "🎯 Tip: Build streaks for bonus multipliers!",
            "⚡ Tip: Adjust difficulty in settings!"
        ]
        
        for i, tip in enumerate(tips):
            if i == 0 or self.score > 20:  # Show more tips for better players
                tip_surface = font.render(tip, True, (24, 19, 17))
                tip_rect = tip_surface.get_rect(center=(self.width // 2, 470 + i * 20))
                self.screen.blit(tip_surface, tip_rect)
                if i >= 0:  # Show only first tip for now
                    break