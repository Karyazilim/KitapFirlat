"""
Basic UI Components for Classroom Chaos
"""
import pygame
import math

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size=18):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        self.is_focused = False
        self.scale = 1.0
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN:
            if self.is_focused and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                return True
        return False
    
    def update(self):
        # Smooth scaling animation
        target_scale = 1.05 if self.is_hovered else 1.0
        self.scale += (target_scale - self.scale) * 0.2
    
    def draw(self, screen):
        # Calculate scaled rect
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Draw shadow
        shadow_rect = scaled_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=12)
        
        # Draw button
        pygame.draw.rect(screen, self.color, scaled_rect, border_radius=12)
        
        # Draw focus indicator
        if self.is_focused:
            pygame.draw.rect(screen, (238, 108, 43), scaled_rect, width=3, border_radius=12)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)

class IconButton:
    def __init__(self, x, y, radius, icon_text, color=(240, 240, 240)):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.center = (x, y)
        self.radius = radius
        self.icon_text = icon_text
        self.color = color
        self.font = pygame.font.Font(None, 24)
        self.is_hovered = False
        self.is_focused = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN:
            if self.is_focused and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                return True
        return False
    
    def draw(self, screen):
        color = (220, 220, 220) if self.is_hovered else self.color
        
        # Draw shadow
        pygame.draw.circle(screen, (0, 0, 0, 30), (self.center[0] + 2, self.center[1] + 2), self.radius)
        
        # Draw circle
        pygame.draw.circle(screen, color, self.center, self.radius)
        
        # Draw focus indicator
        if self.is_focused:
            pygame.draw.circle(screen, (238, 108, 43), self.center, self.radius, width=3)
        
        # Draw icon text
        text_surface = self.font.render(self.icon_text, True, (107, 114, 128))
        text_rect = text_surface.get_rect(center=self.center)
        screen.blit(text_surface, text_rect)

class Label:
    def __init__(self, x, y, text, font_size=18, color=(24, 19, 17), center=False):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.center = center
        self.bounce_offset = 0
        self.bounce_time = 0
        
    def set_text(self, text):
        self.text = text
    
    def update(self, bounce=False):
        if bounce:
            self.bounce_time += 0.1
            self.bounce_offset = math.sin(self.bounce_time) * 5
    
    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        if self.center:
            text_rect = text_surface.get_rect(center=(self.x, self.y + self.bounce_offset))
            screen.blit(text_surface, text_rect)
        else:
            screen.blit(text_surface, (self.x, self.y + self.bounce_offset))

class NavBar:
    def __init__(self, y, width, height):
        self.y = y
        self.width = width
        self.height = height
        self.items = [
            {"text": "Home", "icon": "🏠", "active": True},
            {"text": "Friends", "icon": "👥", "active": False},
            {"text": "Settings", "icon": "⚙️", "active": False}
        ]
        self.font = pygame.font.Font(None, 12)
        self.focused_item = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.focused_item > 0:
                self.focused_item -= 1
                return True
            elif event.key == pygame.K_RIGHT and self.focused_item < len(self.items) - 1:
                self.focused_item += 1
                return True
        return False
    
    def draw(self, screen):
        # Draw background
        nav_rect = pygame.Rect(0, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 255, 255), nav_rect)
        pygame.draw.line(screen, (229, 231, 235), (0, self.y), (self.width, self.y), 1)
        
        # Draw items
        item_width = self.width // len(self.items)
        for i, item in enumerate(self.items):
            x = i * item_width
            item_rect = pygame.Rect(x, self.y, item_width, self.height)
            
            # Highlight active or focused item
            if item["active"]:
                color = (238, 108, 43)  # Primary color
                bg_color = (255, 237, 213)  # Light orange background
                pygame.draw.rect(screen, bg_color, item_rect, border_radius=8)
            elif i == self.focused_item:
                color = (107, 114, 128)
                bg_color = (243, 244, 246)
                pygame.draw.rect(screen, bg_color, item_rect, border_radius=8)
            else:
                color = (107, 114, 128)
            
            # Draw icon and text
            icon_surface = self.font.render(item["icon"], True, color)
            text_surface = self.font.render(item["text"], True, color)
            
            icon_y = self.y + 8
            text_y = self.y + 28
            
            icon_rect = icon_surface.get_rect(center=(x + item_width // 2, icon_y))
            text_rect = text_surface.get_rect(center=(x + item_width // 2, text_y))
            
            screen.blit(icon_surface, icon_rect)
            screen.blit(text_surface, text_rect)