import pygame, random, sys
from pygame.locals import *

windowWidth = 600
windowHeight = 600
textColor = (0, 0, 255)
backgroundColor = (0, 0, 0)
FPS = 20
tankSize = 25
tankMinSpeed = 8
tankMaxSpeed = 10
add_mg_Rate = 700
tonicSize = 40
tonicMinSpeed = 4
tonicMaxSpeed = 5
addTonicRate = 45
asteroidMinSize = 20
asteroidMaxSize = 40
asteroidMinSpeed = 2
asteroidMaxSpeed = 8
addNewAsteroidRate = 6
playerMoveRate = 5
MaxLife = 9
SMaxLife = 12
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitAsteroid(playerRect, asteroids):
    for a in asteroids:
        if playerRect.colliderect(a['rect']):
            asteroids.remove(a)
            return True
    return False

def playerHasHitMegaTank(playerRect, MTanks):
    for m in MTanks:
        if playerRect.colliderect(m['rect']):
            MTanks.remove(m)
            return True
    return False

def playerHasHitTonic(playerRect, tonics):
    for t in tonics:
        if playerRect.colliderect(t['rect']):
            tonics.remove(t)
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Asteroid')

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')
pickUpTonicSound = pygame.mixer.Sound('smw_1-up.wav')
gotHitByAsteroid = pygame.mixer.Sound('0477.wav')

# Set up images.
playerImage = pygame.image.load('clipart35059.png')
playerStrechedImage = pygame.transform.scale(playerImage, (35, 35))
playerRect = playerStrechedImage.get_rect()
asteroidImage = pygame.image.load('asteroid.png')
tonicImage = pygame.image.load('Energy_Tank.png')
megaTankImage = pygame.image.load('mega_tank.png')

# Show the "Start" screen.
windowSurface.fill(backgroundColor)
drawText('Asteroid', font, windowSurface, (windowWidth / 3),
       (windowHeight / 3))
drawText('Press a key to start.', font, windowSurface,
       (windowWidth / 3) - 30, (windowHeight / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    asteroids = []
    tonics = []
    MTanks = []
    score = 0
    life = 1
    playerRect.topleft = (windowWidth / 2, windowHeight - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    tonicAddCounter = 0
    asteroidAddCounter = 0
    tankAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

        # Add new asteroids at the right of the screen
        if not reverseCheat and not slowCheat:
            asteroidAddCounter += 1
        if asteroidAddCounter == addNewAsteroidRate:
            asteroidAddCounter = 0
            asteroidSize = random.randint(asteroidMinSize, asteroidMaxSize)
            newAsteroid = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - asteroidSize), asteroidSize, asteroidSize),
                         'speed': random.randint(asteroidMinSpeed, asteroidMaxSpeed),
                         'surface':pygame.transform.scale(asteroidImage, (asteroidSize, asteroidSize)),}

            asteroids.append(newAsteroid)
        
        # Add new tonics at the right of the screen
        if not reverseCheat and not slowCheat:
            tonicAddCounter += 1
        if tonicAddCounter == addTonicRate:
            tonicAddCounter = 0
            tonicSize = tonicSize
            newTonic = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - tonicSize), tonicSize, tonicSize),
                        'speed': random.randint(tonicMinSpeed, tonicMaxSpeed),
                        'surface':pygame.transform.scale(tonicImage, (tonicSize, tonicSize)),}
            
            tonics.append(newTonic)

        # Add new mega tanks at the right of the screen
        if not reverseCheat and not slowCheat:
            tankAddCounter += 1
        if tankAddCounter == add_mg_Rate:
            tankAddCounter = 0
            tankSize = tankSize
            newTank = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - tankSize), tankSize, tankSize),
                       'speed': random.randint(tankMinSpeed, tankMaxSpeed),
                       'surface': pygame.transform.scale(megaTankImage, (tankSize, tankSize)),}

            MTanks.append(newTank)
            
        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * playerMoveRate, 0)
        if moveRight and playerRect.right < windowWidth:
            playerRect.move_ip(playerMoveRate, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * playerMoveRate)
        if moveDown and playerRect.bottom < windowHeight:
            playerRect.move_ip(0, playerMoveRate)

        # Move the asteroids left
        for a in asteroids:
            if not reverseCheat and not slowCheat:
                a['rect'].move_ip(-a['speed'], 0)
            elif reverseCheat:
                a['rect'].move_ip(5, 0)
            elif slowCheat:
                a['rect'].move_ip(-1, 0)
                
        # Move the tonics left
        for t in tonics:
            if not reverseCheat and not slowCheat:
                t['rect'].move_ip(-t['speed'], 0)
            elif reverseCheat:
                t['rect'].move_ip(5, 0)
            elif slowCheat:
                t['rect'].move_ip(-1, 0)

        # Move the tanks left
        for m in MTanks:
            if not reverseCheat and not slowCheat:
                m['rect'].move_ip(-m['speed'], 0)
            elif reverseCheat:
                m['rect'].move_ip(5, 0)
            elif slowCheat:
                m['rect'].move_ip(-1, 0)
            
        
        # Delete asteroids that have fallen past the bottom.
        for a in asteroids[:]:
            if a['rect'].left < 0:
                asteroids.remove(a)
        
        # Delete tonics that have fallen past the bottom
        for t in tonics[:]:
            if t['rect'].left < 0:
                tonics.remove(t)

        # Delete tanks that have fallen past the bottom
        for m in MTanks[:]:
            if m['rect'].left < 0:
                MTanks.remove(m)

        # Draw the game world on the window.
        windowSurface.fill(backgroundColor)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,
               10, 40)
        drawText('Life: %s' % (life), font, windowSurface, 10, 80)

        # Draw the player's rectangle.
        windowSurface.blit(playerStrechedImage, playerRect)

        # Draw each baddie.
        for a in asteroids:
            windowSurface.blit(a['surface'], a['rect'])

        pygame.display.update()
        
        # Draw each tonic
        for t in tonics:
            windowSurface.blit(t['surface'], t['rect'])
           
        pygame.display.update()

        # Draw each mega tank
        for m in MTanks:
            windowSurface.blit(m['surface'], m['rect'])

        pygame.display.update()

        # Check if any of the tonics have hit the player
        if playerHasHitTonic(playerRect, tonics):
            pickUpTonicSound.play()
            score += 50
            if life < MaxLife:
                life += 1
                
                

        # Check if any of the asteroids have hit the player.
        if playerHasHitAsteroid(playerRect, asteroids):
            score -= 10
            life -= 1
            gotHitByAsteroid.play()
            if life <= 0:
                if score > topScore:
                    topScore = score # Set new top score.
                break

        # Check if player has hit a mega tank
        if playerHasHitMegaTank(playerRect, MTanks):
            score += 1000
            life += 3
            if life <= SMaxLife:
                life = life 
            
        mainClock.tick(FPS)
        

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (windowWidth / 3),
           (windowHeight / 3))
    drawText('Press a key to play again.', font, windowSurface,
           (windowWidth / 3) - 80, (windowHeight / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

gameOverSound.stop()
