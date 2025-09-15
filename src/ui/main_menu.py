"""
Main Menu Screen for Classroom Chaos
"""
import pygame
import requests
import os
from src.ui.components import Button, IconButton, Label, NavBar

class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Colors
        self.primary_color = (238, 108, 43)  # #ee6c2b
        self.text_color = (24, 19, 17)  # #181311
        self.gray_color = (107, 114, 128)  # gray-500
        self.secondary_button_color = (244, 242, 240)  # #f4f2f0
        
        # UI Components
        self.leaderboard_btn = IconButton(50, 70, 20, "📊")
        self.store_btn = IconButton(width - 50, 70, 20, "🏪")
        self.class_title = Label(width // 2, 70, "9 Anadolu B", 20, self.text_color, center=True)
        
        self.game_title = Label(width // 2, 150, "Classroom Chaos", 48, self.text_color, center=True)
        self.subtitle = Label(width // 2, 190, "The ultimate book and pen throwing showdown!", 16, self.gray_color, center=True)
        
        # Buttons
        button_width = width - 80
        button_height = 56
        button_x = 40
        
        self.play_btn = Button(button_x, 380, button_width, button_height, 
                              "Play", self.primary_color, (255, 255, 255), 20)
        self.settings_btn = Button(button_x, 450, button_width, button_height, 
                                  "Settings", self.secondary_button_color, self.text_color, 20)
        
        # Navigation
        self.navbar = NavBar(height - 60, width, 60)
        
        # Focus management
        self.focusable_items = [self.leaderboard_btn, self.store_btn, self.play_btn, self.settings_btn]
        self.focused_index = 2  # Start with Play button focused
        self.update_focus()
        
        # Banner image
        self.banner_image = None
        self.banner_rect = pygame.Rect(40, 220, width - 80, 140)
        self.load_banner_image()
        
    def load_banner_image(self):
        """Load banner image from URL or use placeholder"""
        image_path = "/home/runner/work/KitapFirlat/KitapFirlat/assets/banner.png"
        
        # Try to load cached image first
        if os.path.exists(image_path):
            try:
                self.banner_image = pygame.image.load(image_path)
                self.banner_image = pygame.transform.scale(self.banner_image, (self.banner_rect.width, self.banner_rect.height))
                return
            except:
                pass
        
        # Try to download image
        try:
            url = "https://lh3.googleusercontent.com/aida-public/AB6AXuCLGl_8ZvHt0ObEiTCfukQSkIsadgKSbvBuczBsT3mTyVmbrfCpZySwnEOa3S2XwmlPaLnbPDzm1Eb8qOybhmLVaZo-7-7QXoI2Gk3QoNF2LFw3q0xPY8Ea9RDDiKcdfo1mROJ_pMepmFbQb9D_7B_BBhqQVB-G6CxfcnSgxhTchr1WXhPNCo3jv0J8MxrBruB889-SRWN1njGqIhTHMwjqSfBIcGtLlpXRmVHwn4ezIuek6ffWCfEbFmT_NxS3UzeIONbTWfTQ_uM"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            # Save image to assets
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            # Load the saved image
            self.banner_image = pygame.image.load(image_path)
            self.banner_image = pygame.transform.scale(self.banner_image, (self.banner_rect.width, self.banner_rect.height))
        except:
            # Create placeholder image
            self.create_placeholder_banner()
    
    def create_placeholder_banner(self):
        """Create a simple placeholder banner"""
        self.banner_image = pygame.Surface((self.banner_rect.width, self.banner_rect.height))
        self.banner_image.fill((200, 200, 255))  # Light blue background
        
        # Draw some simple shapes to represent classroom scene
        pygame.draw.rect(self.banner_image, (139, 69, 19), (20, 80, 60, 40))  # Desk
        pygame.draw.rect(self.banner_image, (255, 255, 255), (30, 70, 40, 10))  # Paper
        pygame.draw.circle(self.banner_image, (255, 100, 100), (200, 60), 15)  # Book
        pygame.draw.circle(self.banner_image, (100, 100, 255), (250, 80), 8)   # Pen
        
        # Add title text
        font = pygame.font.Font(None, 24)
        text = font.render("Classroom Scene", True, (50, 50, 50))
        text_rect = text.get_rect(center=(self.banner_rect.width // 2, 30))
        self.banner_image.blit(text, text_rect)
    
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
                if self.focused_index == 2:  # Play button
                    return "play"
                elif self.focused_index == 3:  # Settings button
                    return "settings"
        
        # Handle button clicks
        if self.leaderboard_btn.handle_event(event):
            # Could implement leaderboard functionality
            pass
        elif self.store_btn.handle_event(event):
            # Could implement store functionality
            pass
        elif self.play_btn.handle_event(event):
            return "play"
        elif self.settings_btn.handle_event(event):
            return "settings"
        
        # Handle navbar
        self.navbar.handle_event(event)
        
        return None
    
    def update(self):
        """Update animations and states"""
        self.game_title.update(bounce=True)
        self.play_btn.update()
        self.settings_btn.update()
    
    def draw(self):
        """Draw the main menu"""
        # Clear screen
        self.screen.fill((255, 255, 255))
        
        # Draw header
        header_rect = pygame.Rect(0, 0, self.width, 100)
        pygame.draw.rect(self.screen, (255, 255, 255), header_rect)
        
        # Draw header shadow
        pygame.draw.line(self.screen, (229, 231, 235), (0, 100), (self.width, 100), 2)
        
        # Draw header components
        self.leaderboard_btn.draw(self.screen)
        self.store_btn.draw(self.screen)
        self.class_title.draw(self.screen)
        
        # Draw title and subtitle
        self.game_title.draw(self.screen)
        self.subtitle.draw(self.screen)
        
        # Draw banner with rounded corners and shadow
        shadow_rect = self.banner_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, (0, 0, 0, 30), shadow_rect, border_radius=16)
        
        pygame.draw.rect(self.screen, (255, 255, 255), self.banner_rect, border_radius=16)
        
        if self.banner_image:
            # Create a mask for rounded corners
            mask_surface = pygame.Surface((self.banner_rect.width, self.banner_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(mask_surface, (255, 255, 255, 255), mask_surface.get_rect(), border_radius=16)
            
            # Apply the banner image
            banner_surface = self.banner_image.copy()
            banner_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
            self.screen.blit(banner_surface, self.banner_rect)
        
        # Draw buttons
        self.play_btn.draw(self.screen)
        self.settings_btn.draw(self.screen)
        
        # Draw navbar
        self.navbar.draw(self.screen)