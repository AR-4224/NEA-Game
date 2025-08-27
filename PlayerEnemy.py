from image import *
import math
import random

#  global variables
clock = pygame.time.Clock()
Max_Health = 100
frames = 0
bullet_list = []
S_bullet_list = []
Item_list = []
Weapon_list = []
Enemy_list = []
Chest_list = []
Boss_list = []
Rooms = []
run = True


#  stack data structure
class Stack:
    def __init__(self, max_size):
        self.stack = []
        self.max_size = max_size

    # checks if stack is empty
    def is_empty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False

    # returns the top value of the stack
    def peek(self):
        return self.stack[len(self.stack) - 1]

    # returns the size of the stack
    def size(self):
        return len(self.stack)

    # adds an item to the stack if it is not full
    def push(self, item):
        if not self.size == self.max_size:
            self.stack.append(item)

    # returns the item of the top of the stack and removes it off the stack
    def pop(self):
        if not self.is_empty():
            item = self.stack[-1]
            self.stack = self.stack[:-1]
            return item

    # empties the stack
    def reset(self):
        self.stack.clear()


# generating enemies for a wave function #

def E_wave():
    NPC = []

    NumOfEnemies = random.randint(9, 11)

    # decides if enemy in wave is a ground type or flying type
    for x in range(NumOfEnemies):
        if random.randint(0, 1) == 1:  # deciding if it's a ground or flying enemy
            enemy = GroundEnemy()
            NPC.append(enemy)
        else:
            enemy = FlyingEnemy()
            NPC.append(enemy)

    return NPC


# generating chests for a room function #

def C_Wave():
    items = []
    NumOfChests = random.randint(1, 4)

    # adds a chest object to the list
    for x in range(NumOfChests):
        items.append(Chest())

    return items


# initialising wave stack for chests and enemy with a max size of 20
ChestWaveStack = Stack(20)
EnemyWaveStack = Stack(20)


# Player class #

class Player:
    def __init__(self):
        self.status_time = 0
        self.pos = pygame.Vector2((1536 // 2, 864 // 2))
        self.image = player_img
        self.rect = self.image.get_rect()
        self.speed = PLAYER_SPEED
        self.health = 100
        self.shield = 0
        self.KeyCount = 2
        self.LevelCount = 1
        self.immunity = True
        self.alive = True
        self.DashCooldown = 0
        self.ShootCooldown = 0
        self.angle = 0
        self.RoomIndex = 0
        self.WeaponType = None

        self.score = 0
        self.EnemiesKilled = 0
        self.BossesKilled = 0
        self.ItemsUsed = 0
        self.FloorsCleared = 0
        self.TotalRuns = 0

        self.Burn = False
        self.Decay = False
        self.Invincible = False
        self.Stun = False

        self.Pellet = True
        self.Flame = False
        self.Cannon = False
        self.Ice = False
        self.Axe = False
        self.Shadow = False

    # manages the cooldowns of the player
    def Cooldowns(self):
        # updating cooldowns
        if self.DashCooldown > 0:
            self.DashCooldown -= 1

        if self.ShootCooldown > 0:
            self.ShootCooldown -= 1

    # manages movement of the player
    def movement(self, Rooms):

        room = Rooms[self.RoomIndex]
        keys = pygame.key.get_pressed()

        velocity_y = 0
        velocity_x = 0

        # movement, and checking that the player cannot go past the borders of the room rect
        if keys[pygame.K_a] and self.rect.left > room.rect.left:
            velocity_x -= self.speed
        if keys[pygame.K_d] and self.rect.right < room.rect.right:
            velocity_x += self.speed
        if keys[pygame.K_w] and self.rect.top > room.rect.top:
            velocity_y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < room.rect.bottom:
            velocity_y += self.speed

        return velocity_x, velocity_y

    def update(self, Rooms):
        room = Rooms[self.RoomIndex]
        global ChestWaveStack, EnemyWaveStack

        # adds the velocity variables from the movement function to pos to move the player, updating their position
        velocity_x, velocity_y = self.movement(Rooms)
        self.pos += (velocity_x, velocity_y)
        self.rect.center = self.pos

        # if the player collides with the door and all enemies are dead then it moves calls the next room function
        if self.rect.colliderect(room.door_rect) and room.EnemiesCleared:
            self.next_room(Rooms)

            # resetting the stacks each time the player enters a new room
            EnemyWaveStack = EnemySpawn(EnemyWaveStack)
            ChestWaveStack = ChestSpawn(ChestWaveStack)

        # runs the update function in bullet class for all bullets in list and their effects if they have any
        for bullet in bullet_list:
            bullet.update()
            bullet.effect()

    def dash(self, Rooms):
        room = Rooms[self.RoomIndex]
        keys = pygame.key.get_pressed()
        velocity_x = 0
        velocity_y = 0
        # dash mechanic will make the player move in that direction instantaneously by 45 pixels
        if keys[pygame.K_a] and keys[pygame.K_LSHIFT] and self.DashCooldown == 0 and self.rect.left > room.rect.left:
            velocity_x -= 45
            self.DashCooldown = 70

        if keys[pygame.K_d] and keys[pygame.K_LSHIFT] and self.DashCooldown == 0 and self.rect.right < room.rect.right:
            velocity_x += 45
            self.DashCooldown = 70

        if keys[pygame.K_w] and keys[pygame.K_LSHIFT] and self.DashCooldown == 0 and self.rect.top > room.rect.top:
            velocity_y -= 45
            self.DashCooldown = 70

        if keys[pygame.K_s] and keys[pygame.K_LSHIFT] and self.DashCooldown == 0 and self.rect.bottom < room.rect.bottom:
            velocity_y += 45
            self.DashCooldown = 70

        self.pos += (velocity_x, velocity_y)
        self.rect.center = self.pos

    # user's health cannot decrease if immunity is true
    def immune(self):
        if self.immunity:
            hero.health -= 0

    def Shooting(self, BulletType):
        if pygame.mouse.get_pressed()[0] and self.ShootCooldown == 0:
            # initialising bullet object
            bullets = BulletType(self.rect.centerx, self.rect.centery, self.angle)
            self.WeaponType = bullets
            # getting mouse position and finding distance of mouse to player
            pos = pygame.mouse.get_pos()
            dist_x = pos[0] - self.rect.midleft[0]
            dist_y = -(pos[1] - self.rect.midleft[1])
            # finding the angle between player and mouse
            self.angle = math.degrees(math.atan2(dist_y, dist_x))
            # adding bullet to list
            bullet_list.append(bullets)
            self.ShootCooldown = bullets.Cooldown

    def next_room(self, Rooms):
        global Item_list
        global Weapon_list

        if self.RoomIndex < len(Rooms):
            room = Rooms[self.RoomIndex]  # initialising room variable from the Rooms parameter
            self.RoomIndex += 1  # increase room index by one
            self.pos = pygame.Vector2((room.rect.left + 50), room.rect.centery)  # moves the player to left of room

        # deleting items not picked up from the game when u move to the next room
        Item_list.clear()
        Weapon_list.clear()

    def draw(self):
        Screen.blit(self.image, self.rect)  # draws the player onto the screen

        for bullet in bullet_list:  # draws all the bullets in the bullet list
            bullet.draw()

    def add_burn(self):
        self.Burn = True
        self.Decay = False
        self.Invincible = False
        self.Stun = False

    def use_burn(self):
        keys = pygame.key.get_pressed()
        if self.Burn:
            if keys[pygame.K_SPACE]:
                for enemy in Enemy_list:
                    enemy.flame()  # runs the flame method in enemy base class
                self.Burn = False
                self.ItemsUsed += 1  # adds to user statistics

    def add_decay(self):
        self.Decay = True
        self.Stun = False
        self.Invincible = False
        self.Burn = False

    def use_decay(self):
        keys = pygame.key.get_pressed()
        if self.Decay:
            if keys[pygame.K_SPACE]:
                for enemy in Enemy_list:
                    enemy.alive = False  # kills all the enemies in a wave
                self.Decay = False
                self.ItemsUsed += 1

    def add_stun(self):
        self.Stun = True
        self.Invincible = False
        self.Burn = False
        self.Decay = False

    def use_stun(self):
        keys = pygame.key.get_pressed()
        if self.Stun:
            if keys[pygame.K_SPACE]:
                self.status_time = pygame.time.get_ticks()
                for enemy in Enemy_list:
                    enemy.speed = 0  # freezes all enemies

                self.Stun = False
                self.ItemsUsed += 1

        if pygame.time.get_ticks() - self.status_time > 1500:
            for enemy in Enemy_list:
                enemy.speed = enemy.original_speed  # after a set amount of time has passed, unfreezes all enemies

    def add_invincibility(self):
        self.Invincible = True
        self.Decay = False
        self.Burn = False
        self.Stun = False

    def use_invincibility(self):
        keys = pygame.key.get_pressed()
        if self.Invincible:
            if keys[pygame.K_SPACE]:
                self.status_time = pygame.time.get_ticks()
                for enemy in Enemy_list:
                    enemy.damage = 0  # sets all enemy damage to 0

                self.Invincible = False
                self.ItemsUsed += 1

        if pygame.time.get_ticks() - self.status_time > 2000:
            for enemy in Enemy_list:
                enemy.damage = enemy.original_damage  # after a set amount of time has passed, restores enemy damage

    def add_pellet(self):
        self.Pellet = True
        self.Cannon = False
        self.Ice = False
        self.Shadow = False
        self.Axe = False
        self.Flame = False

    def use_pellet(self):
        if self.Pellet:
            self.Shooting(Pellet)

    def add_flame(self):
        self.Flame = True
        self.Pellet = False
        self.Cannon = False
        self.Ice = False
        self.Shadow = False
        self.Axe = False

    def use_flame(self):
        if self.Flame:
            self.Shooting(FlameThrower)

    def add_cannon(self):
        self.Cannon = True
        self.Shadow = False
        self.Flame = False
        self.Axe = False
        self.Pellet = False
        self.Ice = False

    def use_cannon(self):
        if self.Cannon:
            self.Shooting(CannonBall)

    def add_ice(self):
        self.Ice = True
        self.Shadow = False
        self.Pellet = False
        self.Axe = False
        self.Flame = False
        self.Cannon = False

    def use_ice(self):
        if self.Ice:
            self.Shooting(Blizzard)

    def add_shadow(self):
        self.Shadow = True
        self.Pellet = False
        self.Ice = False
        self.Axe = False
        self.Flame = False
        self.Cannon = False

    def use_shadow(self):
        if self.Shadow:
            self.Shooting(ShadowBlade)

    def add_axe(self):
        self.Axe = True
        self.Shadow = False
        self.Ice = False
        self.Cannon = False
        self.Flame = False
        self.Pellet = False

    def use_axe(self):
        if self.Axe:
            self.Shooting(BattleAxe)


hero = Player()


# Bullet baseclass #

class Bullet:
    def __init__(self, x, y, angle, speed, image, cooldown, expire, damage):
        self.speed = speed
        self.image = image
        self.Cooldown = cooldown
        self.expire = expire
        self.damage = damage
        self.angle = math.radians(angle)  # converting angle to radians
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.time_shot = pygame.time.get_ticks()
        # calculating horizontal and vertical speeds based off angle using trig
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
        # move bullet
        self.rect.x += self.dx
        self.rect.y += self.dy

        # checking if bullet's time to live has expired or not
        hit_list = []
        for index in bullet_list:
            if pygame.time.get_ticks() - index.time_shot > index.expire:
                hit_list.append(index)

        # if bullet has expired it will be removed from the bullet list, de-spawning it
        for index in hit_list:
            bullet_list.remove(index)

    def draw(self):
        Screen.blit(self.image, self.rect)

    def effect(self):
        pass


# Bullet subclasses #


class Pellet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 10, bullet_img, 8, 1700, 15)


class FlameThrower(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 20, fire_img, 15, 500, 10)

    def effect(self):
        hit = self.rect.collidelistall(Enemy_list)

        for enemy in hit:
            Enemy_list[enemy].burn()


class CannonBall(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 2, CannonBall_img, 40, 1700, 50)


class Blizzard(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 7, SnowBall_img, 10, 1000, 10)

    def effect(self):
        hit = self.rect.collidelistall(Enemy_list)

        for enemy in hit:
            Enemy_list[enemy].speed = Enemy_list[enemy].original_speed * 0.5


class ShadowBlade(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 10, crescent_img, 7, 400, 30)


class BattleAxe(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 5, B_Axe_img, 50, 20000, 120)


# Enemy baseclass #


class Enemy:
    def __init__(self, health, image, speed):
        x = random.randrange(400, 1536)
        y = random.randrange(0, 864)
        self.pos = pygame.math.Vector2((x, y))
        self.knockback = False
        self.immunity = False
        self.alive = True
        self.health = health
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.time_hit = 0
        self.speed = speed
        self.original_speed = speed
        self.damage = 20
        self.original_damage = 20
        self.Burn = False
        self.fire = False
        self.slow = False
        self.status_time = 0

    def collision(self, BulletType):

        # checks if they have collided with player and if player has no shield
        if self.rect.colliderect(hero.rect) and hero.shield == 0:
            self.knockback = True
            if not hero.immunity:
                hero.health -= self.damage  # if hero is not immune they will take damage
            self.immunity = True  # sets immunity to true
            self.time_hit = pygame.time.get_ticks()

        # checks if they have collided with player and if player has shield
        elif self.rect.colliderect(hero.rect) and hero.shield > 0:
            self.knockback = True
            self.time_hit = pygame.time.get_ticks()
            hero.shield -= 1  # reduces shield counter by 1
            if hero.shield < 0:
                hero.shield = 0

        if pygame.time.get_ticks() - self.time_hit > 100:
            self.immunity = False  # after a set amount of time the player will no longer be immune

        if pygame.time.get_ticks() - self.time_hit > 650:
            self.knockback = False  # after a set amount of time the enemy will not be sent backwards

        if self.immunity:
            hero.immunity = True
        else:
            hero.immunity = False

        # checking if enemy has collided with a bullet, and if yes health is reduced by how much damage weapon deals
        collide_hit = self.rect.collidelistall(bullet_list)
        if collide_hit:
            self.health -= BulletType.damage

        # for each bullet that collides with an enemy, it gets removed from list, de-spawning it
        for index in collide_hit:
            bullet_list.remove(bullet_list[index])

    def burn(self):
        self.status_time = pygame.time.get_ticks()
        self.Burn = True

    def flame(self):
        self.status_time = pygame.time.get_ticks()
        self.fire = True

    def check_status(self):
        # if either status effect is true, it will decrease their health by a set amount for a set number of ticks
        if self.Burn:
            self.health -= 0.1
            if pygame.time.get_ticks() - self.status_time > 3000:
                self.Burn = False

        if self.fire:
            self.health -= 0.5
            if pygame.time.get_ticks() - self.status_time > 3000:
                self.fire = False

    def draw(self):
        Screen.blit(self.image, self.rect)

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def drop_item(self):
        global Item_list

        if self.health <= 0 and random.randint(1, 10) == 1:  # chance to drop an item upon death
            Item_list.append(Items(self.pos, random.randint(0, 2)))  # randomly selects what item to add to list


# Enemy subclasses #


class FlyingEnemy(Enemy):
    def __init__(self):
        super().__init__((50 * (hero.LevelCount * 1.6)), bat_img, FLY_SPEED)
        self.alive = True

    def movement(self, position):
        # finding distance between player and flying enemy
        F_distance_x = position[0] - self.pos[0]
        F_distance_y = position[1] - self.pos[1]
        F_distance = (F_distance_x ** 2 + F_distance_y ** 2) ** 0.5  # pythagoras

        # moving flying enemy towards player
        if F_distance != 0:
            if not self.knockback:
                self.pos[0] += self.speed * (F_distance_x / F_distance)
                self.pos[1] += self.speed * (F_distance_y / F_distance)
            else:
                self.pos[0] -= self.speed * (F_distance_x / F_distance)
                self.pos[1] -= self.speed * (F_distance_y / F_distance)

        self.rect.center = self.pos


class GroundEnemy(Enemy):
    def __init__(self):
        super().__init__((75 * (hero.LevelCount * 1.6)), skull_img, GROUND_SPEED)
        self.speed = GROUND_SPEED
        self.alive = True

    def movement(self, position):

        G_distance_x = position[0] - self.pos[0]
        G_distance_y = position[1] - self.pos[1]
        G_distance = (G_distance_x ** 2 + G_distance_y ** 2) ** 0.5  # pythagoras

        # moving ground enemy towards player only if player is within range
        if G_distance < 700:
            if G_distance != 0:
                if not self.knockback:
                    self.pos[0] += self.speed * G_distance_x / G_distance
                    self.pos[1] += self.speed * G_distance_y / G_distance
                else:
                    self.pos[0] -= self.speed * G_distance_x / G_distance
                    self.pos[1] -= self.speed * G_distance_y / G_distance

                self.rect.center = self.pos


# Shadow Boss class #


class ShadowBoss:
    def __init__(self):
        self.alive = True
        room = Rooms[hero.RoomIndex]
        self.pos = pygame.Vector2(room.rect.centerx, room.rect.top)
        self.health = (2500 * ((hero.LevelCount - 0.5) * 1.6))
        self.image = ShadowBoss_img
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.time_hit = 0
        self.speed = 0.5
        self.damage = 20
        self.ShootCooldown = 0
        self.shooting = False
        self.immunity = False
        self.knockback = False
        self.distance_x = hero.pos[0] - self.pos[0]
        self.distance_y = hero.pos[1] - self.pos[1]
        self.angle = math.atan2(self.distance_y, self.distance_x)

    def draw(self):
        Screen.blit(self.image, self.rect)

        for bullet in S_bullet_list:  # draws the ShadowBullets and runs their update function
            bullet.draw()
            bullet.update()

    def cooldowns(self):
        if self.ShootCooldown == 0:
            self.shooting = True
        else:
            self.shooting = False

        if self.ShootCooldown > 0:
            self.ShootCooldown -= 1

    def movement(self, position):

        # finding the distance to the player
        distance_x = position[0] - self.pos[0]
        distance_y = position[1] - self.pos[1]
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5  # pythagoras

        # if the boss is not shooting then it will move towards the player
        if not self.shooting:
            if distance != 0:
                if not self.knockback:
                    self.pos[0] += self.speed * (distance_x / distance)
                    self.pos[1] += self.speed * (distance_y / distance)
                else:
                    self.pos[0] -= self.speed * (distance_x / distance)
                    self.pos[1] -= self.speed * (distance_y / distance)

        self.rect.center = self.pos

    def collision(self, BulletType):

        # checks if they have collided with player and player has no shield
        if self.rect.colliderect(hero.rect) and hero.shield == 0:
            self.knockback = True
            if not hero.immunity:
                hero.health -= self.damage  # if hero is not immune they will take damage
            self.immunity = True  # set immunity to true
            self.time_hit = pygame.time.get_ticks()

        # checks if they have collided with player and if player has shield
        elif self.rect.colliderect(hero.rect) and hero.shield > 0:
            self.knockback = True
            self.time_hit = pygame.time.get_ticks()
            hero.shield -= 5  # reduces the amount of shield a user has by 5
            if hero.shield < 0:
                hero.shield = 0

        if pygame.time.get_ticks() - self.time_hit > 100:
            self.immunity = False

        if pygame.time.get_ticks() - self.time_hit > 650:
            self.knockback = False

        if self.immunity:
            hero.immunity = True
        else:
            hero.immunity = False

        # checking if boss has collided with a bullet, and if yes health is reduced by how much damage weapon deals
        collide_hit = self.rect.collidelistall(bullet_list)
        if collide_hit:
            self.health -= BulletType.damage

        # for each bullet that collides with boss, it gets removed from list, de-spawning it
        for index in collide_hit:
            bullet_list.remove(bullet_list[index])

        for bullet in S_bullet_list:
            # if shadow bullet object collides with player, will decrease player's health by bullet damage
            if hero.rect.colliderect(bullet.rect):
                hero.health -= bullet.damage
                S_bullet_list.remove(bullet)  # removes bullet from list after collision occurs

    def attack(self):

        if self.shooting:
            AttackChoice = random.randint(1, 3)  # selecting one of the three attacks

            if AttackChoice == 1:
                if self.ShootCooldown == 0:
                    for i in range(16):  # generates 16 bullets
                        angle = (i / 16) * 2 * math.pi  # will change the angle at which each bullet is shot at
                        bullets = ShadowKey(self.rect.centerx, self.rect.centery, angle)
                        S_bullet_list.append(bullets)  # adds ShadowKey object to list
                    self.ShootCooldown = 50  # sets ShootCooldown to 50

            if AttackChoice == 2:
                if self.ShootCooldown == 0:
                    for i in range(4):  # generates 4 bullets
                        bullets = ShadowSkull(self.rect.centerx, self.rect.centery, self.angle)
                        S_bullet_list.append(bullets)  # Adds skull object to list
                    self.ShootCooldown = 75  # sets ShootCooldown to 75

            if AttackChoice == 3:
                if self.ShootCooldown == 0:
                    for i in range(6):  # generates 6 bullets
                        bullets = Blade(self.rect.centerx, self.rect.centery, self.angle)
                        S_bullet_list.append(bullets)  # adds blade object to list
                    self.ShootCooldown = 100  # sets ShootCooldown to 100

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False


# Shadow Bullet baseclass #


class ShadowBullets:
    def __init__(self, x, y, angle, speed, damage, expire, image):
        self.pos = pygame.Vector2(x, y)
        self.speed = speed
        self.angle = angle
        self.expire = expire
        self.damage = damage
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.time_shot = pygame.time.get_ticks()
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
        # move bullet
        self.rect.x += self.dx
        self.rect.y += self.dy

        # checking if bullet's time to live has expired or not
        time_list = []
        for index in S_bullet_list:
            if pygame.time.get_ticks() - index.time_shot > index.expire:
                time_list.append(index)

        for index in time_list:
            S_bullet_list.remove(index)

    def draw(self):
        Screen.blit(self.image, self.rect)


# Shadow Bullet subclasses #


class ShadowKey(ShadowBullets):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 8, 10, 1700, S_key_img)


class ShadowSkull(ShadowBullets):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 4, 5, 1750, S_skull_img)

        self.distance_x = hero.pos[0] - self.pos[0]
        self.distance_y = hero.pos[1] - self.pos[1]

    def update(self):

        distance = (self.distance_x ** 2 + self.distance_y ** 2) ** 0.5  # pythagoras

        #  bullet will track the player following it like the common enemies
        if distance != 0:
            self.pos[0] += self.speed * self.distance_x / distance
            self.pos[1] += self.speed * self.distance_y / distance

        self.rect.center = self.pos

        time_list = []
        for index in S_bullet_list:
            if pygame.time.get_ticks() - index.time_shot > index.expire:  # checking if bullet has exceeded its TTL
                time_list.append(index)

        # removes bullet in time_list from the Shadow bullet list, resulting in it de-spawning
        for index in time_list:
            S_bullet_list.remove(index)


class Blade(ShadowBullets):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 10, 15, 2000, blade_img)


# Item Class #


class Items:
    def __init__(self, pos, item):
        self.type = item
        self.image = skills[self.type]
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


# Weapon Class #


class Weapon:
    def __init__(self, pos, weapon):
        self.type = weapon
        self.image = weapons[self.type]
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


# Chest class #


class Chest:
    def __init__(self):
        x = random.randrange(400, 1000)
        y = random.randrange(400, 800)
        self.image = chest_img
        self.pos = pygame.Vector2(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.present = True  # checks if the chest should be appearing on screen or not

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def update(self):
        keys = pygame.key.get_pressed()
        # checking if player is able to open chest or not
        if keys[pygame.K_e] and self.rect.colliderect(hero.rect) and hero.KeyCount > 0:
            hero.KeyCount -= 1
            self.drop_item()

    def drop_item(self):
        self.present = False

        for count in range(1):
            Item_list.append(Items(
                (random.uniform(self.pos.x - 40, self.pos.x + 40), random.uniform(self.pos.y - 40, self.pos.y + 40)),
                random.randint(0, 1)))
            if random.randint(0, 1) == 0:  # determines if chest drops an ability or weapon
                Item_list.append(Items((random.uniform(self.pos.x - 40, self.pos.x + 40),
                                        random.uniform(self.pos.y - 40, self.pos.y + 40)), random.randint(3, 6)))
            else:
                Weapon_list.append(Weapon((random.uniform(self.pos.x - 40, self.pos.x + 40),
                                           random.uniform(self.pos.y - 40, self.pos.y + 40)), random.randint(0, 4)))


# generating the number of waves in a room function #

def EnemySpawn(stack):
    NumOfWaves = random.randint(2, 4)  # determines the number of waves in an enemy room

    for number in range(NumOfWaves):
        stack.push(E_wave())  # pushes that number of waves onto the EnemyWaveStack

    return stack


# pushing chests to the stack function #

def ChestSpawn(stack):
        stack.push(C_Wave())

        return stack


EnemyWaveStack = EnemySpawn(EnemyWaveStack)
ChestWaveStack = ChestSpawn(ChestWaveStack)


# spawning an enemy wave in a room function #


def EnemyWave(Rooms):
    global Enemy_list, EnemyWaveStack
    room = Rooms[hero.RoomIndex]
    if len(Enemy_list) == 0:
        # if enemy list is empty it will add the popped value of the enemy stack to list, running an enemy wave
        list = EnemyWaveStack.pop()
        if list:
            Enemy_list = list

    if len(Enemy_list) != 0:  # whilst the list is not empty it will run the enemy methods
        for enemy in Enemy_list:
            enemy.draw()
            enemy.movement(hero.pos)
            enemy.collision(BulletType=hero.WeaponType)
            enemy.check_alive()
            enemy.drop_item()
            enemy.check_status()

            if not enemy.alive:
                hero.score += 50  # adds to the score of the player
                hero.EnemiesKilled += 1  # adds to the player's statistics
                Enemy_list.remove(enemy)

            if len(Enemy_list) == 0:  # checking if the list is empty to determine whether the player can move on or no
                room.EnemiesCleared = True
            else:
                room.EnemiesCleared = False


# spawning chests in a room function #


def ChestWave():
    global Chest_list, ChestWaveStack
    # if chest list is empty it will add the popped value of the chest stack to list, outputting all the chests
    if len(Chest_list) == 0:
        list = ChestWaveStack.pop()
        if list:
            Chest_list = list

    if len(Chest_list) != 0:  # whilst the list is not empty it will run the chest methods
        for chest in Chest_list:
            chest.draw(Screen)
            chest.update()

            if not chest.present:
                hero.score += 10  # adds to score of the player
                Chest_list.remove(chest)


# enabling player to use weapons function #


def player_weapons():
    hero.use_burn()
    hero.use_stun()
    hero.use_decay()
    hero.use_invincibility()

    hero.use_pellet()
    hero.use_flame()
    hero.use_ice()
    hero.use_cannon()
    hero.use_shadow()
    hero.use_axe()


# player picking up items function #


def pick_item():
    global Item_list
    keys = pygame.key.get_pressed()

    for item in Item_list:

        item_hit = hero.rect.colliderect(item.rect)

        if item_hit and keys[pygame.K_f]:
            if item.type == 3:
                hero.add_burn()
                Item_list.remove(item)
            elif item.type == 4:
                hero.add_decay()
                Item_list.remove(item)
            elif item.type == 5:
                hero.add_stun()
                Item_list.remove(item)
            elif item.type == 6:
                hero.add_invincibility()
                Item_list.remove(item)

        if item_hit:
            if item.type == 0:
                hero.health += 10
                Item_list.remove(item)

        if hero.health > Max_Health:
            OverHeal = hero.health - Max_Health
            hero.health -= OverHeal

        if item_hit:
            if item.type == 1:
                hero.shield += 1
                Item_list.remove(item)
            elif item.type == 2:
                hero.KeyCount += 1
                Item_list.remove(item)


# player picking up weapons function #


def pick_weapon():
    global Weapon_list
    keys = pygame.key.get_pressed()

    for weapon in Weapon_list:

        weapon_hit = hero.rect.colliderect(weapon.rect)

        if weapon_hit and keys[pygame.K_f]:
            if weapon.type == 0:
                hero.add_flame()
                Weapon_list.remove(weapon)
            elif weapon.type == 1:
                hero.add_cannon()
                Weapon_list.remove(weapon)
            elif weapon.type == 2:
                hero.add_ice()
                Weapon_list.remove(weapon)
            elif weapon.type == 3:
                hero.add_axe()
                Weapon_list.remove(weapon)
            elif weapon.type == 4:
                hero.add_shadow()
                Weapon_list.remove(weapon)
