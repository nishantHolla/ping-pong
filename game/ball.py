import pygame
import random
import os

# Load sound effects
paddle_hit_sound = pygame.mixer.Sound(
    os.path.join("assets", "sounds", "paddle_hit.wav")
)
wall_bounce_sound = pygame.mixer.Sound(
    os.path.join("assets", "sounds", "wall_bounce.wav")
)
score_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "score.wav"))


class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, player=None, ai=None):
        # Update ball position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            wall_bounce_sound.play()

        # Check paddle collisions immediately after movement
        if player and self.rect().colliderect(player.rect()):
            self.x = player.x + player.width  # prevent overlap
            self.velocity_x *= -1
            paddle_hit_sound.play()
        elif ai and self.rect().colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x *= -1
            paddle_hit_sound.play()

    def check_collision(self, player, ai):
        if self.rect().colliderect(player.rect()) or self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1

    def reset(self, play_score_sound=False):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

        if play_score_sound:
            score_sound.play()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
