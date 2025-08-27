from PlayerEnemy import *

# Node class #


class Node:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None


# random splitting function #


def ran_split(rect):
    if random.randint(0, 1) == 0:
        # horizontal splitting
        room1 = rect.copy()
        room1.height = random.randrange(MIN_R_SIZE, room1.height)
        room2 = rect.copy()
        room2.height -= room1.height
        room2.top += room1.height

        room1_h_ratio = room1.height / room1.width
        room2_h_ratio = room2.height / room2.width
        if room2_h_ratio < MIN_R_RATIO or room1_h_ratio < MIN_R_RATIO:
            return ran_split(rect)  # if room ratio is less than the min ratio it will redo the function
    else:
        # vertical splitting
        room1 = rect.copy()
        room1.width = random.randrange(MIN_R_SIZE, room1.width)
        room2 = rect.copy()
        room2.width -= room1.width
        room2.left += room1.width

        room1_w_ratio = room1.width / room1.height
        room2_w_ratio = room2.width / room2.height
        if room2_w_ratio < MIN_R_RATIO or room1_w_ratio < MIN_R_RATIO:
            return ran_split(rect)  # if room ratio is less than the min ratio it will redo the function
    return room1, room2


# splitting tree function #


def split_tree(rect, N_iterations):
    root = Node(data=rect)  # initialising root node
    if N_iterations != 0:
        left, right = ran_split(rect)  # generate the first 2 rooms
        root.left = split_tree(left, N_iterations - 1)  # run function to split left node until leaf nodes are formed
        root.right = split_tree(right, N_iterations - 1)  # run function to split right node until leaf nodes are formed
    return root


# generate dungeon function #

def gen_dungeon():
    dungeon_rect = pygame.Rect((0, 0), (D_WIDTH, D_HEIGHT))  # makes the dungeon rect
    rect_tree = split_tree(dungeon_rect, 3)  # splits the dungeon rect using the tree splitting function

    return rect_tree


# generating list of leaf nodes function #


def leaf_node_tree(root_node):
    node_list = []
    if root_node.left and root_node.right:  # detecting if there are child nodes
        node_list.extend(leaf_node_tree(root_node.left))  # runs function to see if current node has child nodes
        node_list.extend(leaf_node_tree(root_node.right))
    else:
        node_list.append(root_node)  # adds leaf node to list
    return node_list


# drawing the dungeon function #


def dungeon_drawn(dungeon_tree):
    floor_list = []

    # runs for each node in the list
    for node in leaf_node_tree(dungeon_tree):
        total_rect = node.data

        room_rect = total_rect.copy()

        room_rect = pygame.Rect((room_rect.x, room_rect.y), (16, 9))  # repositioning rect for the map

        # resizing the room rect
        display_rect = room_rect.copy()
        display_rect.x *= 400
        display_rect.y *= 400
        display_rect.w *= 90
        display_rect.h *= 90

        floor_list.append(display_rect)  # adds to the floor list
    return floor_list


# room declaration function #


def room_declaration(floor_list):
    global Rooms
    Rooms.clear()  # emptying Room list in case there is something in it that shouldn't be
    NumOfSafeRooms = random.randint(2, 4)  # generating number of safe rooms
    queue = floor_list

    random.shuffle(queue)  # shuffles the order of the rooms

    # adds to the end of the Rooms list
    Rooms.extend([EnemyRoom(element) for element in queue])  # converts each room into enemy room, adds them to list

    Rooms.extend([BossRoom(element) for element in [queue.pop(0)]])  # converts first room in queue to a boss room

    for element in range(NumOfSafeRooms):
        Safe = queue.pop(0)  # pops the first enemy room in the list
        Rooms.insert(0, SafeRoom(Safe))  # insert them into the first position of the Room list

    StarterRoom = Rooms.pop(0)  # pops the first safe room from the list
    LastRoom = Rooms.pop()  # pops the boss room from the list

    random.shuffle(Rooms)  # shuffle the list to make the order of rooms random

    Rooms.insert(0, StarterRoom)  # add a safe room to the beginning of list
    Rooms.extend([LastRoom])  # add the boss room to the end of list

    return Rooms


# Room baseclass #


class Room:
    def __init__(self, rect):
        self.rect = rect
        self.screen_rect = Screen.get_rect()
        self.rect.center = self.screen_rect.center
        self.pos = self.rect.topleft
        self.image = pygame.transform.scale(floor_img, (self.rect.w, self.rect.h))
        self.PlayerInRoom = False
        self.door_rect = pygame.Rect((self.rect.right - 10), self.rect.top, 1, self.rect.h)

    def draw(self):
        Screen.blit(self.image, self.pos)


# Room subclasses #


class EnemyRoom(Room):
    def __init__(self, rect):
        super().__init__(rect)
        self.EnemiesCleared = False

    def update(self):
        if self.rect.left < hero.rect.x < self.rect.right and self.rect.top < hero.rect.y < self.rect.bottom:
            self.PlayerInRoom = True  # detecting if player is in the room or not

        if self.PlayerInRoom:
            EnemyWave(Rooms)  # if the player is in the room, run the enemy wave function


class SafeRoom(Room):
    def __init__(self, rect):
        super().__init__(rect)
        self.EnemiesCleared = True

    def update(self):
        if self.rect.left < hero.rect.x < self.rect.right and self.rect.top < hero.rect.y < self.rect.bottom:
            self.PlayerInRoom = True  # detecting if player is in the room or not

        if self.PlayerInRoom:
            ChestWave()  # if the player is in the room, run the chest spawn


class BossRoom(Room):
    global Boss_list

    def __init__(self, rect):
        super().__init__(rect)
        self.EnemiesCleared = False
        self.Boss = ShadowBoss()
        if len(Boss_list) == 0:  # if boss list is empty, initialise boss object and add it to list
            Boss_list.append(ShadowBoss())

    def update(self):
        if self.rect.left < hero.rect.x < self.rect.right and self.rect.top < hero.rect.y < self.rect.bottom:
            self.PlayerInRoom = True

        if self.PlayerInRoom:
            for boss in Boss_list:
                # if the player is in the room, it runs the methods of the boss
                boss.draw()
                boss.movement(hero.pos)
                boss.attack()
                boss.collision(BulletType=hero.WeaponType)
                boss.cooldowns()
                boss.check_alive()

                if not boss.alive:
                    hero.score += 150  # adds to hero score
                    hero.BossesKilled += 1
                    Boss_list.remove(boss)  # removes boss from list

                if len(Boss_list) == 0:
                    self.EnemiesCleared = True
                else:
                    self.EnemiesCleared = False
