import pygame, sys, random, os
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 150
FPS = 60 #초당 프레임 수

GRAVITY = 0.75

# 배경화면 및 효과음
pygame.mixer.init()
BACKGROUND_SOUND = pygame.mixer.Sound("./sound/background.wav")
OBSTACLE_SOUND = pygame.mixer.Sound("./sound/obstacles.wav")
JUMPING_SOUND = pygame.mixer.Sound("./sound/jumping.wav")
ATTACK_SOUND = pygame.mixer.Sound("./sound/attack.wav")

# 속도
SPEED_GROUND = 6
IMG_GROUND = pygame.image.load('./img/ground.png')

SPEED_SKY = 1
IMG_SKY = pygame.image.load('./img/sky.png')

# 공룡
IMG_TREX = pygame.image.load('./img/tRex_.png')
TIME_CHANGE_TREX = 6
X_TREX = 50
Y_TREX = 105

HIGH_MIN = 90
SPEED_TREX = -12.5

# 익룡
ATTACK = pygame.image.load(os.path.join("img", "isAttack.png"))

# 선인장
IMG_CATUS = pygame.image.load('./img/cactus.png')
Y_CATUS = 100 #선인장 높이?

DISTANCE_MIN = 400 #뭘 의미하지?
DISTANCE_MAX = 600

pygame.init() #라이브러리 초기화
pygame.display.set_caption('T-REX') #게임창 이름
FPSCLOCK = pygame.time.Clock() #초당 프레임 잡는 거
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

class T_Rex():
    def __init__(self, option = 3):
        self.x = X_TREX #초기 좌표
        self.y = Y_TREX #초기 좌표
        self.speed = 0 #스피드 0
        self.img = IMG_TREX # 공룡 이미지
        self.option = option # 매개변수로 받은 option
        self.surface = pygame.Surface((55, 43), pygame.SRCALPHA)
        self.surface.blit(self.img, (0, 0), (80, 0, 40, 43)) #가만히 있는 공룡
        self.timeChange = 0 # 시간 변화
        self.jumping = False #점프
        self.lowering = False #슬라이딩
    
    def update(self, up, down): #상태변화
        self.surface.fill((0, 0, 0, 0)) #투명한 배경
        if not self.jumping: #점프 상태가 아닐 때
            if up: #업 키를 누르면 점핑
                self.jumping = True # 점프 상태가 True
                self.speed = SPEED_TREX #-12.5 점프 높이
            elif down: #아니면 다운 상태임
                self.lowering = True
                # if self.timeChange <= 100: #다운 상태일 때 TIME_CHANGE_TREX
                self.option = 4 #option 은 4
                self.y = 50
                # self.timeChange += 1 #timeChange 값을 계속 변화시킨다.
                # print(self.timeChange)
                # if self.timeChange > 100:
                #     self.timeChange = 0
            else:
                if self.timeChange <= TIME_CHANGE_TREX:
                    self.option = 0
                    self.y = Y_TREX
                else:
                    self.option = 1 # 발구르는거
                self.timeChange += 1
                if self.timeChange > TIME_CHANGE_TREX * 2:
                    self.timeChange = 0
        elif self.jumping: #점프 상태일때
            self.option = 2
            if self.y <= Y_TREX - HIGH_MIN and self.speed < 0 and (not up): #점프 상태도 아니고, y 좌표 위치가 15 보다 작으면 이미 점프 상태
                self.speed = 0
            self.y += int(self.speed + GRAVITY/2)
            self.speed += GRAVITY
            if self.y >= Y_TREX:
                self.jumping = False
                self.y = Y_TREX

        if self.option == 0:
            self.surface.blit(self.img, (0, 0), (0, 0, 40, 43))
        elif self.option == 1:
            self.surface.blit(self.img, (0, 0), (40, 0, 40, 43))
        elif self.option == 2:
            self.surface.blit(self.img, (0, 0), (80, 0, 40, 43))
        elif self.option == 3:
            self.surface.blit(self.img, (0, 0), (120, 0, 40, 43))
        elif self.option == 4:
            self.surface.blit(self.img, (0, 0), (270, 0, 55, 43))
        elif self.option == 5:
            self.surface.blit(self.img, (0, 0), (270, 0, 55, 43))
        
    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

class Catus():
    def __init__(self, x, y, option):
        self.x = x
        self.y = y
        self.option = option
        self.img = IMG_CATUS
        self.rect = [0, 0, 0, 0]
        if option == 0:
            self.rect = [0, 0, 23, 46]
        elif option == 1:
            self.rect = [0, 0, 47, 46]
        elif option == 2:
            self.rect = [100, 0, 49, 46]
        elif option == 3:
            self.rect = [100, 0, 49, 46]
        elif option == 4:
            self.rect = [25, 0, 73, 46]
        self.surface = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        self.surface.blit(self.img, (0, 0), self.rect)

    
    def update(self, speed):
        self.x -= int(speed)
    
    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

class Bird():
    def __init__(self, x, y, option = 0):
        self.x = x
        self.y = y
        self.option = option
        self.surface = pygame.Surface((42, 36), pygame.SRCALPHA)
        self.timeChange = 0
        self.img = pygame.image.load('./img/bird.png')
    
    def update(self, speed):
        self.surface.fill((0, 0, 0, 0))

        self.x -= int(speed)

        if self.timeChange <= TIME_CHANGE_BIRD:
            self.option = 0
        else:
            self.option = 1
        self.timeChange += 1
        if self.timeChange > TIME_CHANGE_BIRD * 2:
            self.timeChange = 0
        
        if self.option == 0:
            self.surface.blit(self.img, (0, 0), (0, 0, 42, 36))
        elif self.option == 1:
            self.surface.blit(self.img, (0, 0), (42, 0, 42, 36))
    
    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

class ListCatusAndBirds():
    def __init__(self):
        self.list = []
        for i in range(0, 3):
            self.list.append(Catus(500 + WINDOWWIDTH + random.randint(DISTANCE_MIN, DISTANCE_MAX)*i, Y_CATUS, random.randint(0, 3)))
        self.speed = SPEED_GROUND
    
    def update(self, score):
        self.speed = SPEED_GROUND * (1 + score/500)
        if self.speed > SPEED_GROUND * 2:
            self.speed = SPEED_GROUND * 2
        for i in range(len(self.list)):
            self.list[i].update(self.speed)
        
        if self.list[0].x < -132:
            self.list.pop(0)
            if self.speed > SPEED_GROUND * 1.5:
                rand = random.randint(0, 5)
                if rand == 5:
                    self.list.append(Catus(self.list[1].x + random.randint(DISTANCE_MIN + 200, DISTANCE_MAX + 100), Y_CATUS, random.randint(0, 3)))
                else:
                    self.list.append(Catus(self.list[1].x + random.randint(DISTANCE_MIN + 100, DISTANCE_MAX + 100), Y_CATUS, random.randint(0, 4)))
            else:
                self.list.append(Catus(self.list[1].x + random.randint(DISTANCE_MIN, DISTANCE_MAX), Y_CATUS, random.randint(0, 3)))
    
    def draw(self):
        for i in range(len(self.list)):
            self.list[i].draw()

class Ground():
    def __init__(self):
        self.x = 0
        self.y = 138
        self.img = IMG_GROUND
        self.speed = SPEED_GROUND
    
    def update(self, score):
        self.speed = SPEED_GROUND * (1 + score/500)
        if self.speed > SPEED_GROUND * 2:
            self.speed = SPEED_GROUND * 2
        self.x -= int(self.speed)
        if self.x <= -600:
            self.x += 600
    
    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))

class Sky():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = SPEED_SKY
        self.img = IMG_SKY
    
    def update(self, score):
        self.speed = SPEED_SKY * (1 + score/500)
        if self.speed > SPEED_SKY * 2:
            self.speed = SPEED_SKY * 2
        self.x -= int(self.speed)
        if self.x <= -600:
            self.x += 600
    
    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))

class Score():
    def __init__(self):
        self.score = 0
        self.highScore = 0
        self.textScore = ""
        self.textHighScore = ""
        self.size = 15

    def update(self):
        self.score += 0.15
        if self.score > self.highScore:
            self.highScore = int(self.score)

        self.textScore = str(int(self.score))
        for i in range(5 - len(self.textScore)):
            self.textScore = '0' + self.textScore

        self.textHighScore = str(int(self.highScore))
        for i in range(5 - len(self.textHighScore)):
            self.textHighScore = '0' + self.textHighScore
        self.textHighScore = "HI : " + self.textHighScore
    
    def draw(self):
        fontObj = pygame.font.SysFont('consolas', self.size)

        textSurfaceScore = fontObj.render(self.textScore, True, (0, 0, 0))
        DISPLAYSURF.blit(textSurfaceScore, (550, 10))

        textSurfaceHighScore = fontObj.render(self.textHighScore, True, (60, 60, 60))
        DISPLAYSURF.blit(textSurfaceHighScore, (450, 10))

class BlinkText():
    def __init__(self, text):
        self.text = text
        self.timeChange = 0
        self.size = 14
        fontObj = pygame.font.SysFont('consolas', self.size)
        textSurface = fontObj.render(self.text, False, (0, 0, 0))
        self.surface = pygame.Surface(textSurface.get_size()) 
        self.surface.fill((255, 255, 255))
        self.surface.blit(textSurface, (0, 0))
        self.surface.set_colorkey((255, 255, 255))
        self.alpha = 255
    def update(self):
        self.alpha = abs(int(255 - self.timeChange))
        if self.timeChange > 255*2:
            self.timeChange = 0
        self.timeChange += 5

    def draw(self): 
        self.surface.set_alpha(self.alpha)
        DISPLAYSURF.blit(self.surface, (int(WINDOWWIDTH/2 - self.surface.get_width()/2), 100))
        
def isCollision(tRex, ls):
    tRexMask = pygame.mask.from_surface(tRex.surface)
    for catusOrBird in ls.list:
        catusOrBird_mask = pygame.mask.from_surface(catusOrBird.surface)
        result = tRexMask.overlap(catusOrBird_mask, (catusOrBird.x - tRex.x, catusOrBird.y - tRex.y))
        if result:
            return True
    return False

class Attack():
    def __init__(self):
        self.count = 0
    def draw(self):
        DISPLAYSURF.blit(ATTACK, (200, 100))

def main():
    print("""/* =====Dino Jump===== */

// Space to Play, Esc to Exit

// Up to jump, Down to bow down""")
    BACKGROUND_SOUND.play(-1)
    sky = Sky()
    ground = Ground()
    tRex = T_Rex(0)
    up = False
    down = False
    ls = ListCatusAndBirds()
    score = Score()
    attack = Attack()
    change_count = 0
    blinkText = BlinkText("Enter to Play, esc to Exit")
# haven't start yet
    while True:
        isStart = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                isStart = True
        if isStart:
            break
        sky.draw()
        ground.draw()
        tRex.draw()
        score.draw()
        blinkText.update()
        blinkText.draw()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
# started and control the game
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    up = True
                    attack.count += 1
                    JUMPING_SOUND.play() #효과음
                    print(attack.count)
                # elif event.key == K_DOWN:
                #     down = True
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    up = False
                # elif event.key == K_DOWN:
                #     down = False

        if attack.count == 5:
            ATTACK_SOUND.play()
            down = True
            if change_count >= 400:
                down = False
                change_count = 0
                attack.count = 0
            change_count += 1
            print("change_count" + str(change_count))
        
        sky.update(score.score)
        sky.draw()

        ground.update(score.score)
        ground.draw()

        tRex.update(up, down)
        tRex.draw()

        ls.update(score.score)
        ls.draw()

        score.update()
        score.draw()
                
# game over and play again
        if isCollision(tRex, ls):
            OBSTACLE_SOUND.play()
            tRex.surface.fill((0, 0, 0, 0))
            tRex.surface.blit(tRex.img, (0, 0), (120, 0, 40, 43))
            gameOverFontObj = pygame.font.SysFont('consolas', 30, bold=1)
            gameOverTextSurface = gameOverFontObj.render("GAME OVER", True, (0, 0, 0))
            while True:
                isStart = False
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_RETURN:
                        isStart = True
                if isStart:
                    break
                sky.draw()
                ground.draw()
                tRex.draw()
                ls.draw()
                score.draw()
                DISPLAYSURF.blit(gameOverTextSurface, (int(WINDOWWIDTH/2 - gameOverTextSurface.get_width()/2), 50))
                blinkText.update()
                blinkText.draw()
                pygame.display.update()
                FPSCLOCK.tick(FPS)
            score.score = 0
            attack.count = 0
            down = False
            ls = ListCatusAndBirds()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
if __name__ == '__main__':
    main()
