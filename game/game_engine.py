import os
import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)


class GameEngine:
    def __init__(self, width, height):
        # Game geometry
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Game objects
        self.player = Paddle(
            10, height // 2 - 50, self.paddle_width, self.paddle_height
        )
        self.ai = Paddle(
            width - 20, height // 2 - 50, self.paddle_width, self.paddle_height
        )
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # Game values
        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5
        self.running = True

        self.winner_text = None
        self.PLAYER_WON_TEXT = "Player wins!"
        self.AI_WON_TEXT = "AI wins!"

        self.options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit",
        ]

        # Game states
        self.PLAYING_STATE = "playing"
        self.GAME_OVER_STATE = "game_over"
        self.state = self.PLAYING_STATE

        # Game fonts
        self.font = pygame.font.SysFont("Arial", 30)

        # Load sound effects
        self.paddle_hit_sound = pygame.mixer.Sound(
            os.path.join("assets", "sounds", "paddle_hit.wav")
        )
        self.wall_bounce_sound = pygame.mixer.Sound(
            os.path.join("assets", "sounds", "wall_bounce.wav")
        )
        self.score_sound = pygame.mixer.Sound(
            os.path.join("assets", "sounds", "score.wav")
        )

    def is_running(self):
        return self.running

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.state == self.GAME_OVER_STATE:
                    self.running = False
                    return

                elif event.key == pygame.K_3 and self.state == self.GAME_OVER_STATE:
                    self.target_score = 2
                    self.reset_game()

                elif event.key == pygame.K_5 and self.state == self.GAME_OVER_STATE:
                    self.target_score = 3
                    self.reset_game()

                elif event.key == pygame.K_7 and self.state == self.GAME_OVER_STATE:
                    self.target_score = 4
                    self.reset_game()

    def handle_input(self):
        if self.state != self.PLAYING_STATE:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.state != self.PLAYING_STATE:
            return

        self.ball.move(
            self.player,
            self.ai,
            wall_bounce_sound=self.wall_bounce_sound,
            paddle_hit_sound=self.paddle_hit_sound,
        )

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset(score_sound=self.score_sound)

        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset(score_sound=self.score_sound)

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(
            screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height)
        )

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        if self.state == self.GAME_OVER_STATE and self.winner_text:
            text_surface = self.font.render(self.winner_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                center=(self.width // 2, self.height // 2 - 40)
            )
            screen.blit(text_surface, text_rect)

            for i, opt in enumerate(self.options):
                opt_surface = self.font.render(opt, True, (255, 255, 255))
                opt_rect = opt_surface.get_rect(
                    center=(self.width // 2, self.height // 2 + 30 + i * 40)
                )
                screen.blit(opt_surface, opt_rect)

    def check_game_over(self, screen):
        if self.state != self.PLAYING_STATE:
            return

        if self.player_score >= self.target_score or self.ai_score >= self.target_score:
            self.winner_text = (
                self.PLAYER_WON_TEXT
                if self.player_score >= self.target_score
                else self.AI_WON_TEXT
            )
            self.state = self.GAME_OVER_STATE

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset(score_sound=None)
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
        self.state = self.PLAYING_STATE
