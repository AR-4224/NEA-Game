import sys
from map import *
import random
import mysql.connector
from button import Button

#  connecting file to the database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Project@1025',
    port='3306',
    database='amitdb'
)
cursor = mydb.cursor()

# allowing keys to continue actuation when pressed down
pygame.key.set_repeat(500, 100)
clock = pygame.time.Clock()
logged_in = False

# game loop function #


def game_loop(username, UID):
    global score
    base_font = pygame.font.Font(None, 25)
    colour = (0, 0, 0)
    WHITE = (255, 255, 255)
    hero.add_pellet()
    # resetting player attributes
    hero.health = 100
    hero.KeyCount = 2
    hero.RoomIndex = 0
    hero.EnemiesKilled = 0
    hero.BossesKilled = 0
    hero.FloorsCleared = 0
    hero.TotalRuns = 0
    hero.alive = True

    # generating map and assign rooms a room types
    DungeonTree = gen_dungeon()
    floor_list = dungeon_drawn(DungeonTree)
    Rooms = room_declaration(floor_list)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if hero.RoomIndex == len(Rooms):  # checking if the player has reached the final room
            hero.RoomIndex = 0  # move player back to the first room
            hero.LevelCount += 1  # increasing the level count by 1
            DungeonTree = gen_dungeon()  # regenerating the map
            floor_list = dungeon_drawn(DungeonTree)
            Rooms = room_declaration(floor_list)

        if hero.alive:
            # text and text boxes for the UI
            health = 'Health: ' + str(hero.health) + '/100'
            health_rect = pygame.Rect(0, 0, 300, 25)
            shield = 'Shield count: ' + str(hero.shield)
            shield_rect = pygame.Rect(400, 0, 300, 25)
            key = 'Key count: ' + str(hero.KeyCount)
            key_rect = pygame.Rect(800, 0, 300, 25)
            floor = 'Floor: ' + str(hero.RoomIndex + 1)
            floor_rect = pygame.Rect(0, 840, 300, 25)
            level = 'Level: ' + str(hero.LevelCount)
            level_rect = pygame.Rect(400, 840, 300, 25)

            rect_list = [health_rect, shield_rect, key_rect, floor_rect, level_rect]
            text_list = [health, shield, key, floor, level]

            Screen.fill((0, 0, 0))
            Screen.blit(background_img, (0, 0))

            # running room class methods
            Rooms[hero.RoomIndex].draw()
            Rooms[hero.RoomIndex].update()

            for item in Item_list:
                if item.image:
                    Screen.blit(item.image, item.rect)

            for weapon in Weapon_list:
                if weapon.image:
                    Screen.blit(weapon.image, weapon.rect)

            # run functions and methods for the player
            pick_item()
            pick_weapon()
            hero.movement(Rooms)
            hero.dash(Rooms)
            hero.update(Rooms)
            hero.draw()
            hero.immune()
            hero.Cooldowns()
            player_weapons()

            # checking if the player has died
            if hero.health <= 0:
                hero.health = 0
                if hero.health == 0:
                    hero.alive = False

            count = 0

            # drawing the UI
            for rect in rect_list:
                pygame.draw.rect(Screen, colour, rect, 4)
                surface = base_font.render(text_list[count], True, WHITE)
                Screen.blit(surface, (rect.x + 10, rect.y + 10))
                count += 1

        if not hero.alive:
            Rooms.clear()  # empties room list to be reset
            DungeonTree = gen_dungeon()
            floor_list = dungeon_drawn(DungeonTree)
            Rooms = room_declaration(floor_list)  # regenerate map
            # resetting player attributes
            hero.health = 100
            hero.KeyCount = 2
            hero.EnemiesKilled = 0
            hero.BossesKilled = 0
            hero.FloorsCleared = 0
            hero.TotalRuns = 0
            hero.add_pellet()  # resetting to starter weapon
            hero.FloorsCleared = hero.RoomIndex - 1
            game_over(username, UID)  # run the game over function

        clock.tick(60)
        pygame.display.update()


# ID generator function #


def generate_ID():
    generate_Number = random.randint(0, 9999)
    ID = str(generate_Number)
    if len(ID) < 4:
        for count in range(4 - len(ID)):
            ID = '0' + ID

    return ID


# Main Menu Screen function #


def main(user, UID):
    while True:
        Screen.fill((0, 0, 0))

        mouse_pos = pygame.mouse.get_pos()

        # buttons for the main menu
        play_button = Button(Play_img, 800, 180)
        menu_button = Button(Menu_img, 800, 380)
        option_button = Button(Option_img, 800, 580)
        quit_button = Button(Quit_img, 800, 780)

        # runs the update function for the buttons
        for button in [play_button, menu_button, option_button, quit_button]:
            button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # checks what button the user has pressed and runs their corresponding screens
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.CheckForInput(mouse_pos):
                    game_loop(user, UID)
                if option_button.CheckForInput(mouse_pos):
                    Options_Screen(user, UID)
                if menu_button.CheckForInput(mouse_pos):
                    if user:  # checks if a username has been returned and if so, means that user is logged in
                        Menu_Screen(user, UID)
                if quit_button.CheckForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Login Screen function #


def login_screen():
    global logged_in
    base_font = pygame.font.Font(None, 70)
    grey = (50, 50, 50)
    user = ''  # allows for user input
    pin = ''  # allows for user input

    # rects for the username and password box
    user_text_rect = pygame.Rect(570, 200, 400, 32)
    username_rect = pygame.Rect(570, 250, 400, 64)
    password_text_rect = pygame.Rect(570, 400, 400, 32)
    password_rect = pygame.Rect(570, 450, 400, 64)
    # colour's for whether the box has been selected or not
    active_colour = (255, 255, 255)
    passive_colour = (0, 0, 0)
    user_active = False
    pass_active = False

    # buttons to either skip or login
    Confirm_button = Button(confirm_img, 580, 650)
    Skip_button = Button(skip_img, 980, 650)

    Login_rect = pygame.Rect(650, 50, 256, 128)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # checking if the user has clicked the username box
                if username_rect.collidepoint(event.pos):
                    user_active = True
                else:
                    user_active = False

                # checking if the user has clicked the password box
                if password_rect.collidepoint(event.pos):
                    pass_active = True
                else:
                    pass_active = False

                # if the player has pressed skipped return nothing for username and password
                if Skip_button.rect.collidepoint(event.pos):
                    return None, None

                # checking if there's a matching username and password in the database
                if Confirm_button.rect.collidepoint(event.pos):
                    cursor.execute("SELECT Username, UserID FROM userinfo WHERE Username = %s AND password = %s",
                                   (user, pin))
                    Check = cursor.fetchall()  # returning query result

                    logged_in = True  # confirming that player is logged in
                    if Check:
                        return user, Check[0][1]  # returns username and password
                    else:
                        ID = generate_ID()
                        cursor.execute("INSERT INTO userinfo VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                       (ID, pin, user, 0, 0, 0, 0, 0))

                        mydb.commit()  # making a new account and creating record in the database

                        return user, ID  # returns username and password

            if event.type == pygame.KEYDOWN:
                if user_active:
                    # allowing the player to delete what they enter, and hold down the button
                    if event.key == pygame.K_BACKSPACE:
                        user = user[:-1]
                    # allowing the player to de-select text box by pressing enter
                    elif event.key == pygame.K_RETURN:
                        user_active = False
                    else:
                        user += event.unicode

                if pass_active:
                    # allowing the player to delete what they enter, and hold down the button
                    if event.key == pygame.K_BACKSPACE:
                        pin = pin[:-1]
                    # allowing the player to de-select text box by pressing enter
                    elif event.key == pygame.K_RETURN:
                        pass_active = False
                    else:
                        pin += event.unicode

        Screen.fill(grey)

        if user_active:
            user_colour = active_colour
        else:
            user_colour = passive_colour

        if pass_active:
            password_colour = active_colour
        else:
            password_colour = passive_colour

        # draws the text and text boxes rects
        pygame.draw.rect(Screen, user_colour, username_rect, 4)
        pygame.draw.rect(Screen, password_colour, password_rect, 4)
        pygame.draw.rect(Screen, grey, user_text_rect, 1)
        pygame.draw.rect(Screen, grey, password_text_rect, 1)

        user_surface = base_font.render(user, True, active_colour)  # renders text and gives it colour
        Screen.blit(user_surface, (username_rect.x + 5, username_rect.y + 5))  # adds it to the screen
        username_rect.w = max(400, user_surface.get_width() + 10)  # allows for the box to be extended if need be

        password_surface = base_font.render(pin, True, active_colour)  # renders text and gives it colour
        Screen.blit(password_surface, (password_rect.x + 5, password_rect.y + 5))  # adds it to the screen
        password_rect.w = max(400, password_surface.get_width() + 10)  # allows for the box to be extended if need be

        pass_text_surface = base_font.render('Password', True, active_colour)
        Screen.blit(pass_text_surface, password_text_rect)

        user_text_surface = base_font.render('Username', True, active_colour)
        Screen.blit(user_text_surface, user_text_rect)

        for button in [Confirm_button, Skip_button]:
            button.update(Screen)  # runs the update method from button class

        Screen.blit(Login_img, Login_rect)

        pygame.display.flip()


# Options Screen function #


def Options_Screen(username, UID):
    control_rect = control_img.get_rect()
    base_font = pygame.font.Font(None, 70)
    colour = (36, 34, 52)
    WHITE = (255, 255, 255)
    mov_rect = []
    int_rect = []

    mov1, mov2, mov3, mov4, mov5 = 'Up: W', 'Down: S', 'Left: A', 'Right: D', 'Dash: LShift + key'
    int1, int2, int3, int4 = 'Open Chest: E', 'Pick up item: F', 'Use item: SPACE', 'Shoot: Left Click'

    # list of the texts
    mov_list = [mov1, mov2, mov3, mov4, mov5]
    int_list = [int1, int2, int3, int4]

    # makes a rect for each item in each lists
    for i in range(5):
        mov_rect.append(pygame.Rect(100, 350 + (i * 100), 500, 64))

    for i in range(4):
        int_rect.append(pygame.Rect(900, 350 + (i * 100), 500, 64))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main(username, UID)  # allows player to go back to the main menu

        Screen.fill((50, 50, 50))
        Screen.blit(control_img, control_rect)

        m_count = 0
        i_count = 0

        for rect in mov_rect:
            pygame.draw.rect(Screen, colour, rect, 4)  # drawing the rect on the screen
            surface = base_font.render(mov_list[m_count], True, WHITE)  # rendering the text
            Screen.blit(surface, (rect.x + 10, rect.y + 10))  # making the text appear on screen
            m_count += 1  # increase count by 1 to move to the next text box

        for rect in int_rect:
            pygame.draw.rect(Screen, colour, rect, 4)  # drawing the rect on the screen
            surface = base_font.render(int_list[i_count], True, WHITE)  # rendering the text
            Screen.blit(surface, (rect.x + 10, rect.y + 10))  # making the text appear on screen
            i_count += 1  # increase count by 1 to move to the next text box

        pygame.display.flip()


# Menu Screen function #


def Menu_Screen(username, UID):
    legacy_button = pygame.Rect(0, 0, 768, 128)
    leaderboard_button = pygame.Rect(768, 0, 768, 128)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if legacy_button.collidepoint(event.pos):
                    legacy_menu(username, UID)  # player enters the legacy screen
                if leaderboard_button.collidepoint(event.pos):
                    leaderboard_menu(username, UID)  # player enters the leaderboard screen

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main(username, UID)  # allows player to back out into the main menu

        Screen.fill((50, 50, 50))

        Screen.blit(legacy_img, legacy_button)
        Screen.blit(leaderboard_img, leaderboard_button)

        pygame.display.flip()


# Legacy Screen function #


def legacy_menu(username, UserID):
    base_font = pygame.font.Font(None, 70)
    colour = (255, 255, 255)
    grey = (50, 50, 50)
    # putting rects at the top of the screen, next to one another
    legacy_button = pygame.Rect(0, 0, 768, 128)
    leaderboard_button = pygame.Rect(768, 0, 768, 128)

    # rects for each statistics
    username_rect = pygame.Rect(570, 300, 400, 32)
    Enemies_rect = pygame.Rect(570, 350, 400, 64)
    Bosses_rect = pygame.Rect(570, 450, 400, 64)
    Items_rect = pygame.Rect(570, 550, 400, 64)
    Floors_rect = pygame.Rect(570, 650, 400, 64)
    Runs_rect = pygame.Rect(570, 750, 400, 64)

    if type(UserID) is list:  # checking to see if variable UserID is a list or not
        UserID = UserID[0][0]

    cursor.execute("SELECT EnemiesKilled, BossesKilled, ItemsUsed, TotalRuns, FloorsCleared FROM userinfo "
                   "WHERE Username = %s AND UserID = %s", (username, UserID))

    Statistics = cursor.fetchall()  # retrieving data from the player's record

    # adding them to the current number of enemies they've killed
    EnemiesKilled = hero.EnemiesKilled + Statistics[0][0]
    BossesKilled = hero.BossesKilled + Statistics[0][1]
    ItemsUsed = hero.ItemsUsed + Statistics[0][2]
    TotalRuns = hero.TotalRuns + Statistics[0][3]
    FloorsCleared = hero.FloorsCleared + Statistics[0][4]

    cursor.execute("UPDATE userinfo SET EnemiesKilled = %s WHERE UserID = %s", (EnemiesKilled, UserID))
    cursor.execute("UPDATE userinfo SET BossesKilled = %s WHERE UserID = %s", (BossesKilled, UserID))
    cursor.execute("UPDATE userinfo SET ItemsUsed = %s WHERE UserID = %s", (ItemsUsed, UserID))
    cursor.execute("UPDATE userinfo SET TotalRuns = %s WHERE UserID = %s", (TotalRuns, UserID))
    cursor.execute("UPDATE userinfo SET FloorsCleared = %s WHERE UserID = %s", (FloorsCleared, UserID))

    mydb.commit()  # updating each field for the user and committing it to the table

    Username = 'Username: ' + username
    Enemies = 'Enemies killed: ' + str(EnemiesKilled)
    Bosses = 'Bosses killed: ' + str(BossesKilled)
    Items = 'Items used: ' + str(ItemsUsed)
    Floors = 'Floors cleared: ' + str(FloorsCleared)
    Runs = 'Total Runs: ' + str(TotalRuns)

    text_list = [Enemies, Bosses, Items, Floors, Runs]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if leaderboard_button.collidepoint(event.pos):
                    leaderboard_menu(username, UserID)  # allows player to go to the leaderboard screen

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('UserID is ' + str(UserID))
                    main(username, UserID)  # allows player to back out to main menu

        Screen.fill((50, 50, 50))

        Screen.blit(H_legacy_img, legacy_button)  # highlighted button to show that it is selected
        Screen.blit(leaderboard_img, leaderboard_button)
        count = 0

        for rect in [Enemies_rect, Bosses_rect, Items_rect, Floors_rect, Runs_rect]:
            pygame.draw.rect(Screen, colour, rect, 4)  # drawing the rect on the screen
            surface = base_font.render(text_list[count], True, colour)  # rendering the text
            Screen.blit(surface, (rect.x + 5, rect.y + 10))  # making the text appear on screen
            rect.w = max(500, surface.get_width() + 10)  # sets a max size for the rect
            count += 1  # increases count by 1 to move to the next text box

        # drawing the player username onto the screen
        pygame.draw.rect(Screen, grey, username_rect, 4)
        surface = base_font.render(Username, True, colour)
        Screen.blit(surface, username_rect)

        pygame.display.flip()


# Leaderboard Screen function #


def leaderboard_menu(username, UserID):
    legacy_button = pygame.Rect(0, 0, 768, 128)
    leaderboard_button = pygame.Rect(768, 0, 768, 128)
    podium_rect = []
    username_rect = []
    score_rect = []
    user_list = []
    podium_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    score_list = []

    base_font = pygame.font.Font(None, 70)
    colour = (255, 255, 255)

    # querying to get the usernames and scores of the top 10 players on the database
    cursor.execute("SELECT Username, Score FROM leaderboard, userinfo "
                   "WHERE userinfo.UserID = leaderboard.UserID "
                   "ORDER BY Score DESC LIMIT 10")
    records = cursor.fetchall()

    # generating each text box and adding them to their respective list
    for i in range(10):
        username_rect.append(pygame.Rect(400, 225 + (i * 60), 500, 64))
        user_list.append(records[i][0])

    for i in range(10):
        podium_rect.append(pygame.Rect(330, 225 + (i * 60), 70, 64))

    for i in range(10):
        score_rect.append(pygame.Rect(900, 225 + (i * 60), 300, 64))
        score_list.append(records[i][1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if legacy_button.collidepoint(event.pos):
                    legacy_menu(username, UserID)  # allowing player to go to the legacy screen

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main(username, UserID)  # allows player to back out into the main menu screen

        Screen.fill((50, 50, 50))
        u_count = 0
        p_count = 0
        s_count = 0

        for rect in username_rect:
            pygame.draw.rect(Screen, colour, rect, 4)  # drawing the rect on the screen
            surface = base_font.render(user_list[u_count], True, colour)  # rendering the text
            Screen.blit(surface, (rect.x + 100, rect.y + 10))  # making the text appear on screen
            u_count += 1  # increases count by 1 to move to the next text box in list

        for rect in podium_rect:
            pygame.draw.rect(Screen, colour, rect, 4)  # drawing the rect on the screen
            surface = base_font.render(podium_list[p_count], True, colour)  # rendering the text
            Screen.blit(surface, (rect.x + 10, rect.y + 10))  # making the text appear on screen
            p_count += 1  # increases count by 1 to move to the next text box in list

        for rect in score_rect:
            pygame.draw.rect(Screen, colour, rect, 4)
            surface = base_font.render(str(score_list[s_count]), True, colour)
            Screen.blit(surface, (rect.x + 100, rect.y + 10))
            s_count += 1  # increases count by 1 to move to the next text box in list

        Screen.blit(legacy_img, legacy_button)
        Screen.blit(H_leaderboard_img, leaderboard_button)  # highlighted button to show that it is selected

        pygame.display.flip()


# game over screen function #


def game_over(username, UID):
    global logged_in
    base_font = pygame.font.Font(None, 70)
    colour = (255, 255, 255)
    hero.TotalRuns += 1

    # boxes for the statistics after a run
    score_rect = pygame.Rect(570, 250, 400, 64)
    enemies_rect = pygame.Rect(570, 350, 400, 64)
    bosses_rect = pygame.Rect(570, 450, 400, 64)
    items_rect = pygame.Rect(570, 550, 400, 64)
    floors_rect = pygame.Rect(570, 650, 400, 64)
    levels_rect = pygame.Rect(570, 750, 400, 64)

    quit_button = pygame.Rect(1050, 720, 400, 64)

    # text for the statistics after a run
    Score = 'Score: ' + str(hero.score)
    Enemies = 'Enemies killed: ' + str(hero.EnemiesKilled)
    Bosses = 'Bosses killed: ' + str(hero.BossesKilled)
    Items = 'Items used ' + str(hero.ItemsUsed)
    Floors = 'Floors cleared: ' + str(hero.FloorsCleared)
    Levels = 'Levels cleared: ' + str(hero.LevelCount - 1)

    text_list = [Score, Enemies, Bosses, Items, Floors, Levels]

    if logged_in:
        cursor.execute("SELECT UserID FROM userinfo WHERE Username = %s", (username,))
        UID = cursor.fetchall()

        if type(UID) is list:  # checking to see if variable UserID is a list or not
            UID = UID[0][0]

        SID = generate_ID()
        cursor.execute("INSERT INTO leaderboard VALUES (%s, %s, %s)", (SID, hero.score, UID))

        mydb.commit()  # inserting run values into leaderboard and inserting them into database

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    main(username, UID)  # allows player to back out to the main menu

        Screen.fill((0, 0, 0))

        Game_Over = pygame.Rect(400, 50, 768, 128)

        Screen.blit(game_over_img, Game_Over)
        Screen.blit(Quit_img, quit_button)
        count = 0

        # displays each statistic's text box
        for rect in [score_rect, enemies_rect, bosses_rect, items_rect, floors_rect, levels_rect]:
            pygame.draw.rect(Screen, colour, rect, 4)
            surface = base_font.render(text_list[count], True, colour)
            Screen.blit(surface, (rect.x + 5, rect.y + 10))
            rect.w = max(450, surface.get_width() + 10)
            count += 1

        pygame.display.flip()
