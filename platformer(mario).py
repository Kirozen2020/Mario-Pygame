import pygame
from pygame import *
import pyganim
import os

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = '#004400'
MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
MOVE_EXTRA_SPEED = 2.5
JUMP_EXTRA_POWER = 1
ANIMATION_SUPER_SPEED_DELAY = 1
ANIMATION_BLOCKTELEPORT = [
    ("portal1.png"),
    ("portal2.png")]

ANIMATION_DELAY = 1
ANIMATION_RIGHT = [('r1.png'),
                   ('r2.png'),
                   ('r3.png'),
                   ('r4.png'),
                   ('r5.png')]
ANIMATION_LEFT = [('l1.png'),
                  ('l2.png'),
                  ('l3.png'),
                  ('l4.png'),
                  ('l5.png')]
ANIMATION_JUMP_LEFT = [('jl.png', 1)]
ANIMATION_JUMP_RIGHT = [('jr.png', 1)]
ANIMATION_JUMP = [('j.png', 1)]
ANIMATION_STAY = [('0.png', 1)]

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#2110FF"
ICON_DIR = os.path.dirname(__file__)

ANIMATION_MONSTERHORYSONTAL = [('fire1.png'),
                      ('fire2.png')]

ANIMATION_PRINCESS = [('princess_l.png'), ('princess_r.png')]


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h)


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("platform.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.winner = False

class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_PRINCESS:
            boltAnim.append((anim, 0.8))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(BACKGROUND_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX
        self.goY = goY
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(BACKGROUND_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.maxLengthUp= maxLengthUp
        self.xvel = left
        self.yvel = up
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, platforms):
        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
        self.rect.y += self.yvel
        self.rect.x += self.xvel
        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                self.xvel = - self.xvel
                self.yvel = - self.yvel


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("dieBlock.png")


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.yvel = 0
        self.onGround = False

        self.image.set_colorkey(Color(COLOR))

        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()

        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()



    def update(self, left, right, up, running, platforms):
        if left:
            self.xvel = -MOVE_SPEED
            self.image.fill(pygame.Color(COLOR))
            if running:
                self.xvel -= MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimLeft.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED
            self.image.fill(pygame.Color(COLOR))
            if running:
                self.xvel += MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))

        if not (left or right):
            self.xvel = 0
            if not up:
                self.image.fill(pygame.Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
                if running and (left or right):
                    self.yvel -= JUMP_EXTRA_POWER
                self.image.fill(pygame.Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

                if isinstance(p, BlockDie) or isinstance(p, Monster):
                    self.die()
                elif isinstance(p, BlockTeleport):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, Princess):
                    self.einner = True

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY


def main():
    global running
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Super Mario Boy")
    bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(pygame.Color(BACKGROUND_COLOR))
    PLATFORM_WIDTH = 32
    PLATFORM_HEIGHT = 32
    PLATFORM_COLOR = "#FF6262"
    hero = Player(55, 55)
    left = right = False
    up = False
    running = False
    entities = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    platforms = []
    entities.add(hero)

    level = [
        "----------------------------------",
        "-                                -",
        "-   ---                 ---      -",
        "-                          -     -",
        "-            --         *        -",
        "-                                -",
        "--                               -",
        "-         *                   P  -",
        "-                   ----     --- -",
        "-                                -",
        "--            --                 -",
        "-                                -",
        "-                            --- -",
        "-                  *             -",
        "-                                -",
        "-  *   ---                       -",
        "-                                -",
        "-   -------         ----         -",
        "-                                -",
        "-     **                  -      -",
        "-                            --  -",
        "-          ---      -            -",
        "-                   -            -",
        "----------------------------------"]

    timer = pygame.time.Clock()

    animatedEntities = pygame.sprite.Group()
    tp = BlockTeleport(128, 512, 800, 64)
    entities.add(tp)
    platforms.append(tp)
    animatedEntities.add(tp)
    mn = Monster(190,200,2,3,150,15)
    entities.add(mn)
    platforms.append(mn)
    monsters.add(mn)

    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)
    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:

                pygame.quit()
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

        screen.blit(bg, (0, 0))

        camera.update(hero)
        hero.update(left, right, up, running, platforms)
        animatedEntities.update()
        monsters.update(platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()

main()