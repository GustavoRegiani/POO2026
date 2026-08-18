import arcade 

class Coin(arcade.Sprite):
    def __init__(self):
         base_path = "Sprites/"
         super().__init__(f"{base_path}coin.png", scale=0.4)

    # def update(self, delta_time):
    #     self.center_x += self.change_x
    #     self.center_y += self.change_y
