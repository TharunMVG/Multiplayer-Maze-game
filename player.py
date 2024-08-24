import pygame
from network import Network


treasure_pos = (300, 300)

class Player:
    def __init__(self, x, y, width, height, color, maze):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.maze = maze
        self.vel = 1
        self.treasure_rect = pygame.Rect(treasure_pos[0], treasure_pos[1], 10, 10)  # Create a rect for treasure

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        new_x = self.x
        new_y = self.y

        if keys[pygame.K_LEFT]:
            new_x -= self.vel
        if keys[pygame.K_RIGHT]:
            new_x += self.vel
        if keys[pygame.K_UP]:
            new_y -= self.vel
        if keys[pygame.K_DOWN]:
            new_y += self.vel

        # Check for collision with maze walls
        if self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
        self.update()

    def check_collision(self, new_x, new_y):
        # Calculate the player's new rectangle
        new_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        # Check for collision with each wall in the maze
        for row_index, row in enumerate(self.maze):
            for col_index, tile in enumerate(row):
                if tile == "#":
                    wall_rect = pygame.Rect(col_index * 40, row_index * 40, 40, 40)
                    if new_rect.colliderect(wall_rect):
                        return False  # Collision detected
        return True  # No collision detected
     
    def check_treasure_collision(self):
        # Check if the player's rectangle collides with the treasure's rectangle
        return self.rect.colliderect(self.treasure_rect)
    

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.check_treasure_collision():
            return True  # Player has reached the treasure
        return False
     



