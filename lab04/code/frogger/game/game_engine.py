"""
GameEngine: owns the frog and all vehicles, and runs one frame's worth
of game logic.
"""

import random

import pygame

from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS,
    GRID_ROWS,
    GOAL_ROW,
    ROAD_ROWS,
    START_ROW,
    CELL_SIZE,
    WIDTH,
    HEIGHT,
)

LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]

# Task 2
INITIAL_LIVES = 3

# Task 3
GOAL_SCORE = 100

# Task 4
ATTEMPT_TIME = 30


class GameEngine:
    def __init__(self):
        # Task 2: lives
        self.lives = INITIAL_LIVES

        # Task 3: score and win state
        self.score = 0
        self.won = False

        # Task 4: timer and game-over state
        self.game_over = False
        self.time_remaining = ATTEMPT_TIME
        self.attempt_start_time = pygame.time.get_ticks()

        self._build_entities()

    def _build_entities(self):
        start_col = GRID_COLS // 2

        self.frog = Frog(
            col=start_col,
            row=START_ROW,
            start_col=start_col,
            start_row=START_ROW,
            cols=GRID_COLS,
            start_row_limit=START_ROW,
        )

        frog_x_range = (
            start_col * CELL_SIZE,
            start_col * CELL_SIZE + CELL_SIZE,
        )

        self.vehicles = []

        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]

            vehicle_width = 40 if i % 2 == 0 else 70
            spacing = 300
            count = 2

            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)

                positions = []
                safe = True

                for n in range(count):
                    offset = phase + n * spacing

                    x = (
                        offset
                        if speed > 0
                        else WIDTH - offset - vehicle_width
                    )

                    positions.append(x)

                    if not (
                        x + vehicle_width <= frog_x_range[0]
                        or x >= frog_x_range[1]
                    ):
                        safe = False

                if safe:
                    break

            for x in positions:
                self.vehicles.append(
                    Vehicle(
                        x=x,
                        row=row,
                        width=vehicle_width,
                        height=CELL_SIZE - 8,
                        speed=speed,
                    )
                )

    # Task 4
    def _reset_attempt_timer(self):
        self.time_remaining = ATTEMPT_TIME
        self.attempt_start_time = pygame.time.get_ticks()

    # Task 2 + Task 4
    def _lose_attempt(self):
        self.lives -= 1

        # Respawn frog at original position.
        self.frog.reset()

        # Never allow negative lives.
        if self.lives <= 0:
            self.lives = 0
            self.game_over = True
            return

        # Reset timer for the next attempt.
        self._reset_attempt_timer()

    def handle_keydown(self, key):
        # R completely restarts the game.
        if key == pygame.K_r:
            self.lives = INITIAL_LIVES
            self.score = 0
            self.won = False

            self.game_over = False

            self.time_remaining = ATTEMPT_TIME
            self.attempt_start_time = pygame.time.get_ticks()

            self._build_entities()

            return

        # Do not allow movement after winning or losing.
        if self.won or self.game_over:
            return

        if key == pygame.K_UP:
            self.frog.move(0, -1)

        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)

        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)

        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)

    def update(self):
        # Game stops after win or Game Over.
        if self.won or self.game_over:
            return

        # -------------------------
        # Task 4: Timer
        # -------------------------

        current_time = pygame.time.get_ticks()

        elapsed_seconds = (
            current_time - self.attempt_start_time
        ) / 1000.0

        self.time_remaining = max(
            0,
            ATTEMPT_TIME - elapsed_seconds,
        )

        # Timer reached zero.
        if self.time_remaining <= 0:
            self._lose_attempt()
            return

        # -------------------------
        # Vehicle movement
        # -------------------------

        for v in self.vehicles:
            v.update(road_width_px=WIDTH)

        # -------------------------
        # Task 1 + Task 2:
        # Rectangle collision + lives
        # -------------------------

        if check_collision(self.frog, self.vehicles):
            self.lives -= 1

            # Respawn immediately.
            self.frog.reset()

            # Prevent negative lives.
            if self.lives <= 0:
                self.lives = 0
                self.game_over = True
                return

            # Reset timer after losing a life.
            self._reset_attempt_timer()

            return

        # -------------------------
        # Task 3: Goal / Score
        # -------------------------

        if self.frog.row == GOAL_ROW:
            self.score += GOAL_SCORE
            self.won = True
            return

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.frog,
            self.vehicles,
        )

        # Task 2: Lives
        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 10),
        )

        # Task 3: Score
        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 35),
        )

        # Task 4: Timer
        renderer.draw_text(
            surface,
            font,
            f"Time: {int(self.time_remaining)}",
            (10, 60),
        )

        renderer.draw_text(
            surface,
            font,
            "Arrow keys to move. R to restart.",
            (10, HEIGHT - 24),
        )

        # Task 3: Win
        if self.won:
            renderer.draw_banner(
                surface,
                font,
                "YOU WIN!",
            )

        # Task 4: Game Over
        elif self.game_over:
            renderer.draw_banner(
                surface,
                font,
                "GAME OVER",
            )