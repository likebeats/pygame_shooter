from pygame.locals import *
from random import randint
from AnimatedSprite import *

class Game(object):
    def __init__(self):
        object.__init__(self)
        
        self.gameWidth = 600
        self.gameHeight = 700
        self.fps = 60
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.gameGrid = pygame.display.set_mode((self.gameWidth, self.gameHeight))
        pygame.display.set_caption('SC Shooter')
        
        self.moveSpeed = 4
        self.enemySpeed = 2
        self.bgSpeed = 1
        self.spawnTime = 8
        self.spawnCount = 0
        self.shotSpeed = 13
        self.laserWidth = 3
        self.laserHeight = 13
        self.maxhealth = 100
        self.score = 0
        
        self.healthBarBorder = 3
        self.healthBarWidth  = 175
        self.healthBarHeight = 30
        
        self.ship = pygame.image.load('images/ship2.png').convert_alpha()
        self.bgImage = pygame.image.load('images/bg.png').convert_alpha()
        self.enemyShip = pygame.image.load('images/enemy2.png').convert_alpha()
        self.heartIcon = pygame.image.load('images/heart_icon.png').convert_alpha()
        
        self.panel()
        self.reset()
        
        pygame.display.update()
        
        self.enemy_expl_imgs = self.load_sliced_sprites(56, 56, 'images/explosion-sprite.png')
        
    def load_sliced_sprites(self, w, h, filename):
        images = []
        master_image = pygame.image.load(os.path.join('', filename)).convert_alpha()
        
        master_width, master_height = master_image.get_size()
        for i in xrange(int(master_width/w)):
            images.append(master_image.subsurface((i*w,0,w,h)))
        return images
    
    def play(self):
        self.gameLoop()
    
    def reset(self):
        self.is_dead = False
        
        # reset variables
        self.shots = []
        self.enemies = []
        self.bgs = []
        self.sprites = []
        self.setHealth(self.maxhealth)
        self.moveLeft = self.moveUp = self.moveDown = self.moveRight = False
        self.score = 0
        
        # postion player ship
        self.shipRect = self.ship.get_rect()
        self.shipRect.midbottom = (self.gameWidth/2, self.gameHeight-50)
        
        #arrange backgrounds
        for i in range(3):
            newBg = {'image': self.bgImage, 'rect': self.bgImage.get_rect()}
            newBg['rect'].topleft = (0,(-i*newBg['rect'].height))
            self.bgs.append(newBg)
    
    # show score screen
    def game_over(self):
        self.moveLeft = self.moveUp = self.moveDown = self.moveRight = False
        
        font = pygame.font.SysFont(None, 48)
        loseText = font.render("You Died :(", True, (0,0,0))
        loseRect = loseText.get_rect()
        loseRect.centerx = self.gameWidth/2
        loseRect.centery = (self.gameHeight/2)-50
        self.gameGrid.blit(loseText, loseRect)
        
        font = pygame.font.SysFont(None, 26)
        retryText = font.render("Press r to retry", True, (0,0,0))
        retryRect = retryText.get_rect()
        retryRect.midtop = (self.gameWidth/2, loseRect.bottom + 10)
        self.gameGrid.blit(retryText, retryRect)
        
        font = pygame.font.SysFont(None,40)
        scoreText = font.render("Final Score:", True, (0,0,0))
        score2Text = font.render(str(self.score), True, (0,0,0))
        scoreRect = scoreText.get_rect()
        score2Rect = score2Text.get_rect()
        scoreRect.midtop = (self.gameWidth/2, retryRect.bottom + 70)
        score2Rect.midtop = (self.gameWidth/2, scoreRect.bottom + 5)
        self.gameGrid.blit(scoreText, scoreRect)
        self.gameGrid.blit(score2Text, score2Rect)
        
    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()
    
    def setHealth(self, health):
        if (health > 0):
            self.health = health
            self.healthBar.width = (health * self.healthBarWidth) / self.maxhealth
            self.panelUpdate()
        else:
            self.health = 0
            self.healthBar.width = 0
            self.is_dead = True
            
    def createShot(self):
        newShot = pygame.Rect(0,0,self.laserWidth,self.laserHeight)
        newShot.topleft = (self.shipRect.left, self.shipRect.top)
        self.shots.append(newShot)
        
        newShot2 = pygame.Rect(0,0,self.laserWidth,self.laserHeight)
        newShot2.topright = (self.shipRect.left+self.shipRect.width, self.shipRect.top)
        self.shots.append(newShot2)
    
    def spawnEnemy(self):
        randomX = randint(1, self.gameWidth)
        newEnemy = {'image': self.enemyShip, 'rect': self.enemyShip.get_rect()}
        newEnemy['rect'].midbottom = (randomX, -newEnemy['rect'].height)
        self.enemies.append(newEnemy)
    
    # check ship collision
    def checkShipHit(self, shipRect, enemies):
        for e in enemies:
            if shipRect.colliderect(e['rect']):
                return e
        return False
    
    # check bullet collision
    def checkBulletHit(self, enemy, shots):
        for s in shots:
            if enemy['rect'].colliderect(s):
                return s
        return False
    
    def shipHitConfirmed(self):
        self.setHealth(self.health-10)
    
    def makeExplosion(self, rect, imgs):
        explosion = AnimatedSprite(imgs, 15)
        explosion.location = (rect.centerx, rect.centery)
        self.sprites.append(explosion)
                
    def panel(self):
        self.heartIconRect = self.heartIcon.get_rect()
        self.healthBar = pygame.Rect(0,0,self.healthBarWidth,self.healthBarHeight)
        self.healthBarBg = pygame.Rect(0,0,self.healthBarWidth,self.healthBarHeight)
        self.healthBarBg.bottomleft = (10,self.gameHeight-10)
        self.heartIconRect.center = (self.healthBarBg.left+15, self.healthBarBg.centery)
        self.healthBar.topright = self.healthBarBg.topright
        
        self.healthBarBorderTop               = pygame.Rect(0,0,self.healthBar.width,self.healthBarBorder)
        self.healthBarBorderTop.topleft       = (self.healthBar.left, self.healthBar.top)
        self.healthBarBorderRight             = pygame.Rect(0,0,self.healthBarBorder,self.healthBar.height)
        self.healthBarBorderRight.topright    = (self.healthBar.left+self.healthBar.width, self.healthBar.top)
        self.healthBarBorderBottom            = pygame.Rect(0,0,self.healthBar.width,self.healthBarBorder)
        self.healthBarBorderBottom.bottomleft = (self.healthBar.left, self.healthBar.top+self.healthBar.height)
        self.healthBarBorderLeft              = pygame.Rect(0,0,self.healthBarBorder,self.healthBar.height)
        self.healthBarBorderLeft.topleft      = (self.healthBar.left, self.healthBar.top)
        
    def panelUpdate(self):
        pygame.draw.rect(self.gameGrid, (255,255,255), self.healthBarBg)
        if self.is_dead == False:
            pygame.draw.rect(self.gameGrid, (255,0,0), self.healthBar)
            self.healthBar.topright = self.healthBarBg.topright
        pygame.draw.rect(self.gameGrid, (0,0,0), self.healthBarBorderTop)
        pygame.draw.rect(self.gameGrid, (0,0,0), self.healthBarBorderRight)
        pygame.draw.rect(self.gameGrid, (0,0,0), self.healthBarBorderBottom)
        pygame.draw.rect(self.gameGrid, (0,0,0), self.healthBarBorderLeft)
        self.gameGrid.blit(self.heartIcon, self.heartIconRect)
        
        font = pygame.font.SysFont(None,30)
        scoreText = font.render("Score: "+str(self.score), True, (0,0,0))
        scoreRect = scoreText.get_rect()
        scoreRect.bottomright = (self.gameWidth-10, self.gameHeight-10)
        self.gameGrid.blit(scoreText, scoreRect)
        
    def gameLoop(self):
        self.running = True
        while self.running:
            # set fps
            self.clock.tick(self.fps)
            
            # get keys the player is pressing
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == KEYDOWN:
                    if self.is_dead == False:
                        if event.key == K_LEFT or event.key == ord('a'):
                            self.moveLeft = True
                        if event.key == K_UP or event.key == ord('w'):
                            self.moveUp = True
                        if event.key == K_DOWN or event.key == ord('s'):
                            self.moveDown = True
                        if event.key == K_RIGHT or event.key == ord('d'):
                            self.moveRight = True
                        if event.key == K_SPACE:
                            self.createShot()
                    else:
                        if event.key == ord('r'):
                            self.reset()
                if event.type == KEYUP:
                    if self.is_dead == False:
                        if event.key == K_LEFT or event.key == ord('a'):
                            self.moveLeft = False
                        if event.key == K_UP or event.key == ord('w'):
                            self.moveUp = False
                        if event.key == K_DOWN or event.key == ord('s'):
                            self.moveDown = False
                        if event.key == K_RIGHT or event.key == ord('d'):
                            self.moveRight = False
            
            # clear screen
            self.gameGrid.fill((0,0,0))
            
            # move background
            for i in range(len(self.bgs)):
                if (self.bgs[i]['rect'].top > (self.gameHeight+(self.bgs[i]['rect'].height/2))):
                    if (i == 0): next = 2
                    elif (i == 1): next = 0
                    elif (i == 2): next = 1
                    self.bgs[i]['rect'].bottom = self.bgs[next]['rect'].top
                if self.is_dead == False:
                    self.bgs[i]['rect'].top += self.bgSpeed
                self.gameGrid.blit(self.bgs[i]['image'], self.bgs[i]['rect'])
            
            # spawn enemies
            if self.is_dead == False:
                self.spawnCount += 1
                if (self.spawnCount == self.spawnTime):
                    self.spawnEnemy()
                    self.spawnCount = 0
            
            # move bullets
            for s in self.shots:
                s.top -= self.shotSpeed
                pygame.draw.rect(self.gameGrid, (255,0,0), s)
                if s.top < -s.height:
                    self.shots.remove(s)
            
            # check to see if bullets hit an enemy ship
            for e in self.enemies:
                bulletHit = self.checkBulletHit(e, self.shots)
                if bulletHit and self.is_dead == False: # hit
                    self.score += 10
                    self.makeExplosion(e['rect'],self.enemy_expl_imgs)
                    self.enemies.remove(e)
                    self.shots.remove(bulletHit)
                    continue
                else:   # miss
                    if self.is_dead == False:
                        e['rect'].top += self.enemySpeed
                    self.gameGrid.blit(e['image'], e['rect'])
                    if e['rect'].top > self.gameHeight:
                        self.enemies.remove(e)
            
            # check to see if player ship collides with enemy ships
            shipHit = self.checkShipHit(self.shipRect, self.enemies)
            if shipHit and self.is_dead == False:   # hit
                self.shipHitConfirmed()
                self.makeExplosion(shipHit['rect'],self.enemy_expl_imgs)
                self.enemies.remove(shipHit)
            
            # render all sprites
            for sprite in self.sprites:
                next = sprite.render(self.gameGrid)
                if (next == False):
                    self.sprites.remove(sprite)
            
            # move player ship
            if (self.moveLeft == True) and (self.shipRect.centerx > 0):
                self.shipRect.left -= self.moveSpeed
            if (self.moveUp == True) and (self.shipRect.centery > 0):
                self.shipRect.top -= self.moveSpeed
            if (self.moveDown == True) and (self.shipRect.centery < self.gameHeight):
                self.shipRect.top += self.moveSpeed
            if (self.moveRight == True) and (self.shipRect.centerx < self.gameWidth):
                self.shipRect.left += self.moveSpeed
            
            # is the player dead?
            if self.is_dead == True:
                self.game_over()
            
            self.gameGrid.blit(self.ship, self.shipRect)
            self.panelUpdate()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.play()