import arcade
from player import Player
from special_coin import Special_Coin
from coin import Coin
import random

class JanelaJogo(arcade.Window):

    def __init__(self):
          super().__init__(800, 600, "Coletor de Moedas")
          arcade.set_background_color((43, 201, 237))

          self.velocidade = 2
          self.velocidades = [-2, -1, 1, 2]

          self.jogador = Player()
          self.jogador.center_x = 400
          self.jogador.center_y = 300


          
          
          # Adciona o personagem na lista
          self.sprite_jogador = arcade.SpriteList()
          self.sprite_jogador.append(self.jogador)

          # Lista de moedas do jogo
          self.sprite_moedas = arcade.SpriteList()

          # Cria várias moedas e adiciona cada uma delas na lista
          for i in range(30):
               self.coin = Coin()
               self.coin.center_x = random.randint(32, 600)
               self.coin.center_y = random.randint(32, 500)
               self.sprite_moedas.append(self.coin)

          # Adiciona a moeda especial por cima das outras
          for i in range(15):
               self.coinSpecial = Special_Coin()
               self.coinSpecial.center_x = random.randint(32, 600)
               self.coinSpecial.center_y = random.randint(32, 500)
               self.coinSpecial.change_x = self.velocidades[random.randint(0,3)] 
               self.coinSpecial.change_y = self.velocidades[random.randint(0,3)]
               self.sprite_moedas.append(self.coinSpecial)

    def on_draw(self):
         self.clear()
         self.sprite_moedas.draw()
         self.sprite_jogador.draw()

    def on_key_press(self, key, modifiers):
          if key == arcade.key.RIGHT: # Seta da esquerda ou A
               self.jogador.change_x += self.velocidade
          elif key == arcade.key.LEFT: # Seta da direita ou D
               self.jogador.change_x -= self.velocidade
          elif key == arcade.key.UP: # Seta de cima ou W
               self.jogador.change_y += self.velocidade
          elif key == arcade.key.DOWN: # Seta de baixo ou s
               self.jogador.change_y -= self.velocidade  

    def on_key_release(self, key, modifiers):
          # Ao soltar uma tecla, verifica se é do eixo X ou Y para zerar a velocidade
          if key in [arcade.key.LEFT, arcade.key.RIGHT]:
               self.jogador.change_x = 0
          if key in [arcade.key.UP, arcade.key.DOWN]:
               self.jogador.change_y = 0
      


    def on_update(self, delta_time):
         self.sprite_jogador.update(delta_time)
         self.sprite_moedas.update(delta_time)

def main():
     tela= JanelaJogo()
     arcade.run()
if __name__ == "__main__":
     main()


    