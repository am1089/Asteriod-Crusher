import pygame, random, sys
from pygame.locals import *

windowWidth = 600
windowHeight = 600
textColor = (0, 0, 255)
backgroundColor = (0, 0, 0)
FPS = 40
playerMoveRate = 5
MaxLife = 9
SuperMaxLife = 12

class constantSize(object):
    def __init__(self, Size, MinSpeed, MaxSpeed, addRate):
        self.Size = Size
        self.MinSpeed = MinSpeed
        self.MaxSpeed = MaxSpeed
        self.addRate = addRate

class inconstantSize(object):
    def __init__(self, MinSize, MaxSize, MinSpeed, MaxSpeed, addRate):
        self.MinSize = MinSize
        self.MaxSize = MaxSize
        self.MinSpeed = MinSpeed
        self.MaxSpeed = MaxSpeed
        self.addRate = addRate

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

def playerHasHitBigShroom(playerRect, BigShrooms):
    for b in BigShrooms:
        if playerRect.colliderect(b['rect']):
            BigShrooms.remove(b)
            return True
    return False

def playerHasHitTonic(playerRect, tonics):
    for t in tonics:
        if playerRect.colliderect(t['rect']):
            tonics.remove(t)
            return True
    return False

def playerHasHitSmallShroom(playerRect, SmallShrooms):
    for s in SmallShrooms:
        if playerRect.colliderect(s['rect']):
            SmallShrooms.remove(s)
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Set up pygame and the window
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
gotHitByMT = pygame.mixer.Sound('cheering.wav')
gotHitByBigShroom = pygame.mixer.Sound('blip.wav')
gotHitBySmallShroom = pygame.mixer.Sound('blurp.wav')

# Set up images
player = pygame.Rect(300, 100, 35, 35)
playerImage = pygame.image.load('player-1.png')
playerStrechedImage = pygame.transform.scale(playerImage, (35, 35))
playerRect = playerStrechedImage.get_rect()
asteroidImage = pygame.image.load('asteroid.png')
tonicImage = pygame.image.load('Energy_Tank.png')
megaTankImage = pygame.image.load('mega_tank.png')
BigShroomImage = pygame.image.load('BigShroom.png')
SmallShroomImage = pygame.image.load('SmallShroom.png')

# Show the "Start" screen.
windowSurface.fill(backgroundColor)
drawText('Asteroid', font, windowSurface, (windowWidth / 3),
       (windowHeight / 3))
drawText('Press a key to start.', font, windowSurface,
       (windowWidth / 3) - 30, (windowHeight / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
tank = constantSize(25, 8, 10, 500)
tonic = constantSize(30, 4, 5, 25)
asteroid = inconstantSize(20, 40 , 2, 8, 10)
BigShroom = constantSize(25, 3, 5, 60)
SmallShroom = constantSize(25, 4, 5, 60)
while True:
    # Set up the start of the game.
    asteroids = []
    tonics = []
    MTanks = []
    BigShrooms = []
    SmallShrooms = []
    score = 0
    life = 1
    playerRect.topleft = (windowWidth / 2, windowHeight - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    tonicAddCounter = 0
    asteroidAddCounter = 0
    tankAddCounter = 0
    bigShroomAddCounter = 0
    smallShroomAddCounter = 0
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
        if asteroidAddCounter == asteroid.addRate:
            asteroidAddCounter = 0
            asteroidSize = random.randint(asteroid.MinSize, asteroid.MaxSize)
            newAsteroid = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - asteroidSize), asteroidSize, asteroidSize),
                         'speed': random.randint(asteroid.MinSpeed, asteroid.MaxSpeed),
                         'surface':pygame.transform.scale(asteroidImage, (asteroidSize, asteroidSize)),}

            asteroids.append(newAsteroid)
        
        # Add new tonics at the right of the screen
        if not reverseCheat and not slowCheat:
            tonicAddCounter += 1
        if tonicAddCounter == tonic.addRate:
            tonicAddCounter = 0
            newTonic = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - tonic.Size), tonic.Size, tonic.Size),
                        'speed': random.randint(tonic.MinSpeed, tonic.MaxSpeed),
                        'surface':pygame.transform.scale(tonicImage, (tonic.Size, tonic.Size)),}
            
            tonics.append(newTonic)

        # Add new mega tanks at the right of the screen
        if not reverseCheat and not slowCheat:
            tankAddCounter += 1
        if tankAddCounter == tank.addRate:
            tankAddCounter = 0
            newTank = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - tank.Size), tank.Size, tank.Size),
                       'speed': random.randint(tank.MinSpeed, tank.MaxSpeed),
                       'surface': pygame.transform.scale(megaTankImage, (tank.Size, tank.Size)),}

            MTanks.append(newTank)

        # Add new Bigshrooms at the right of the screen
        if not reverseCheat and not slowCheat:
            bigShroomAddCounter += 1
        if bigShroomAddCounter == BigShroom.addRate:
            bigShroomAddCounter = 0
            newBigShroom = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - BigShroom.Size), BigShroom.Size, BigShroom.Size),
                            'speed': random.randint(BigShroom.MinSpeed, BigShroom.MaxSpeed),
                            'surface': pygame.transform.scale(BigShroomImage, (BigShroom.Size, BigShroom.Size)),}

            BigShrooms.append(newBigShroom)

        # Add new SmallShrooms at the right of the screen
        if not reverseCheat and not slowCheat:
            smallShroomAddCounter += 1
        if smallShroomAddCounter == SmallShroom.addRate:
            smallShroomAddCounter = 0
            newSmallShroom = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - SmallShroom.Size), SmallShroom.Size, SmallShroom.Size),
                              'speed': random.randint(SmallShroom.MinSpeed, SmallShroom.MaxSpeed),
                              'surface': pygame.transform.scale(SmallShroomImage, (SmallShroom.Size, SmallShroom.Size)),}
            
            SmallShrooms.append(newSmallShroom)
            
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

        # Move the Bigshrooms left
        for b in BigShrooms:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(-b['speed'], 0)
            elif reverseCheat:
                b['rect'].move_ip(5, 0)
            elif slowCheat:
                b['rect'].move_ip(-1, 0)

        # Move Smallshrooms left
        for s in SmallShrooms:
            if not reverseCheat and not slowCheat:
                s['rect'].move_ip(-s['speed'], 0)
            elif reverseCheat:
                s['rect'].move_ip(5, 0)
            elif slowCheat:
                s['rect'].move_ip(-1, 0)
        
        # Delete asteroids that have fallen past the left of the screen.
        for a in asteroids[:]:
            if a['rect'].left < 0:
                asteroids.remove(a)
        
        # Delete tonics that have fallen past the left of the screen
        for t in tonics[:]:
            if t['rect'].left < 0:
                tonics.remove(t)

        # Delete tanks that have fallen past the left of the screen
        for m in MTanks[:]:
            if m['rect'].left < 0:
                MTanks.remove(m)

        # Delete BigShrooms that have fallen past the left of the screen
        for b in BigShrooms[:]:
            if b['rect'].left < 0:
                BigShrooms.remove(b)

        # Delete Smallshrooms that have fallen past the left of the screen
        for s in SmallShrooms[:]:
            if s['rect'].left < 0:
                SmallShrooms.remove(s)
        
        # Draw the game world on the window.
        windowSurface.fill(backgroundColor)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,
               10, 40)
        drawText('Life: %s' % (life), font, windowSurface, 10, 80)

        # Draw the player's rectangle.
        windowSurface.blit(playerStrechedImage, playerRect)

        # Draw each asteroid.
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

        # Draw each Bigshroom
        for b in BigShrooms:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Draw each SmallShroom
        for s in SmallShrooms:
            windowSurface.blit(s['surface'], s['rect'])

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
            gotHitByMT.play()
            playerMoveRate = 5
            player.height = 35
            player.width = 35
            playerStrechedImage = pygame.transform.scale(playerImage, (player.height, player.width))
            score += 1000
            life += 3
            if life > SuperMaxLife:
                life = SuperMaxLife

        # Check if player has hit Bigshroom
        if playerHasHitBigShroom(playerRect, BigShrooms):
            gotHitByBigShroom.play()
            score += 20
            playerMoveRate -= 1
            player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
            playerStrechedImage = pygame.transform.scale(playerImage, (player.height, player.width))

        if playerHasHitSmallShroom(playerRect, SmallShrooms):
            gotHitBySmallShroom.play()
            score += 20
            playerMoveRate += 1
            player = pygame.Rect(player.left, player.top, player.width - 2, player.height - 2)
            playerStrechedImage = pygame.transform.scale(playerImage, (player.height, player.width))
            
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
