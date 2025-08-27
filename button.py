import pygame


class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.pos = pygame.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, screen):
        screen.blit(self.image, self.rect)  # draws object onto screen

    def CheckForInput(self, position):
        # checks if the player has clicked the object or not
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
