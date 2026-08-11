import arcade
import Player
import coin

class JanelaJogo(arcade.Window):

    def __init__(self):
          super().__init__(800, 600, "Coletor de Moedas - POO")
          arcade.set_background_color(43, 201, 237)

          self.jogador = Player()
          self.jogador.center_x = 400
          self.jogador.center_y = 300
          self.coin = coin()
          self.coin.center_x = 600
          self.coin.center_y = 500
          self.sprite_moedas = arcade.SpriteList()
          self.sprite_moedas.append(self.coin)

    def on_draw(self):
         self.clear()
         self.sprite_jogador.draw()
         self.sprite_moedas.draw()

    def on_update(self, delta_time):
         pass

    def main():
         tela= JanelaJogo()
         arcade.run()
    if __name__ == "__main__":
        main()


    