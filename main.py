from menu import *

pygame.init()

username, UserID = login_screen()
main(username, UserID)
