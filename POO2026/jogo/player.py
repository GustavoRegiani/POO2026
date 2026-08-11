import arcade 

class Player(arcade.Sprite):
    def __init__(self):
        base_path = "jogo/sprites"
        super().__init__(f"{base_path}/Homem-Aranha stand direita.png", scale=0.5)
        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture(f"{base_path}/Homem-Aranha stand esquerda.png")

    def update(self, delta_time):
       self.center_x += self.change_x
       self.center_y += self.change_y

       if self.right > 800:
         self.right = 800
         self.change_x = 0

       if self.top > 600:
          self.top = 600
          self.change_y = 0 

       if self.left < 0:
        self.left = 0
        self.change_x = 0  

       if self.bottom < 0:
        self.bottom = 0
        self.change_y = 0 

       if self.change_x > 0:
        self.texture = self.textura_direita
       elif self.change_x < 0:
        self.texture = self.textura_esquerda