"""
Main Game Screen for Classroom Chaos
"""
import pygame
import time
from src.game.entities import Player, Projectile, TargetSpawner
from src.ui.components import Label

class GameScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Colors
        self.bg_color = (220, 240, 255)  # Light blue sky
        self.ground_color = (139, 69, 19)  # Brown ground
        
        # Game entities
        player_width, player_height = 40, 30
        player_x = width // 2 - player_width // 2
        player_y = height - 150
        self.player = Player(player_x, player_y, player_width, player_height)
        
        self.projectiles = []
        self.target_spawner = TargetSpawner(width, height)
        
        # Game state
        self.score = 0
        self.streak = 0
        self.max_streak = 0
        self.time_remaining = 60.0
        self.game_active = True
        self.settings = {'difficulty': 'Normal', 'sound_enabled': True}
        
        # UI elements
        self.score_label = Label(20, 20, f"Score: {self.score}", 24, (255, 255, 255))
        self.streak_label = Label(20, 50, f"Streak: {self.streak}", 18, (255, 255, 255))
        self.time_label = Label(width - 120, 20, f"Time: {int(self.time_remaining)}", 24, (255, 255, 255))
        
        # Instructions
        self.instruction_labels = [
            Label(width // 2, height - 100, "Left Click: Throw Book (+10 pts)", 16, (255, 255, 255), center=True),
            Label(width // 2, height - 80, "Right Click: Throw Pen (+5 pts)", 16, (255, 255, 255), center=True),
            Label(width // 2, height - 60, "ESC: Back to Menu", 16, (255, 255, 255), center=True)
        ]
        
        # Initialize based on settings
        self.target_spawner.set_difficulty(self.settings['difficulty'])
    
    def reset(self):
        """Reset game to initial state"""
        self.score = 0
        self.streak = 0
        self.time_remaining = 60.0
        self.game_active = True
        self.projectiles.clear()
        self.target_spawner.targets.clear()
        self.target_spawner.spawn_timer = 0
        self.update_ui()
    
    def update_settings(self, settings):
        """Update game settings"""
        self.settings = settings
        self.target_spawner.set_difficulty(settings['difficulty'])
    
    def get_score(self):
        """Get current score"""
        return self.score
    
    def update_ui(self):
        """Update UI labels"""
        self.score_label.set_text(f"Score: {self.score}")
        self.streak_label.set_text(f"Streak: {self.streak} (Best: {self.max_streak})")
        self.time_label.set_text(f"Time: {int(self.time_remaining)}")
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back_to_menu"
        
        if not self.game_active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click - throw book
                self.throw_projectile("book")
            elif event.button == 3:  # Right click - throw pen
                self.throw_projectile("pen")
        
        return None
    
    def throw_projectile(self, projectile_type):
        """Throw a projectile"""
        vx, vy = self.player.get_launch_velocity()
        projectile = Projectile(
            self.player.rect.centerx,
            self.player.rect.centery,
            vx, vy, projectile_type
        )
        self.projectiles.append(projectile)
    
    def update(self):
        """Update game state"""
        if not self.game_active:
            return
        
        # Update timer
        self.time_remaining -= 1/60  # Assuming 60 FPS
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.game_active = False
            return "game_over"
        
        # Update player aim
        mouse_pos = pygame.mouse.get_pos()
        self.player.update_aim(mouse_pos)
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.active:
                self.projectiles.remove(projectile)
        
        # Update targets
        self.target_spawner.update()
        
        # Check collisions
        hits = self.target_spawner.check_collisions(self.projectiles)
        for hit in hits:
            base_score = hit['score']
            # Apply streak multiplier (max 3x)
            multiplier = min(1 + self.streak * 0.1, 3.0)
            final_score = int(base_score * multiplier)
            
            self.score += final_score
            self.streak += 1
            self.max_streak = max(self.max_streak, self.streak)
        
        # Reset streak if no hits recently (could be improved with a timer)
        if not hits and len(self.projectiles) == 0:
            # Only reset streak when no projectiles are active
            pass  # Keep streak for now, could add timer-based reset
        
        self.update_ui()
        
        return None
    
    def draw(self):
        """Draw the game screen"""
        # Draw background
        self.screen.fill(self.bg_color)
        
        # Draw ground
        ground_height = 120
        ground_rect = pygame.Rect(0, self.height - ground_height, self.width, ground_height)
        pygame.draw.rect(self.screen, self.ground_color, ground_rect)
        
        # Draw some classroom elements
        self.draw_classroom_background()
        
        # Draw game entities
        self.player.draw(self.screen)
        
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        
        self.target_spawner.draw(self.screen)
        
        # Draw UI
        self.score_label.draw(self.screen)
        self.streak_label.draw(self.screen)
        self.time_label.draw(self.screen)
        
        # Draw instructions
        for label in self.instruction_labels:
            label.draw(self.screen)
        
        # Draw game over overlay if needed
        if not self.game_active:
            self.draw_game_over_overlay()
    
    def draw_classroom_background(self):
        """Draw simple classroom background elements"""
        # Draw blackboard
        board_rect = pygame.Rect(50, 50, self.width - 100, 80)
        pygame.draw.rect(self.screen, (40, 40, 40), board_rect, border_radius=5)
        pygame.draw.rect(self.screen, (60, 60, 60), board_rect, width=3, border_radius=5)
        
        # Draw some desks
        desk_color = (139, 89, 42)
        for i in range(3):
            x = 80 + i * 100
            y = self.height - 200
            desk_rect = pygame.Rect(x, y, 60, 30)
            pygame.draw.rect(self.screen, desk_color, desk_rect, border_radius=3)
    
    def draw_game_over_overlay(self):
        """Draw game over overlay"""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Time's Up!", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Final score
        score_font = pygame.font.Font(None, 32)
        score_text = score_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(score_text, score_rect)
        
        # Instructions
        inst_font = pygame.font.Font(None, 24)
        inst_text = inst_font.render("Press ESC for menu", True, (255, 255, 255))
        inst_rect = inst_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(inst_text, inst_rect)