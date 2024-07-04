import pygame
import math
import random
from pygame import mixer
from localStoragePy import localStoragePy

localStorage = localStoragePy('bikegame')
    

# initialize pygame
pygame.init()
# set the window game name
pygame.display.set_caption("Bike Race Game")
# set game icon 
icon =  pygame.image.load("./images/icon.png")
pygame.display.set_icon(icon)

# create a game window with width and height
screen_width  =  500
screen_height = 750
screen = pygame.display.set_mode((screen_width,screen_height))

road1 = pygame.image.load("./images/road.png")
road1 = pygame.transform.scale(road1,(screen_width,screen_height +3 ))
road2 = pygame.image.load("./images/road.png")
road2 = pygame.transform.scale(road2,(screen_width,screen_height + 3))

road1_Y = 0
road2_Y = -screen_height
road_speed = 4

#background sound
mixer.music.load("./music/bg.mp3")
mixer.music.play(-1)

# load the player image
playerImg =  pygame.image.load("./images/player.png")
#initial player position on screen
playerPosX =  250 - (64/2)
playerPosY =  650
#rate of change of player position
playerXPosChange = 0
playerYPosChange = 0
playerXSpeed  =  4
playerYSpeed  =  2

gameOver  =  False
overCheck = 0

enemyImg =  []
#set the speed of the enemy
enemySpeed   =  []
enemyYPos  = []
enemyXPos  = []
#four spawn positions in the x-axis
enemySpawnPositions  = [120,210, 305,380]
numberOfEnemies = 8

# load the explosionImg
explosionImg  =  pygame.image.load("./images/explosion.png")
explosionImg  = pygame.transform.scale(explosionImg,(70,70))
# load the game over image
gameOverImg  =  pygame.image.load("./images/gameover.png")
gameOverImg  = pygame.transform.scale(gameOverImg,(screen_width,screen_height))

# create an array of enemies with random speed , y position , image , and x position
for i in range(numberOfEnemies):
    enemyImg.append(pygame.image.load("./images/enemy_" + str( random.randint(1,4))+ ".png"))
    enemySpeed.append(random.randint(50,100)/50)
    enemyYPos.append(random.randint(-1000,0))
    enemyXPos.append(enemySpawnPositions[random.randint(0,3)] + random.randint(-20,20))

#load the coin
coinImg = pygame.image.load("./images/coin.png")
coinImg  = pygame.transform.scale(coinImg,(30,30))

#draw the coin out of the screen 
coinYPos  = -100
coinXPos  = 100
coinSpeed = 1.5

score  = 0
highScore = 0
#retrieve highscore saved on localstorage , asssigns 0 when its empty
if localStorage.getItem("highscore") is None:
    highScore =  0
else:
    highScore  = localStorage.getItem("highscore") 
#score text on screen 
scoreText =  pygame.font.Font("freesansbold.ttf",18)
highScoreText =  pygame.font.Font("freesansbold.ttf",18)


#set if game is running as a variable
running  =  True

#collision
def isCollision(enemyX,enemyY,playerX,playerY):
    distance  =  math.sqrt(math.pow(enemyX - playerX ,2)  + math.pow(enemyY - playerY,2))
    
    if distance < 25:
        return True
    else :
        return False
    
def displayRoad():
    global road1_Y,road2_Y
     #draw the road image
    screen.blit(road1,(0,road1_Y))
    screen.blit(road2,(0,road2_Y))
    
    #move the road
    road1_Y += road_speed
    road2_Y += road_speed
    # reset the road
    if(road1_Y >= screen_height):
        road1_Y = -screen_height
    if(road2_Y >= screen_height):
        road2_Y = -screen_height

#game running loop process
while running :
    #for loop responsible for running game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #check wether the keyboard key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXPosChange = -playerXSpeed 
                # playerPosX -= playerXPosChange        
            if event.key  == pygame.K_RIGHT:
                playerXPosChange = playerXSpeed   
                
            if event.key == pygame.K_UP:
                playerYPosChange = -playerYSpeed 
                # playerPosX -= playerXPosChange        
            if event.key  == pygame.K_DOWN:
                playerYPosChange = playerYSpeed  
            if event.key  == pygame.K_h:
                #reset highscore
                localStorage.removeItem("highscore")
                highScore = 0
            if event.key  == pygame.K_r:
                #restart the game
                if gameOver:
                    highScore = localStorage.getItem("highscore")
                    gameOver = False
                    overCheck = 0
                    score  = 0
                    playerXSpeed  = 4 
                    playerYSpeed  = 2 
                    playerPosX =  200 - (64/2)
                    playerPosY =  650
                    road_speed = 4
                    mixer.music.play(-1)
                    #reset the enemy positions
                    enemyYPos = []
                    enemyXPos = []
                    for i in range(numberOfEnemies):
                        enemyYPos.append(random.randint(-1000,0))
                        enemyXPos.append(enemySpawnPositions[random.randint(0,3)] + random.randint(-20,20))
                        enemySpeed[i] = random.randint(50,100)/45
                  
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key  == pygame.K_RIGHT:
                playerXPosChange = 0
            if event.key == pygame.K_UP or event.key  == pygame.K_DOWN:
                playerYPosChange = 0
    
    
    #change the location of the player
    playerPosX += playerXPosChange
    playerPosY += playerYPosChange
    #set boundaried so it does'nt move out of frame
    if(playerPosX <= 45):
        playerPosX = 45
    if(playerPosX >= screen_width - 66):
        playerPosX = screen_width - 66
    if(playerPosY <= 1):
        playerPosY = 1
    if(playerPosY >= screen_height - 60):
        playerPosY = screen_height - 60
        
    #display the road
    displayRoad()    
    #show player
    screen.blit(playerImg,(playerPosX,playerPosY))  

    
    for i in range(numberOfEnemies):
        #draw the enemy or obstacle on the screen
        screen.blit(enemyImg[i],( enemyXPos[i], enemyYPos[i] ))
        #move the enemy
        enemyYPos[i]  +=  enemySpeed[i]
        #when the player collids , stop all movement
        if isCollision(enemyXPos[i] ,enemyYPos[i], playerPosX, playerPosY): 
            gameOver  = True
            if overCheck == 0 : 
                if score > int(highScore):
                    localStorage.setItem("highscore" , score)
                mixer.music.pause()
                crash_sound = mixer.Sound("./music/crash.mp3")
                crash_sound.play()
                gameOver = mixer.Sound("./music/gameover.mp3")
                gameOver.play()
                screen.blit(explosionImg,(playerPosX,playerPosY))
                playerXSpeed  = 0 
                playerYSpeed  = 0 
                road_speed = 0
                #make all the vehicles go forward
                for j in range(numberOfEnemies):
                    enemySpeed[j] = -(random.randint(50,100)/45)
                #stop the colided enemy    
                enemySpeed[i]  = 0
            overCheck  = 1
        
        #when the enemy goes off screen reset the x and y position
        if enemyYPos[i] > screen_height + 10 :
            enemyYPos[i] = random.randint(-1000,0)
            enemyXPos[i] = enemySpawnPositions[random.randint(0,3)] + random.randint(-20,20)
            enemySpeed[i] = random.randint(50,100)/45

     

    #draw the coin the screen
    screen.blit(coinImg,(coinXPos,coinYPos))
    #move the coin y axis
    if gameOver is False:
     coinYPos  +=  coinSpeed
    #when the player collids with the coin increase score
    if isCollision(coinXPos ,coinYPos, playerPosX, playerPosY): 
        coin_sound = mixer.Sound("./music/coin.mp3")
        coin_sound.play()
        score += 1
        coinYPos =  -100
        coinXPos = enemySpawnPositions[random.randint(0,3)] + random.randint(-20,20)
        if score == int(highScore) + 1: 
            highScore_sound = mixer.Sound("./music/highscore.mp3")
            highScore_sound.play()

       
    
    # when the coins goes off screen reset the x and y position
    if coinYPos > screen_height + 10 :
        coinYPos = -100
        coinXPos = enemySpawnPositions[random.randint(0,3)] + random.randint(-20,20)
        
    #render the score on the screen
    screen.blit(scoreText.render("Score: " + str(score) ,True,(255,255,255)) , (45,10))
    screen.blit(highScoreText.render(  "High score: " + str(highScore)  ,True,(255,255,255)) , (45,40))
     
    if gameOver:
        screen.blit(gameOverImg,(0,0))


      
    #update the screen
    pygame.display.update()
    
pygame.quit()