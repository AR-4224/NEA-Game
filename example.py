import random
import pygame

class Entity:
    def __init__(self, image, position, speed):
        self.image = image
        self.rect = image.get_rect(center=position)
        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
        self.speed = speed

    def move(self, delta):
        self.center += self.vector * self.speed * delta
        self.rect.center = self.center


class Player(Entity):
    def __init__(self, image, position):
        super().__init__(image, position, 50)
        self.gun = Gun(300)

class Enemy(Entity):
    def __init__(self, image, position):
        super().__init__(image, position, 60)
        self.alive = True

class Bullet(Entity):
    def __init__(self, image, position, speed, distance):
        super().__init__(image, position, speed)
        self.start = pygame.Vector2(self.center)
        self.distance = distance
        self.alive = True

    def update(self, delta):
        if self.start.distance_to(self.center) > self.distance:
            self.alive = False
        else:
            self.move(delta)

class Gun:
    def __init__(self, firing_rate):
        self.firing_rate = firing_rate
        self.tick = 0

    def shoot(self, ticks):
        if ticks > self.tick + self.firing_rate:
            self.tick = ticks
            return True

        return False

class Camera:
    def __init__(self, area, player):
        self.area = area
        self.enemies = []
        self.bullets = []
        self.player = player
        self.center = pygame.Vector2(area.center)

    def get_position(self, entity):
        return (entity.rect.centerx - self.area.x,
                entity.rect.centery - self.area.y)

    def draw(self, surface):
        surface.blit(self.player.image, self.player.rect)
        for enemy in self.enemies:
            print("pos:",enemy.center)
            print("camera pos:",self.get_position(enemy))
            surface.blit(enemy.image, self.get_position(enemy))

        for bullet in self.bullets:
            surface.blit(bullet.image, self.get_position(bullet))

    def update(self, delta, keys):
        self.update_keys(delta, keys)
        bullets = []

        for bullet in self.bullets:
            if bullet.alive:
                bullet.update(delta)
                bullets.append(bullet)

        self.bullets = bullets

    def update_keys(self, delta, keys):
        direction = pygame.Vector2()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1

        if direction != pygame.Vector2():
            direction.normalize_ip()
            self.center += direction * self.player.speed * delta
            self.area.center = self.center

class ImageHandler:
    def __init__(self):
        self.player = self.simple_image((30, 30), 'dodgerblue')
        self.enemy = self.simple_image((10, 10), 'firebrick')
        self.bullet = self.simple_image((6, 2), 'lawngreen')

    def simple_image(self, size, color):
        image = pygame.Surface(size, pygame.SRCALPHA)
        image.fill(color)
        return image

def main():
    pygame.display.set_caption("Example")
    surface = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    rect = surface.get_rect()
    running = True
    delta = 0
    fps = 60

    # Variables
    image = ImageHandler()
    player = Player(image.player, rect.center)
    camera = Camera(rect, player)
    rnd = random.randint
    for i in range(4):
        pos = rnd(rect.left, rect.right), rnd(rect.top, rect.bottom)
        enemy = Enemy(image.enemy, pos)
        camera.enemies.append(enemy)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Logic
        ticks = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        mpos = pygame.mouse.get_pos()
        mpressed = pygame.mouse.get_pressed()

        camera.update(delta, keys)
        if keys[pygame.K_SPACE] or mpressed[0]:
            if player.gun.shoot(ticks):
                vector = (mpos - player.center).normalize()
                position = player.center + camera.area.topleft + vector * 10
                # Second value from vector is the angle
                angle = vector.as_polar()[1]
                # Since coords are in topleft. You use -angle.
                b_image = pygame.transform.rotate(image.bullet, -angle)
                bullet = Bullet(b_image, position, 120, 150)
                bullet.vector = vector
                camera.bullets.append(bullet)

        # Draw
        surface.fill('black')
        camera.draw(surface)
        pygame.display.flip()
        delta = clock.tick(fps) * 0.001

pygame.init()
main()
pygame.quit()