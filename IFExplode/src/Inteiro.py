#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Lucas"
__date__ = "$26/09/2015 16:52:42$"

import pygame, sys,os , time
from pygame.locals import *

pygame.init()

pygame.mixer.init()

inicio = pygame.mixer.Sound('comecou.wav')

clock = pygame.time.Clock()

running = True

class Player:
    x = 100
    y = 100
    accx = 0
    accy = 0
    speedx = 0
    speedy = 0

    ball_file = os.path.join("Images", "Player.png")
    ball_surface = pygame.image.load(ball_file)

    def move(self):
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            if self.y > 0:
                self.y += -5
        if key[pygame.K_DOWN]:
            if self.y < 580:
                self.y += 5
        if key[pygame.K_LEFT]:
            if self.x > 0:
                self.x += -5
        if key[pygame.K_RIGHT]:
            if self.x < 780:
                self.x += 5
        if key[pygame.K_w]:
            self.speedy -= 5
        if key[pygame.K_s]:
            self.speedy += 5
        if key[pygame.K_p]:
            self.accx += 1
        if key[pygame.K_o]:
            self.accx -= 1


    def speed(self):
        if self.x > 0 & self.x < 780:
            self.speedx += self.accx
            self.x += self.speedx

        if self.y > 0 & self.x < 580:
            self.speedy += self.accy
            self.y += self.speedy

    def blit(self):
        screen.blit(self.ball_surface, (self.x, self.y))

Player= Player()

window = pygame.display.set_mode((1024, 768))

screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0xFF, 0xFF, 0xFF))


def handle():
    global running
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False;
        elif event.type == KEYDOWN:
            Player.move()

pygame.key.set_repeat(1)

inicio.play()

while running:
    clock.tick(10)
    pygame.display.set_caption('x:%d, y:%d'%(Player.x, Player.y))
    handle()

    screen.blit(background, (0, 0))
    Player.speed()
    Player.blit()

    pygame.display.flip()

pygame.display.quit()