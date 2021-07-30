import pygame
import random
import math
from pygame import mixer

#initilization
pygame.init()


#screen
screen = pygame.display.set_mode((800,600))
background = pygame.image.load('background.png')

#name
pygame.display.set_caption('Space Invaders')

icon = pygame.image.load('ufo.png')

pygame.display.set_icon(icon)



#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []

enemyY_change = []

num_enemies = 234


#Music
mixer.music.load('music.mp3')
mixer.music.play(-1)


for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(-5000,-70))
    enemyX_change.append(random.randint(1,4))
    enemyY_change.append(30)

senemyX_change = enemyX_change.copy()
#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


#Plasma
plasmaImg = pygame.image.load('plasma.png')
plasmaX = 0
plasmaY = playerY
plasmaY_change = -5

plasma_condition = "ready"


#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
fontX = 10
fontY =10

#Game Over

game_over = pygame.image.load('gameover.png')

game_overX =300
game_overY = 180
game_overY_change = -3



def show_score(x,y):
    score = font.render("Score:" +" " + str(score_value),True,(0,255,50))
    screen.blit(score,(x,y))



def player(x,y):
    screen.blit(playerImg,(playerX,playerY))


def enemy(x,y,i):



    screen.blit(enemyImg[i],(x,y))




def fire_plasma(x,y):
    global plasma_condition
    plasma_condition = "fire"
    screen.blit(plasmaImg,(plasmaX+4,plasmaY+10))




def iScollision(plasmaX,plasmaY,enemyX,enemyY):
    distance = math.sqrt(math.pow(enemyX - plasmaX, 2) + (math.pow(enemyY - plasmaY, 2)))
    if distance <27:
        return True
    else:
        return False



def GameOver(x,y):
    screen.blit(game_over,(x,y))



#Game loop
running = True


while running:




#Close Window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:


            running = False
#color
    screen.fill((0,0,0))



#Background
    screen.blit(background,(0,0))



#Keyboard

    if event.type==pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -4
        if event.key == pygame.K_RIGHT:
            playerX_change = 4


        if event.key == pygame.K_UP:
            if plasma_condition == "ready":
                Plasma_sound = mixer.Sound('plasma.wav')
                Plasma_sound.play()
                plasmaX = playerX

                fire_plasma(plasmaX,plasmaY)


    if event.type==pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0


#Changing player coordinate
    playerX += playerX_change

    if playerX <= 0:
        playerX = 800
    elif playerX >= 800:
        playerX = 0

#Changing enemy coordinate
    for i in range(num_enemies):



        # Game Over!!!!!
        if enemyY[i] > 450:
            for j in range(num_enemies):
                enemyY[j] = 2000
            GameOver(game_overX,game_overY)
            break

        enemyX[i] += (enemyX_change[i])

        if enemyX[i]<=0:
           enemyX_change[i] = senemyX_change[i]
           enemyY[i] += enemyY_change[i]
        elif enemyX[i]>=800:
            enemyX_change[i] = (-1)*senemyX_change[i]
            enemyY[i] += enemyY_change[i]

            # Collision
        collision = iScollision(plasmaX, plasmaY, enemyX[i], enemyY[i])
        if collision:
            Explosion_sound = mixer.Sound('damage.wav')
            Explosion_sound.play()

            bulletY = 480
            bulletState = "ready"
            score_value += 1

            enemyX[i] = random.randint(100, 800)
            enemyY[i] = random.randint(-400, -100)


        enemy(enemyX[i], enemyY[i],i)



#Changing plasma coordinate


    if plasmaY<=-50:
        plasmaY = playerY
        plasma_condition = "ready"

    if plasma_condition is "fire":
        fire_plasma(plasmaX,plasmaY)
        plasmaY+=plasmaY_change


#Changing game_over coordinate
    for game_overY in range(900, 400):
        game_overY+=game_overY_change





    player(playerX,playerY)

    show_score(fontX,fontY)

    pygame.display.update()