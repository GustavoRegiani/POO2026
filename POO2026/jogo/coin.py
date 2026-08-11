import arcade 

class coin(arcade.Sprite):
    def __init__(self):
         base_path = "jogo/sprites"
         super().__init__(f"{base_path}coin.png", scale=0.6)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
