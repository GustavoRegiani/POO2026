import arcade
import player
import coin
import moeda_especial

class JanelaJogo(arcade.Window):

    def __init__(self):
          super().__init__(800, 600, "Coletor de Moedas")
          arcade.set_background_color(43, 201, 237)

          self.velocidade = 2

          self.jogador = player()
          self.jogador.center_x = 400
          self.jogador.center_y = 300

          self.coin = coin()
          self.coin.center_x = 600 #posição x
          self.coin.center_y = 500  #posição y
          self.coin.change_x = self.velocidade # Velocidade x
          self.coin.change_y = self.velocidade # Velocidade y

          self.sprite_jogador = arcade.SpriteList()
          self.sprite_jogador.append(self.jogador)

          self.sprite_moedas = arcade.SpriteList()
          self.sprite_moedas.append(self.coin)

    def on_draw(self):
         self.clear()
         self.sprite_jogador.draw()
         self.sprite_moedas.draw()

    def on_update(self, delta_time):
         self.sprite_jogador.update(delta_time)
         self.sprite_moedas.update(delta_time)

    def main():
         tela= JanelaJogo()
         arcade.run()
    if __name__ == "__main__":
        main()


    