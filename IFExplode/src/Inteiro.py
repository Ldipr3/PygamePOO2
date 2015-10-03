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

class Player (pygame.sprite.Sprite):
    # define as propriedades da imagem como cor e tamanho
    def __init__(self, color = blue, largura = 70, altura = 86):
        
        super( Player, self ).__init__() #pega as caracteristicas do pai e construtor
        self.image = pygame.Surface((largura, altura))
        self.image.fill(color) #preenche a imagem com uma cor
        
        self.set_properties()
        
        self.hspeed = 0
        self.vspeed = 0
        
        self.fase = None
    
    def set_properties(self):
        
        self.rect = self.image.get_rect() #da propriedades de um retangulo a imagem feito pelao pygame
        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery
        
        self.speed = 5
        
    
    #Define a posicao em que o objetos sera criado
    def set_position(self, x, y ):
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y
    
    def set_fase(self, fase):
        self.fase = fase
        self.set_position(fase.player_inicio_x, fase.player_inicio_y)
    
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
                    self.hspeed = -self.speed
                if (event.key == pygame.K_RIGHT):
                    self.hspeed = self.speed
                if (event.key == pygame.K_UP):
                    if(len(collision_list)>=1):
                        self.vspeed = -(self.speed)*2.0 # dobra a velocidade e pula
                '''
                if (event.key == pygame.K_DOWN):
                    #self.change_speed( 0, 5 )
                    pass
                '''
            
            if(event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT):
                    if (self.hspeed < 0): self.hspeed = 0
                if (event.key == pygame.K_RIGHT):
                    if (self.hspeed > 0): self.hspeed = 0
                '''
                comentado pois temos gravidade, pode ser usado depois
                if (event.key == pygame.K_UP):
                    #if (self.vspeed != 0): self.vspeed = 0
                    pass
                if (event.key == pygame.K_DOWN):
                    #if (self.vspeed != 0): self.vspeed = 0
                    pass
                '''
    def aplicar_gravidade(self, gravidade = .50):
        if (self.vspeed == 0): self.vspeed = 1
        else: self.vspeed += gravidade
        
        
class Block( pygame.sprite.Sprite): # Usa a classe sprite do java
    
    def __init__(self, x, y,  largura, altura, color = blue):
        
        super( Block, self ).__init__() #pega as caracteristicas do pai e construtor
        self.image = pygame.Surface((largura, altura))
        self.image.fill(color) #preenche a imagem com uma cor
        
        self.rect = self.image.get_rect() #da propriedades de um retangulo a imagem feito pelao pygame
        
        #self.origin_x = self.rect.centerx
        #self.origin_y = self.rect.centery
        
        self.rect.x = x #- self.origin_x
        self.rect.y = y #- self.origin_y

class Fase(object): #utiliza o novo jeito do python de usar heranca colocando object para conseguir chamar as funcoes da classe pai
    
    def __init__(self, objeto_player):
        
        self.lista_de_objetos = pygame.sprite.Group() # grupo para os objeto das plataformas da fase
        self.objeto_player = objeto_player
        self.player_inicio = self.player_inicio_x, self.player_inicio_y = 0,0 
    
        self.deslocamento_mundo_x = self.deslocamento_mundo_y = 0 #o quanto o mundo da fase muda
        
        self.visao_esquerda = window_largura/2 - window_largura/8
        self.visao_direita = window_largura/2 - window_largura/10
        
        self.visao_cima = window_altura/5 
        self.visao_baixo = window_altura/4 - window_altura/10
             
        
    def update(self):
        self.lista_de_objetos.update() #atualiza todos os objetos do grupo de objetos
    
    def draw(self, window):
        
        window.fill(white) #desenha o fundo da janela
        
        self.lista_de_objetos.draw(window) #desenha os objetos da fase na janela
    
    def desloca_mundo(self, desloca_x, desloca_y):
        
        self.deslocamento_mundo_x += desloca_x
        self.deslocamento_mundo_y += desloca_y
        
        for cada_objeto in self.lista_de_objetos:
            cada_objeto.rect.x += desloca_x
            cada_objeto.rect.y += desloca_y
    
    def controla_camera(self):
        
        if(self.objeto_player.rect.x <= self.visao_esquerda):
            diferenca_visao = self.visao_esquerda - self.objeto_player.rect.x #diferenca do quanto podemos ir menos o quanto ja fomos para aquele lado
            self.objeto_player.rect.x = self.visao_esquerda
            self.desloca_mundo(diferenca_visao, 0)
            
        if(self.objeto_player.rect.x >= self.visao_direita):
            diferenca_visao = self.visao_direita - self.objeto_player.rect.x #diferenca do quanto podemos ir menos o quanto ja fomos para aquele lado
            self.objeto_player.rect.x = self.visao_direita
            self.desloca_mundo(diferenca_visao, 0)
        
        if(self.objeto_player.rect.y <= self.visao_cima):
            diferenca_visao = self.visao_cima - self.objeto_player.rect.y #diferenca do quanto podemos ir menos o quanto ja fomos para aquele lado
            self.objeto_player.rect.y = self.visao_cima
            self.desloca_mundo(0, diferenca_visao)
            
        if(self.objeto_player.rect.y >= self.visao_baixo):
            diferenca_visao = self.visao_baixo - self.objeto_player.rect.y #diferenca do quanto podemos ir menos o quanto ja fomos para aquele lado
            self.objeto_player.rect.y = self.visao_baixo
            self.desloca_mundo(0, diferenca_visao)
            
class Fase_1(Fase):
    
    def __init__(self, objeto_player):
        
        super (Fase_1, self).__init__(objeto_player)
        
        #define um lugas especifico aonde o player vai iniciar naquela fase
        self.player_inicio = self.player_inicio_x, self.player_inicio_y = 100,0
        
        level = [
            # [ x, y, largura, altura, color ]
            [2, 124, 365, 47, black],
            [200, 324, 280, 47, black]
        ]
        
        for block in level:
            block = Block(block[0], block[1], block[2], block[3], block[4])
            self.lista_de_objetos.add(block)
        
'''
def set_message( text ):
    global message, previous_message
    message = font.render( text, True, black, white )
    previous_message = message
'''

pygame.init()

# Definicoes da Janela
window_tamanho = window_largura, window_altura = 1024, 768
window = pygame.display.set_mode(window_tamanho, pygame.RESIZABLE)
pygame.display.set_caption('IFExplode!!!')
clock = pygame.time.Clock()#funcao clock controla o tempo dentro da janela
frames_por_segundo = 60

lista_objetos_ativos = pygame.sprite.Group() #cria lista de objetos ativo
player = Player() #cria o player
player.set_image(os.path.join("Images", "PlayerV1.png"))
player.set_position(40, 40) #define uma posicao para o player

lista_objetos_ativos.add(player) #adiciona player na lista de objetos ativos

lista_Fases = [] #uma lista para as fases
lista_Fases.append(Fase_1( player )) #adiciona a fase 1 a lista e passa o objeto player naquela fase

fase_atual_numero = 0 # um numero para identificar a fase atual
fase_atual = lista_Fases[fase_atual_numero] #guarda a posicao da fase atual da lista

player.set_fase(fase_atual)



font = pygame.font.SysFont("Times New Roman, Arial", 30) # carrega a fonte 
#text = font.render("IFExplode!!!", True, black) #renderiza a fonte

'''
massage = previous_message = None
set_message("")        
'''

running = True # Variavel para o loop da janela principal
            
while running:    
    for event in pygame.event.get():
        if (event.type == QUIT) or \
        (event.type == pygame.KEYDOWN and \
        (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
            running = False
    
    #Funcoes de atualizacao
    
    player.update(fase_atual.lista_de_objetos, event)
    event = None #esvazia a variavel event
    fase_atual.update()
    
    
    #Testes de logica do jogo
    
    fase_atual.controla_camera()
    
    #Desenha e redesenha tudo
    
    fase_atual.draw(window)
    lista_objetos_ativos.draw(window)
    
    
    #Atrasa a Framerate
    
    clock.tick(frames_por_segundo)
    
    #Atualiza a tela
    
    pygame.display.update()
            

pygame.quit()