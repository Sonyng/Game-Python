#importando bibliotecas
import os
import sys
import math
import random
import pygame


#altura e largura
WIDTH = 623
HEIGHT = 150


#inicio do game
pygame.init()

#inicializa mixer do pygame para reprodução de audio
pygame.mixer.init()


#setar Tamanho da tela
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )

#nome do jogo Titulo
pygame.display.set_caption('Jogo do dinossauro')


#classe Background
class BG:
    def __init__(self, x):
        #IMG Background vai consumir toda a tela
        self.width = WIDTH
        self.height = HEIGHT
        self.x = x #posições do objeto
        self.y = 0  #posições do objeto
        
        self.set_texture()  #chama functions
        self.show() #function exibe na tela
 

    #Function atualiza a posição do objeto na tela.
    def update(self, dx):
        self.x += dx #dx indica o deslocamento
                  #self x indica a posição atual do objeto
        if self.x <= -WIDTH: #verifica se o objeto ultrapassou o limite esquerdo da tela.
            self.x = WIDTH  #o objeto é reposicionado para a posição inicial na extremidade direita da tela

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    #importando background game
    def set_texture(self):
        path = os.path.join('assets/images/bg.png')
        self.texture = pygame.image.load(path) #Essa função retorna um objeto que representa a imagem carregada.
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height)) #carrega a imagem da textura, redimensiona-a para as dimensões desejadas

#Classe dino
class Dino:

    def __init__(self):
        #definem a largura e a altura do dinossauro como 44 pixels.
        self.width = 44
        self.height = 44
        #definem as coordenadas iniciais do dinossauro na tela, com 
        self.x = 10
        self.y = 80
        # armazena o número da textura do dinossauro
        self.texture_num = 0

        #define a velocidade vertical do dinossauro, ou seja, a quantidade de pixels que o dinossauro se move para cima ou para baixo em cada atualização.
        self.dy = 3

        # especifica o valor da gravidade aplicada ao dinossauro. Afeta o movimento de queda do dinossauro.
        self.gravity = 1.2

        # indica se o dinossauro está no chão.
        self.onground = True

        #indica se o dinossauro está pulando.
        self.jumping = False

        # especifica a altura de parada do salto do dinossauro.
        self.jump_stop = 10

        #indica se o dinossauro está caindo
        self.falling = False
        
        #armazena a posição vertical do dinossauro quando ele começa a cair.
        self.fall_stop = self.y
               
        #Carrega a textura
        self.set_texture()
        
        #Carrega o som do pulo
        self.set_sound()

        #exibir o dinossauro na tela
        self.show()

    #Atualiza o estado do dinossauro
    def update(self, loops):
        # jumping
        if self.jumping:   
            self.y -= self.dy   #for True, significa que o dinossauro está pulando
            if self.y <= self.jump_stop: # define se a coordenada vertical  dinossauro é menor ou igual à altura de parada do salto
                self.fall() #é responsável por fazer o dinossauro começar a cair
        
        # falling
        elif self.falling:
            self.y += self.gravity * self.dy #se for True significa que o dinossauro está em queda, incrementa a gravidade para a queda
            if self.y >= self.fall_stop: # verifica se a posição do dinossauro é maior ou igual a posição de parada da queda
                self.stop() # é chamado para interromper a queda do dinossauro.

        # walking
        elif self.onground and loops % 4 == 0: #se o dinossauro estiver no chão, e o número de ciclos do loop for 4, o dinossauro muda a textura exibida para simular um movimento de caminhada
            self.texture_num = (self.texture_num + 1) % 3 #O número da textura do dinossauro é atualizado
            self.set_texture() #é chamado para carregar a nova textura de acordo com o número atualizado.
        

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    #carrega texturas do dino
    def set_texture(self):
        path = os.path.join(f'assets/images/dino{self.texture_num}.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    #carrega o som do pulo
    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)


    def jump(self): # é chamado quando o dinossauro realiza um salto
        self.sound.play() #Produz um som ao pulo
        self.jumping = True #como True para indicar que o dinossauro está em fase de salto e altera o estado
        self.onground = False #False para indicar que o dinossauro não está mais no chão.

    def fall(self): # é chamado quando o dinossauro atinge a altura máxima do salto e começa a cair
        self.jumping = False #como False para indicar que o dinossauro não está mais em fase de salto e altera o estado
        self.falling = True # True para indicar que o dinossauro está em fase de queda.

    def stop(self): # é chamado quando o dinossauro atinge o solo ou uma plataforma e para de cair
        self.falling = False # False para indicar que o dinossauro não está mais em fase de queda
        self.onground = True # True para indicar que o dinossauro está no chão novamente


#Classe cacto
class Cactus:

    def __init__(self, x):
        #Define altura e largura do cacto
        self.width = 34
        self.height = 44
        #define o ponto de surgimento
        self.x = x
        self.y = 80
        # chama metodos para configurar a textura do cacto e exibi-lo na tela.
        self.set_texture()
        self.show()

    # responsável por atualizar os quadros do cacto
    def update(self, dx): 
        self.x += dx #permite que o cacto se mova na horizontal

    # desenha a textura do cacto na tela
    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    # é responsável por carregar a imagem do cacto e redimensioná-la para o tamanho desejado
    def set_texture(self):
        path = os.path.join('assets/images/cactus.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


#Classe colisao
class Collision:

    # é responsável por verificar se há uma colisão entre dois objetos no jogo.
    def between(self, obj1, obj2): #Recebe 2 objetos
        distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) #O método calcula a distância entre os objetos utilizando  a distância entre os pontos (x, y) de cada objeto.
                                                                #é comparada a distancia com o valor limite de 35 se for menor que 35 indica colisao
        return distance < 35  # retorna True se a distância entre eles for menor que 35, indicando uma colisão


#Classe Score
class Score:
    
    #O construtor da classe inicializa os atributos da pontuação
    def __init__(self, hs):
        self.hs = hs #hs é a pontuação máxima
        self.act = 0 # armazena a pontuação atual em tempo real
        self.font = pygame.font.SysFont('monospace', 18) # define a fonte usada para exibir a pontuação na tela
        self.color = (0, 0, 0) # Define a cor da letra utilizada na pontuação
        self.set_sound() #Chama som a cada 100 Pontos
        self.show() #exibe a pontuação atual na tela

    # Metodo update é atualizada com base no número de loops passado como argumento
    def update(self, loops):
        self.act = loops // 10 # a divisão por 10 é usada para determinar como a pontuação aumenta ao longo do tempo
        self.check_hs() # é chamado para verificar se a pontuação atual é maior do que a pontuação máxima
        self.check_sound() #  é chamado para verificar se a pontuação atual atinge um valor múltiplo de 100 (TIRANDO 0)

    #Exibe 
    def show(self):
        self.lbl = self.font.render(f'HI {self.hs} {self.act}', 1, self.color) #a pontuação atual e a pontuação máxima são renderizadas como uma string na superfície da tela
        lbl_width = self.lbl.get_rect().width #  onde hs é substituído pelo valor da pontuação máxima e act é substituído pelo valor da pontuação atual.
        screen.blit(self.lbl, (WIDTH - lbl_width - 10, 10)) # a imagem da string é exibida na tela usando o método blit() da superfície da tela
                                                  # a posição é alinhada à direita da tela, com uma margem de 10 pixels a partir da borda direita
 
    #o som é carregado a partir de um arquivo de áudio
    def set_sound(self):
        path = os.path.join('assets/sounds/point.wav')
        self.sound = pygame.mixer.Sound(path)
        
    #    
    def check_hs(self):
        if self.act >= self.hs: # a pontuação atual é comparada com a pontuação máxima
            self.hs = self.act #Se a pontuação atual for maior ou igual à pontuação máxima, a pontuação máxima é atualizada para o valor da pontuação atual.

    def check_sound(self):
        if self.act % 100 == 0 and self.act != 0: # é verificado se a pontuação atual é um múltiplo de 100 e diferente de zero
            self.sound.play() #Se essa condição for atendida, o som é reproduzido chamando o método Play()


#Classe Jogo
class Game:
      
      #Metodo INIT
    def __init__(self, hs=0): 
        self.bg = [BG(x=0), BG(x=WIDTH)] #Cria uma lista com duas instâncias de objetos BG, que representam os planos de fundo do jogo e WIDTH representa a largura da janela do jogo. 
        self.dino = Dino() # Cria uma instância do objeto Dino, que representa o personagem principal do jogo.
        self.obstacles = [] #Cria uma lista vazia que será usada para armazenar os obstáculos do jogo.
        self.collision = Collision() # Cria uma instância do objeto Collision, que será usado para verificar colisões entre objetos no jogo.
        self.score = Score(hs) #Cria uma instância do objeto Score, que é responsável por controlar a pontuação do jogo
        self.speed = 3 # Define a velocidade do jogo como 3. Esse valor pode ser ajustado para controlar a dificuldade do jogo.
        self.playing = False # Define a variável playing como False, indicando que o jogo ainda não começou.
        self.set_sound() # Configura o som do jgo
        self.set_labels() #é responsável por configurar as etiquetas utilizadas no jogo
        self.spawn_cactus() #Rescponsavel por  gerar os obstáculos de cacto no início do jogo



    def set_labels(self):
        big_font = pygame.font.SysFont('monospace', 24, bold=True) # A fonte grande é definida com tamanho 24 e negrito ativado. O texto "GAME OVER Utilizado na cor preta"
        small_font = pygame.font.SysFont('monospace', 18) 
        self.big_lbl = big_font.render(f'G A M E  O V E R', 1, (0, 0, 0)) 
        self.small_lbl = small_font.render(f'press r to restart', 1, (0, 0, 0))

    #Som de colisao
    def set_sound(self):
        path = os.path.join('assets/sounds/die.wav') # o arquivo de som é carregado na variável
        self.sound = pygame.mixer.Sound(path) 

    def start(self): # é responsável por iniciar o jogo. Ele define o atributo playing como True, indicando que o jogo está em andamento.
        self.playing = True


    def over(self): #é chamado quando o jogador perde o jogo. Ele reproduz o som de perda, exibe as etiquetas de texto "GAME OVER" 
        self.sound.play()
        screen.blit(self.big_lbl, (WIDTH // 2 - self.big_lbl.get_width() // 2, HEIGHT // 4))#e "press r to restart" na tela e define o atributo playing como False, indicando que o jogo acabou.
        screen.blit(self.small_lbl, (WIDTH // 2 - self.small_lbl.get_width() // 2, HEIGHT // 2))
        self.playing = False

    def tospawn(self, loops): #é utilizado para determinar se é o momento de criar um novo cacto. 
        return loops % 100 == 0 #Ele retorna True se o número de loops for um múltiplo de 100, caso contrário, retorna False.

    def spawn_cactus(self): # é responsável por criar e adicionar um novo cacto à lista de obstáculos.
        # list with cactus
        if len(self.obstacles) > 0: # o novo cacto será posicionado aleatoriamente à frente do último cacto
            prev_cactus = self.obstacles[-1] 
            x = random.randint(prev_cactus.x + self.dino.width + 84, WIDTH + prev_cactus.x + self.dino.width + 84)

        # empty list
        else:
            x = random.randint(WIDTH + 100, 1000)# Caso a lista esteja vazia, o novo cacto será posicionado aleatoriamente entre as coordenadas WIDTH + 100 e 1000. 
                                        # O novo cacto é criado usando a classe Cactus e adicionado à lista self.obstacles.
        #Cria novo cacto
        cactus = Cactus(x)
        self.obstacles.append(cactus)


    def restart(self): # metodo reinicia o jogo
        self.__init__(hs=self.score.hs) # hama Ele chama o método __init__() passando o valor atual de self.score.hs como argumento para reinicializar


# é responsável por executar o loop principal do jogo
def main():

    # É criado um objeto Game chamado game e um objeto Dino chamado dino.
    game = Game()
    dino = game.dino

    # São definidas algumas variáveis
    
    clock = pygame.time.Clock()  #como o objeto clock para controlar a velocidade de atualização do jogo  
    loops = 0   #loops para contar o número de iterações do loop
    over = False # over para indicar se o jogo terminou.

    # O loop principal do jogo é executado indefinidamente.
    while True: 

          #Se o jogo estiver em andamento, as seguintes ações ocorrem:
        if game.playing:
               
            loops += 1

            #Atualizações do plano de fundo (game.bg).
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()

            # Atualizações e exibição do objeto dinossauro (dino).
            dino.update(loops)
            dino.show()

            if game.tospawn(loops):
                game.spawn_cactus()

                       # Verifica se é necessário criar novos cactos e os atualiza e exibe (game.obstacles).
            for cactus in game.obstacles:
                cactus.update(-game.speed)
                cactus.show()

                
                if game.collision.between(dino, cactus):  # Verifica se houve colisão entre o dinossauro e algum cacto 
                   over = True #define a variável over como True se houver colisão.
            
            if over:
                game.over() # Se over for True, chama o método game.over() para exibir a tela de game over.

            # As atualizações e exibições da pontuação (game.score) são feitas.
            game.score.update(loops)
            game.score.show()

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Se o evento de fechar a janela for detectado, o pygame é encerrado usando pygame.quit() e o programa é finalizado usando sys.exit().
                pygame.quit()
                sys.exit()
             #Se o evento de pressionar uma tecla for detectado, as seguintes ações são realizadas:
            if event.type == pygame.KEYDOWN: #Se a tecla pressionada for a tecla de espaço (pygame.K_SPACE), são feitas as seguintes verificações:
                if event.key == pygame.K_SPACE:
                    if not over: #Se o jogo não estiver no estado "game over" (not over).
                        if dino.onground: #Se o dinossauro estiver no chão (dino.onground).
                            dino.jump()#Se todas as verificações forem verdadeiras, o dinossauro é instruído a pular 

                        if not game.playing: #Se o jogo não estiver em andamento (not game.playing).
                            game.start() #o jogo é iniciado (game.start()).

                if event.key == pygame.K_r: #Se a tecla pressionada for a tecla "r" (pygame.K_r), são realizadas as seguintes ações:
                    game.restart() #O jogo é reiniciado (game.restart()).
                    dino = game.dino #O objeto dino é atualizado para a referência atual do dinossauro no jogo (dino = game.dino).
                    loops = 0 # A variável loops é redefinida para 0.
                    over = False # A variável over é definida como False, indicando que o jogo não está mais no estado "game over".

        clock.tick(80) #para limitar a taxa de atualização do jogo a 80 quadros por segundo.
        pygame.display.update() # é chamado para atualizar a tela do jogo com as alterações feitas.

        

main() # é o ponto de entrada do programa e é responsável por executar o jogo.