import pygame
import sys
import time
import random
import ctypes

from ctypes import pythonapi, wintypes
from pygame import sprite
from pygame import key
from pygame.draw import rect
from pygame.event import pump, wait
from pygame import font
pygame.font.init()

myappid = 'elementalstudios.snake.Alpha 0_1' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


#------ Initialize Variables------#
# Player
player_width = 20
player_height = 20
# Food
food_width = 10
food_height = 10
# Colours
seafoam_gr = (159, 226, 191)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
# Score	
score = 0

#------ Score Font Initialize ------#
font = pygame.font.Font(None, 50)
text = font.render("Score:", False, white, None)

#------Sprites Class------#a
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, x, y, height, width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.x, self.y = self.rect.x, self.rect.y

    def move(self, move_x, move_y, speed_up):
        if move_x or move_y:
            direction = pygame.math.Vector2(move_x, move_y)
            direction.scale_to_length(5 if speed_up else 3)
            self.x += direction.x
            self.y += direction.y
            self.rect.x, self.rect.y = round(self.x), round(self.y)

#------ Font Class ------#
def create_font(t, size = 24, colour_font = white, bold = False, italic = False):
    font = pygame.font.Font("prstart.ttf", size, bold, italic)
    text = font.render(t, False, colour_font)
    return text

#------ Initialize Pygame and Window------#
pygame.init()

icon = pygame.image.load('Icon.ico')
pygame.display.set_icon(icon)
gameDisplay = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
#rect = pygame.Rect( * gameDisplay.get_rect().center, 0, 0).inflate(100, 100)
pygame.display.set_caption("Blocky")
gameDisplay.fill(black)
clock = pygame.time.Clock()
running = True

#------Initialize Sprites------#
all_sprites_list = pygame.sprite.Group()
player = Sprite(seafoam_gr, 960, 540, player_height, player_width)
food = Sprite(red, 600, 30, food_height, food_width)
static_enemy = Sprite(green, 200, 300, food_height, food_width)
player.rect.x = 960
player.rect.y = 540
#food.rect.x = random.randrange(100, 1800)
#food.rect.y = random.randrange(100, 1050)
#static_enemy.rect.x = random.randrange(100, 1800)
#static_enemy.rect.y = random.randrange(100, 1050)
#rectangle = pygame.Rect(x_pos, y_pos, width, height)
#def make_rect():    
#	pygame.draw.rect(gameDisplay, seafoam_gr, rectangle)

#------Add Sprites to sprite list------#
all_sprites_list.add(player)
all_sprites_list.add(food)
all_sprites_list.add(static_enemy)

clock = pygame.time.Clock()

while running:
    game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if player.rect.colliderect(food):
        food.rect.x = random.randrange(100, 1500)
        food.rect.y = random.randrange(100, 700)
        static_enemy.rect.x = random.randrange(100, 1800)
        static_enemy.rect.y = random.randrange(100, 1050)
        score += 1
        # render text
        text = font.render("Score: " + str(score), False, white, None)

    if player.rect.colliderect(static_enemy):
        text = font.render("Game Over", False, white, None)
        game_over = True
        wait(5000)
        pygame.quit()
        break

    #if player.rect.colliderect(player):
    #    font.render("Score: " + str(score), False, white, None)
    if game_over == False:
        keys = pygame.key.get_pressed()
        #speed = 5 if keys[pygame.K_LCTRL] else 3
        move_x = ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT]))
        move_y = ((keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP]))
        player.move(move_x, move_y, keys[pygame.K_LCTRL])

    all_sprites_list.update()
    
    gameDisplay.fill(black)

    # draw text
    gameDisplay.blit(text, text.get_rect(center = (100, 50)))
    
    all_sprites_list.draw(gameDisplay)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
quit()