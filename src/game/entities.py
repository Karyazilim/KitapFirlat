"""
Game entities for Classroom Chaos
"""
import pygame
import math
import random

class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 150, 200)  # Blue player
        self.aim_angle = -math.pi / 2  # Start aiming up
        self.aim_line_length = 60
        
    def update_aim(self, mouse_pos):
        """Update aim direction based on mouse position"""
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.aim_angle = math.atan2(dy, dx)
    
    def get_launch_velocity(self, power=15):
        """Get launch velocity vector based on current aim"""
        vx = math.cos(self.aim_angle) * power
        vy = math.sin(self.aim_angle) * power
        return (vx, vy)
    
    def draw(self, screen):
        """Draw the player and aim indicator"""
        # Draw player as simple rectangle
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        
        # Draw aim line
        end_x = self.rect.centerx + math.cos(self.aim_angle) * self.aim_line_length
        end_y = self.rect.centery + math.sin(self.aim_angle) * self.aim_line_length
        pygame.draw.line(screen, (255, 100, 100), self.rect.center, (end_x, end_y), 3)

class Projectile:
    def __init__(self, x, y, vx, vy, projectile_type="book"):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.projectile_type = projectile_type
        self.radius = 8 if projectile_type == "book" else 4
        self.color = (200, 100, 50) if projectile_type == "book" else (50, 50, 200)
        self.gravity = 0.3
        self.active = True
        
    def update(self):
        """Update projectile physics"""
        if not self.active:
            return
            
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity  # Apply gravity
        
        # Remove if off screen
        if self.y > 900 or self.x < -50 or self.x > 500:
            self.active = False
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def draw(self, screen):
        """Draw the projectile"""
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Target:
    def __init__(self, x, y, target_type="student"):
        self.x = float(x)
        self.y = float(y)
        self.target_type = target_type
        self.width = 30
        self.height = 40
        self.speed = random.uniform(1, 3)
        self.direction = random.choice([-1, 1])
        self.color = (150, 200, 150) if target_type == "student" else (200, 150, 150)
        self.active = True
        self.hit_timer = 0
        
    def update(self, screen_width):
        """Update target movement"""
        if not self.active:
            if self.hit_timer > 0:
                self.hit_timer -= 1
            return
            
        self.x += self.speed * self.direction
        
        # Bounce off screen edges
        if self.x <= 0 or self.x >= screen_width - self.width:
            self.direction *= -1
            self.x = max(0, min(screen_width - self.width, self.x))
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def hit(self):
        """Mark target as hit"""
        self.active = False
        self.hit_timer = 30  # Show hit effect for 30 frames
    
    def draw(self, screen):
        """Draw the target"""
        if self.active:
            pygame.draw.rect(screen, self.color, self.get_rect(), border_radius=5)
            # Draw simple face
            eye_size = 3
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 8), int(self.y + 10)), eye_size)
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 22), int(self.y + 10)), eye_size)
        elif self.hit_timer > 0:
            # Draw hit effect
            alpha = int(255 * (self.hit_timer / 30))
            hit_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            hit_surface.fill((255, 255, 0, alpha))
            screen.blit(hit_surface, (self.x, self.y))

class TargetSpawner:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_timer = 0
        self.spawn_delay = 120  # Spawn every 2 seconds at 60 FPS
        self.targets = []
        self.difficulty_multiplier = 1.0
        
    def set_difficulty(self, difficulty):
        """Set spawning difficulty"""
        if difficulty == "Easy":
            self.spawn_delay = 180
            self.difficulty_multiplier = 0.7
        elif difficulty == "Normal":
            self.spawn_delay = 120
            self.difficulty_multiplier = 1.0
        elif difficulty == "Hard":
            self.spawn_delay = 60
            self.difficulty_multiplier = 1.5
    
    def update(self):
        """Update spawner and targets"""
        self.spawn_timer += 1
        
        # Spawn new target
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            self.spawn_target()
        
        # Update existing targets
        for target in self.targets[:]:
            target.update(self.screen_width)
            if not target.active and target.hit_timer <= 0:
                self.targets.remove(target)
    
    def spawn_target(self):
        """Spawn a new target"""
        if len(self.targets) < 5:  # Limit number of targets
            x = random.randint(0, self.screen_width - 30)
            y = random.randint(50, 200)  # Upper portion of screen
            target = Target(x, y)
            target.speed *= self.difficulty_multiplier
            self.targets.append(target)
    
    def check_collisions(self, projectiles):
        """Check for collisions between projectiles and targets"""
        hits = []
        for projectile in projectiles:
            if not projectile.active:
                continue
                
            for target in self.targets:
                if not target.active:
                    continue
                    
                if projectile.get_rect().colliderect(target.get_rect()):
                    projectile.active = False
                    target.hit()
                    score = 10 if projectile.projectile_type == "book" else 5
                    hits.append({
                        'score': score,
                        'type': projectile.projectile_type,
                        'target': target
                    })
        
        return hits
    
    def draw(self, screen):
        """Draw all targets"""
        for target in self.targets:
            target.draw(screen)