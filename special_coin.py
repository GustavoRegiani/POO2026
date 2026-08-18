import arcade 

class Special_Coin(arcade.Sprite):
    def __init__(self):
         base_path = "Sprites/"
         super().__init__(f"{base_path}special_coin.png", scale=0.6)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebote no Eixo X
        if self.left < 0 or self.right > 800:
            self.change_x *= -1
        # Rebote no Eixo Y
        if self.bottom < 0 or self.top > 600:
            self.change_y *= -1 