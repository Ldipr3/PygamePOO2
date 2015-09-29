#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Lucas"
__date__ = "$26/09/2015 16:52:42$"

import pygame, sys, os, time
from color import *
from pygame.locals import *

#Define algumas cores
#white = pygame.Color( 255, 255 ,255 )
#black = pygame.Color( 0, 0, 0 )
#gray = pygame.Color( 90, 90 ,90 )
#silver = pygame.Color( 200, 200, 200 )
#red = pygame.Color( 255, 0, 0 )
#green = pygame.Color( 0, 255, 0 )
#blue = pygame.Color( 0, 0, 255 )

class Block( pygame.sprite.Sprite): # Usa a classe sprite do java
    # define as propriedades da imagem como cor e tamanho
    def __init__(self, color = blue, largura = 64, altura = 64):
        
        super( Block, self ).__init__() #pega as caracteristicas do pai e construtor
        self.image = pygame.Surface((largura, altura))
        self.image.fill(color) #preenche a imagem com uma cor
        self.set_properties()
        
        self.hspeed = 0
        self.vspeed = 0
    
    def set_properties(self):
        
        self.rect = self.image.get_rect() #da propriedades de um retangulo a imagem feito pelao pygame
        
        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery
        
        self.speed = 5
        
    
    def change_speed(self, hspeed, vspeed):
        self.hspeed += hspeed
        self.vspeed += vspeed
        
    
    #Define a posicao em que o objetos sera criado
    def set_position(self, x, y ):
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y
    
    #Carrega a imagem na sprite passando o caminho aonde esta a imagem     
    def set_image(self, filename = None):
        if (filename != None):
            
            self.image = pygame.image.load(filename)          
            self.set_properties()
    
    def update(self, collidable = pygame.sprite.Group() , event = None): #atualiza a imagem detectando a colisao parando o objeto
        
        self.aplicar_gravidade()
        
        self.rect.x += self.hspeed
        
        collision_list = pygame.sprite.spritecollide(self, collidable, False ) #lista de objetos colidiveis
        
        for collided_object in collision_list:
            if ( self.hspeed > 0):
                #pra la deretcha!
                self.rect.right = collided_object.rect.left
            elif (self.hspeed < 0):
                #pra la esquercha!
                self.rect.left = collided_object.rect.right
        
        self.rect.y += self.vspeed
        
        collision_list = pygame.sprite.spritecollide(self, collidable, False ) #lista de objetos colidiveis
        
        for collided_object in collision_list:
            if ( self.vspeed > 0):
                #pra bajo!
                self.rect.bottom = collided_object.rect.top
                self.vspeed = 0
            elif (self.vspeed < 0):
                #pra riba!
                self.rect.top = collided_object.rect.bottom
                self.vspeed = 0
        
        if not ( event == None ):
            if(event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    self.change_speed( -(self.speed), 0 )
                if (event.key == pygame.K_RIGHT):
                    self.change_speed( (self.speed), 0 )
                if (event.key == pygame.K_UP):
                    if(self.vspeed == 0):
                        self.change_speed( 0, -(self.speed)*2.5) # dobra a velocidade e pula
                if (event.key == pygame.K_DOWN):
                    #self.change_speed( 0, 5 )
                    pass
            if(event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT):
                    if (self.hspeed != 0): self.hspeed = 0
                if (event.key == pygame.K_RIGHT):
                    if (self.hspeed != 0): self.hspeed = 0
                if (event.key == pygame.K_UP):
                    #if (self.vspeed != 0): self.vspeed = 0
                    pass
                if (event.key == pygame.K_DOWN):
                    #if (self.vspeed != 0): self.vspeed = 0
                    pass
                
    def aplicar_gravidade(self, gravidade = .50):
        if (self.vspeed == 0): self.vspeed = 1
        else: self.vspeed += gravidade
        
        

def set_message( text ):
    global message, previous_message
    message = font.render( text, True, black, white )
    previous_message = message
    
pygame.init()



# Definicoes da Janela
window_tamanho = window_largura, window_altura = 1024, 768
window = pygame.display.set_mode(window_tamanho, pygame.RESIZABLE)
pygame.display.set_caption('IFExplode!!!')
clock = pygame.time.Clock()#funcao clock controla o tempo dentro da janela
frames_por_segundo = 60

#Maneja os blocos na janela
block_grupo = pygame.sprite.Group() # Cria um grupo de sprites para os blocos

bloco1 = Block()
bloco1.set_image(os.path.join("Images","Player.png"))
bloco1.set_position( window_largura/2 - 150, window_altura/2-100 )

bloco2 = Block( red )
bloco2.set_position( window_largura/2 , window_altura/2 + 80 )

bloco3 = Block( blue, 400, 200 )
bloco3.set_position( window_largura/5 , window_altura/2 + 300 )

bloco4 = Block( green, 400, 1000 )
bloco4.set_position( window_largura , window_altura/2 + 300 )

bloco5 = Block( red )
bloco5.set_position( window_largura/2 + 200 , window_altura/2 - 50 )

block_grupo.add(bloco5, bloco4, bloco3, bloco1, bloco2 ) #adiciona os dois blocos criados no grupo

font = pygame.font.SysFont("Times New Roman, Arial", 30) # carrega a fonte 
#text = font.render("IFExplode!!!", True, black) #renderiza a fonte

massage = previous_message = None
set_message("")        
            
collidable_objects = pygame.sprite.Group()
collidable_objects.add(bloco5, bloco4, bloco3, bloco2)

running = True # Variavel para o loop da janela principal
            
while running:    
    for event in pygame.event.get():
        if (event.type == QUIT) or \
        (event.type == pygame.KEYDOWN and \
        (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
            running = False
            
    clock.tick(frames_por_segundo) #trava a qnt de frames
    window.fill( white ) # fill eh uma funcao do pygame para encher de cor uma superficie
    bloco1.update(collidable_objects, event )
    event = None
    
    if(pygame.sprite.collide_rect(bloco1, bloco2)):
        set_message(" Bateu sa porra !!! ")
    else:
        set_message("")
    
    if(message != previous_message):
        set_message(message)
    
    block_grupo.draw(window) #desenha o grupo na janela
    window.blit(message, (window_largura/2 - message.get_rect().width/2 , window_altura/2 - 100 ))
    
    pygame.display.update()
    


pygame.display.quit()