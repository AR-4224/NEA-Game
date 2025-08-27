from constants import *


pygame.init()
# loading and scaling sprite images

#  ENVIRONMENT SPRITES
floor_img = pygame.image.load('img/flooring.png').convert_alpha()
background_img = pygame.transform.scale(pygame.image.load('img/wall.png').convert_alpha(), (1920, 1080))
control_img = pygame.transform.scale(pygame.image.load('img/ControlPage.png').convert_alpha(), (1536, 864))

#  PLAYER AND ENEMY SPRITES
bat_img = pygame.transform.scale(pygame.image.load('img/bat.png').convert_alpha(), (40, 40))
skull_img = pygame.transform.scale(pygame.image.load('img/floating_skull.png').convert_alpha(), (40, 40))
ShadowBoss_img = pygame.transform.scale(pygame.image.load('img/DungeonKeeper.png').convert_alpha(), (256, 256))
player_img = pygame.transform.scale(pygame.image.load('img/hero_idle.png').convert_alpha(), (64, 64))

# ITEM SPRITES
health_img = pygame.transform.scale(pygame.image.load('img/Health.png').convert_alpha(), (32, 32))
shield_img = pygame.transform.scale(pygame.image.load('img/Shield.png').convert_alpha(), (32, 32))
burn_img = pygame.transform.scale(pygame.image.load('img/BurnSkill.png').convert_alpha(), (32, 32))
decay_img = pygame.transform.scale(pygame.image.load('img/DecaySkill.png').convert_alpha(), (32, 32))
stun_img = pygame.transform.scale(pygame.image.load('img/StunSkill.png').convert_alpha(), (32, 32))
invinc_img = pygame.transform.scale(pygame.image.load('img/InvincibilitySkill.png').convert_alpha(), (32, 32))
key_img = pygame.transform.scale(pygame.image.load('img/key.png').convert_alpha(), (32, 32))

#  WEAPON SPRITES
flame_img = pygame.transform.scale(pygame.image.load('img/flame_weapon.png').convert_alpha(), (32, 32))
cannon_img = pygame.transform.scale(pygame.image.load('img/cannon_weapon.png').convert_alpha(), (32, 32))
ice_img = pygame.transform.scale(pygame.image.load('img/IceWeapon.png').convert_alpha(), (32, 32))
axe_img = pygame.transform.scale(pygame.image.load('img/axe_weapon.png').convert_alpha(), (32, 32))
shadow_img = pygame.transform.scale(pygame.image.load('img/ShadowWeapon.png').convert_alpha(), (32, 32))

#  PROJECTILE SPRITES
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
crescent_img = pygame.transform.scale(pygame.image.load('img/ShadowCrescent.png').convert_alpha(), (32, 32))
B_Axe_img = pygame.transform.scale(pygame.image.load('img/B_axe.png').convert_alpha(), (32, 32))
fire_img = pygame.transform.scale(pygame.image.load('img/fire.png').convert_alpha(), (32, 32))
CannonBall_img = pygame.transform.scale(pygame.image.load('img/CannonBall.png').convert_alpha(), (32, 32))
SnowBall_img = pygame.transform.scale(pygame.image.load('img/Snowball.png').convert_alpha(), (32, 32))

blade_img = pygame.transform.scale(pygame.image.load('img/ShadowBlade.png').convert_alpha(), (32, 32))
S_key_img = pygame.transform.scale(pygame.image.load('img/ShadowKey.png').convert_alpha(), (32, 32))
S_skull_img = pygame.transform.scale(pygame.image.load('img/ShadowSkull.png').convert_alpha(), (32, 32))

#  INTERACTION SPRITES
chest_img = pygame.transform.scale(pygame.image.load('img/chest.png').convert_alpha(), (40, 40))
Play_img = pygame.transform.scale(pygame.image.load('img/PlayButton.png').convert_alpha(), (256, 128))
Option_img = pygame.transform.scale(pygame.image.load('img/OptionButton.png').convert_alpha(), (256, 128))
Quit_img = pygame.transform.scale(pygame.image.load('img/QuitButton.png').convert_alpha(), (256, 128))
Menu_img = pygame.transform.scale(pygame.image.load('img/MenuButton.png').convert_alpha(), (256, 128))
Login_img = pygame.transform.scale(pygame.image.load('img/Login.png').convert_alpha(), (256, 128))
confirm_img = pygame.transform.scale(pygame.image.load('img/Confirm.png').convert_alpha(), (256, 128))
skip_img = pygame.transform.scale(pygame.image.load('img/skip.png').convert_alpha(), (256, 128))
legacy_img = pygame.transform.scale(pygame.image.load('img/legacy.png').convert_alpha(), (768, 192))
leaderboard_img = pygame.transform.scale(pygame.image.load('img/leaderboard.png').convert_alpha(), (768, 192))
H_legacy_img = pygame.transform.scale(pygame.image.load('img/H_legacy.png').convert_alpha(), (768, 192))
H_leaderboard_img = pygame.transform.scale(pygame.image.load('img/H_leaderboard.png').convert_alpha(), (768, 192))
game_over_img = pygame.transform.scale(pygame.image.load('img/GameOver.png').convert_alpha(), (768, 192))

skills = [health_img, shield_img, key_img, burn_img, decay_img, stun_img, invinc_img]
weapons = [flame_img, cannon_img, ice_img, axe_img, shadow_img]

