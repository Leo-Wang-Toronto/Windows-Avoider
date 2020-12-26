#-----------------------------------------------------
# Program: Final Assignment - Pygame
# By: Leo Wang
# Date: Jan 24, 2018
# Desc: Avoider pygame. You try and avoid all of the
# enemies by moving the character.
# Input: Move the character using wasd or arrow keys
# Activate ForceField with "e"
# GUI just follow instructions on screen
# Press ESC to go to end screen while in game
#-----------------------------------------------------

# Imports and constants

import pygame
import math
import random
import inputbox
import time
pygame.init()

RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
BLACK = (  0,  0,  0)
WHITE = (255,255,255)

WIDTH = 1366
HEIGHT = 768
V_PLAYER = 10
playerImage = pygame.image.load("player.png")
shieldImage = pygame.image.load("shield.png")

enemyPhase1 = pygame.image.load("EnemyPhase1.png")
enemyPhase2 = pygame.image.load("EnemyPhase2.png")
enemyPhase3 = pygame.image.load("EnemyPhase3.png")
enemyPhase4 = pygame.image.load("EnemyPhase4.png")
enemyPhase5 = pygame.image.load("EnemyPhase5.png")
enemyImage = enemyPhase1

inGameMusic = pygame.mixer.Sound("inGame.wav")
gameOverMusic = pygame.mixer.Sound("gameOver.wav")
MenuMusic = pygame.mixer.Sound("MainMenu.wav")
DeathSound = pygame.mixer.Sound("DeathSound.wav")

canvas = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Fonts
title_font = pygame.font.SysFont(None, 72)
press_font = pygame.font.SysFont(None, 56)
score_font = pygame.font.SysFont(None, 36)

# Functions

# Draw the player
def drawPlayer(x, y):
    canvas.blit(playerImage, (x, y))

# Draw the forcefield to the player's coordinates
def ForceFieldOn():
    Shield = pygame.transform.scale(shieldImage, (200, 200))
    canvas.blit(Shield, (player_x - 52, player_y - 52))

# Function to blit any text or string to the window
def printText(text, font, canvas, x, y):
    theText = font.render(text, 1, WHITE)
    textbox = theText.get_rect()
    textbox.topleft = (x, y)
    canvas.blit(theText, textbox)

# Function to pause until a button is pressed
def keyPress():
    press = True
    while press == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                press = False

# Draw how many shields the person has in the top right of the screen
def drawNumberOfShields(number_of_shields):
    number = 400
    for i in range(number_of_shields):
        number += 60
        shield_surface = pygame.transform.scale(shieldImage, (50, 50))
        canvas.blit(shield_surface, ((WIDTH/2) + number, 15))

# Create the properties of the enemies
def createEnemy(enemyMaxSize, enemyMinSize, enemyMaxSpeed, enemyMinSpeed):
    enemies = []
    size = random.randint(enemyMinSize, enemyMaxSize)
    velocity = random.randint(enemyMinSpeed, enemyMaxSpeed)
    surface = pygame.transform.scale(enemyImage, (size, size))
    x = random.randint(0, (WIDTH - size))
    y = 0 - size
    isRotating = False
    RotatingDirection = 0
    HitDirection = ""
    enemies = [x, y, velocity, surface, size, isRotating, RotatingDirection, HitDirection]
    return enemies

# Draw enemies falling, and if hit by the forcefield rotate them in the direction specified
def drawEnemy(enemies):
    for i in enemies:
        if i[7] == "R":
            i[6] += 10
        elif i[7] == "L":
            i[6] -= 10
        canvas.blit(pygame.transform.rotate((i[3]), i[6]), (i[0], i[1]))

# Test for enemies hitting the player, only return Collision if they enemy is not rotating
def CollisionTest(player_x, player_y, enemies):
    Collision = False
    for i in enemies:
        # Made the hitboxes smaller to compensate for the corners of the androids counting as a hit
        if player_x + (i[4] * 0.1) <= i[0] <= player_x + (92 - i[4] * 0.1) or player_x + (i[4] * 0.1) <= i[0] + i[4] <= player_x + (92 - i[4] * 0.1):
            if player_y + (i[4] * 0.1) <= i[1] <= player_y + (96 - i[4] * 0.1) or player_y + (i[4] * 0.1) <= i[1] + i[4] <= player_y + (96 - i[4] * 0.1):
                if i[5] == False:
                    Collision = True
    return Collision

# Test for collision for the forcefield, whenever collision is detected, a direction
# for rotating is assigned, also gives 5 extra points for hitting enemies with the shield
def ForceFieldCollision():
    global score
    global enemies
    Collision = False
    ShieldRadius = 70
    ShieldPos = (player_x - 46, player_y - 48)
    for i in enemies:
# Tried to use circle to rectangle collision
# Hit boxes were very off and decided to use rectangle to rectangle
##        a = abs((i[0] - i[4]) - (ShieldPos[0]))
##        b = abs((i[1] - i[4]) - (ShieldPos[1]))
##        c = math.sqrt(a**2 + b**2)
##        if c <= (i[4] / 2) + ShieldRadius:
##            Collision = True
        if ShieldPos[0] + 30 <= i[0] <= ShieldPos[0] + 150 or ShieldPos[0] + 30 <= i[0] + i[4] <= ShieldPos[0] + 150:
            if ShieldPos[1] + 30 <= i[1] <= ShieldPos[1] + 150 or ShieldPos[1] + 30 <= i[1] + i[4] <= ShieldPos[1] + 150:
                Collision = True
                if i[5] == False:
                    score += 5
                    if i[0] < ShieldPos[0] + 100:
                        i[7] = "L"
                    else:
                        i[7] = "R"
                i[5] = True
    return Collision

# Print the score in the top left with a string and the score variable
def printScore(score):
    printText("Score: %s" % (score), score_font, canvas, 25, 25)

# Open the scores.txt file and finds the highest score with the corresponding
# name, if the current players score is higher, that becomes the new highscore
def readInHighScore(file):
    file = open(file, "r")
    scores = file.readlines()
    file.close
    highscore = 0
    highscore_name = ""

    for line in scores:
        name, score = line.strip().split(",")
        score = int(score)
        if score > highscore:
            highscore = score
            highscore_name = name
    return highscore_name, highscore

# Prints the player's score and name into the file
def recordScore(file, name, score):
    scores = open(file, "a")
    print(name+",", score, file = scores)
    scores.close()

# Asks the player to input their name to save their score, only save if they
# type at least 1 character
def HighScore(file, score):
    highscore_name, highscore = readInHighScore("scores.txt")
    if score > highscore:
        name = inputbox.ask(canvas, "NEW HIGH SCORE! Enter your name")
    elif score == highscore:
        name = inputbox.ask(canvas, "YOU TIED THE HIGH SCORE! Enter your name")
    elif score < highscore:
        name = inputbox.ask(canvas, "Enter your name")
    if name == None or len(name) == 0:
        return

    recordScore("scores.txt", name, score)
    return

# Prints the highscore on the play screen right under the score
def printHighScore():
    file = open("scores.txt")
    scores = file.readlines()
    allscores = []
    for line in scores:
        seperator = line.index(",")
        score = int(line[seperator+1:-1])
        allscores.append((score))
    file.close
    allscores.sort()
    highscore = allscores[-1]

    printText("High score: %s" % (highscore), score_font, canvas, 25, 55)

# Increase the difficulty when the player reachs certain score increments
def DifficultyIncrease():
    global enemyMaxSize
    global enemyMinSize
    global enemyMinSpeed
    global enemyMaxSpeed
    global enemyImage
    global enemySpawnRate

    if score > 1000:
        enemyMaxSize = 120
        enemyMinSize = 60
        enemyMinSpeed = 8
        enemyMaxSpeed = 12
        enemySpawnRate = 10
        enemyImage = enemyPhase5
    elif 1000 > score > 500:
        enemyMaxSize = 110
        enemyMinSize = 50
        enemyMinSpeed = 6
        enemyMaxSpeed = 11
        enemySpawnRate = 11
        enemyImage = enemyPhase4
    elif 500 > score > 250:
        enemyMaxSize = 100
        enemyMinSize = 40
        enemyMinSpeed = 5
        enemyMaxSpeed = 10
        enemySpawnRate = 12
        enemyImage = enemyPhase3
    elif 250 > score > 100:
        enemyMinSpeed = 4
        enemyMaxSpeed = 9
        enemyImage = enemyPhase2

# Draw the scoreboard for the top10 scores and names
def drawTop10():
    file = open("scores.txt")
    scores = file.readlines()
    allscores = []

    for line in scores:
        seperator = line.index(",")
        name = line[:seperator]
        score = int(line[seperator+1:-1])
        allscores.append((score, name))
    file.close
    allscores.sort()
    top10 = allscores[-10:]

    title = score_font.render("HIGHSCORES", True, WHITE)
    titlebox = title.get_rect(center=(WIDTH//2, 250))
    canvas.blit(title, titlebox)

    for i, e in enumerate(top10):
        number = str(i + 1)
        text_surface = score_font.render(e[1] + " - " + str(e[0]), True, WHITE)
        number_surface = score_font.render(number, True, WHITE)
        textbox = text_surface.get_rect(center=(WIDTH//2, (HEIGHT/2 + 170)-30*i))
        numberbox = number_surface.get_rect(center=(WIDTH//2 - 200, 30*i+(HEIGHT/4 + 90)))
        canvas.blit(number_surface, numberbox)
        canvas.blit(text_surface, textbox)

# Function to detect a click for a rectangular button
def buttonPress(x, y, x_width, y_width, mousePos):
    isClick = False
    if mousePos[0] >= x and mousePos[1] >= y:
        if mousePos[0] <= x + x_width and mousePos[1] <= y + y_width:
            isClick = True
    return isClick

# Redraw the game window
def redraw_game_window():
    canvas.fill(BLACK)
    drawPlayer(player_x, player_y)
    DifficultyIncrease()
    printScore(score)
    printHighScore()
    printText("Shields:", score_font, canvas,(WIDTH/2) + 350, 25)
    drawNumberOfShields(number_of_forcefields)
    if number_of_enemies > 0:
        drawEnemy(enemies)
    # Make the forcefield flash when it is about to be over
    if ForceField == True:
        if tickClock - forcefield_start <= 4300:
            ForceFieldOn()
        else:
            if 4400 <= tickClock - forcefield_start <= 4500:
                ForceFieldOn()
            if 4600 <= tickClock - forcefield_start <= 4700:
                ForceFieldOn()
            if 4800 <= tickClock - forcefield_start <= 4900:
                ForceFieldOn()
            if 4950 <= tickClock - forcefield_start <= 4999:
                ForceFieldOn()
    pygame.display.update()

# Main game
inGame = True
while inGame:

    # Start Screen
    canvas.fill(BLACK)
    pygame.mouse.set_visible(False)
    player_x = WIDTH / 2 - 50
    player_y = HEIGHT / 2 + 100
    drawPlayer(player_x, player_y)
    printText("Windows Avoider", title_font, canvas, (WIDTH/3), (HEIGHT/3) - 100)
    printText("Press a key to continue", press_font, canvas, (WIDTH/3), (HEIGHT/3) + 50)
    pygame.display.update()
    MenuMusic.play()
    keyPress()
    MenuMusic.stop()
    inGameMusic.play()

    # Starting variables
    enemyImage = enemyPhase1
    enemyMaxSize = 90
    enemyMinSize = 30
    enemyMinSpeed = 3
    enemyMaxSpeed = 8
    enemySpawnRate = 13
    number_of_enemies = 0
    enemyAddRate = 0
    pygame.time.delay(100)
    inPlay = True
    number_of_enemies = 0
    enemies = []
    score = 0
    ForceField = False
    number_of_forcefields = 3

    # Play screen
    while inPlay:
        redraw_game_window()
        pygame.time.delay(10)
        # Counts the ticks while in the play screen
        tickClock = pygame.time.get_ticks()
        #------------------------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
                    inGame = False
                # Activate the shield using "e"
                if event.key == pygame.K_e:
                    if ForceField == False and number_of_forcefields > 0:
                        ForceField = True
                        number_of_forcefields -= 1
                        forcefield_start = pygame.time.get_ticks()
        # Makes the Forcefield last 5 seconds (5000 ticks)
        if ForceField == True:
            if tickClock - forcefield_start >= 5000:
                ForceField = False
            ForceFieldCollision()

        # Makes a true/false value for moving around with arrow keys or wasd
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if player_x > 0:
                player_x = player_x - V_PLAYER
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if player_x < WIDTH - 100:
                player_x = player_x + V_PLAYER
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if player_y > 0:
                player_y = player_y - V_PLAYER
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if player_y < HEIGHT - 100:
                player_y = player_y + V_PLAYER

        # Regulates and spawns enemies
        if enemyAddRate < enemySpawnRate:
            enemyAddRate += 1
        if enemyAddRate == enemySpawnRate:
            enemyAddRate = 0
            number_of_enemies += 1
            newEnemy = createEnemy(enemyMaxSize, enemyMinSize, enemyMaxSpeed, enemyMinSpeed)
            enemies.append(newEnemy)

        # Move the enemies
        for i in enemies:
            if i[5] == False:
                i[1] += i[2]
            if i[6] <= -10:
                i[0] -= 20
            elif i[6] >= 10:
                i[0] += 20

        # Test for Collision
        testCollision = CollisionTest(player_x, player_y, enemies)
        if testCollision == True and ForceField == False:
            inGameMusic.stop()
            DeathSound.play()
            pygame.time.delay(3000)
            inPlay = False

        # Remove the enemies when they fall out of the screen
        for i in enemies:
            if i[1] > HEIGHT + 100:
                enemies.remove(i)
                score += 1

            if i[0] > WIDTH + i[4] or i[0] < 0 - i[4]:
                enemies.remove(i)

    # Game over screen
    inGameMusic.stop()
    gameOverMusic.play()
    pygame.mouse.set_visible(True)
    canvas.fill(BLACK)
    printText("Game Over", title_font, canvas, (WIDTH/3) + 100, 60)
    pygame.display.update()
    pygame.time.delay(500)
    # Input your name to save score
    HighScore("scores.txt", score)
    pygame.display.update()
    pygame.time.delay(500)
    # Display the top 10 scores w/ the names
    drawTop10()
    pygame.display.update()
    pygame.time.delay(500)
    pygame.draw.rect(canvas, GREEN, [(WIDTH/3) + 120, (HEIGHT/3) + 340, 240, 55], 0)
    printText("Play Again?", press_font, canvas, (WIDTH/3) + 130, (HEIGHT/3) + 350)
    pygame.draw.rect(canvas, RED, [(WIDTH/2) - 40, (HEIGHT/3) + 410, 100, 55], 0)
    printText("Exit", press_font, canvas, (WIDTH/2) - 30, (HEIGHT/3) + 420)
    pygame.display.update()

    # Quit the game using ESC, play again using SPACE
    press = True
    while press:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                PlayAgainPressed = buttonPress(WIDTH/3 + 120, HEIGHT/3 + 340, 240, 55, mousePos)
                ExitPressed = buttonPress(WIDTH/2 - 40, HEIGHT/3 + 410, 100, 55, mousePos)
                if PlayAgainPressed:
                    press = False
                if ExitPressed:
                    press = False
                    inGame = False
    gameOverMusic.stop()
    pygame.time.delay(100)

#pygame.quit()
