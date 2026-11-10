import arcade
import random
import time
from pathlib import Path
from PIL import Image
from pontuação import Pontuacao
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_MAX_HEALTH, PLAYER_SCALE, PLAYER_SPEED,
    TILE_SIZE, GRAVITY, COIN_SCALE
)



# Altura da janela do jogo.
ALTURA = 600
# Largura da janela do jogo.
LARGURA = 800
# Título exibido na janela.
TITULO = "Coletor de Moedas"

# Velocidade horizontal do jogador.
VELOCIDADE = 5
# Força do pulo do jogador.
VELOCIDADE_PULO = 14
# Força da gravidade aplicada pela física.
GRAVIDADE = 0.5

# Quantidade de moedas necessária para vencer.
META_MOEDAS = 10

LIMITE_NOME = 15

# Efeitos visuais da colisao (duracoes em segundos).
TEMPO_FLASH = 0.3
TEMPO_TREMOR = 0.35
INTENSIDADE_TREMOR = 8
ALPHA_FLASH = 120
QUADROS_EXPLOSAO = 6
ESCALA_EXPLOSAO = 1.0
# Intervalo minimo entre duas explosoes enquanto o fantasma continua encostado.
TEMPO_ENTRE_EXPLOSOES = 0.4
# Espera antes do Game Over, para a explosao do golpe final aparecer.
ATRASO_GAME_OVER = 0.6


def asset_path(nome_arquivo):
    pasta_base = Path(__file__).resolve().parent
    caminhos = [
        pasta_base / 'Sprites_Png',
        pasta_base.parent / 'Png',
        pasta_base
    ]

    for pasta in caminhos:
        caminho = pasta / nome_arquivo
        if caminho.exists():
            return str(caminho)

    return str(pasta_base / 'Sprites_Png' / nome_arquivo)


# Cria os blocos usados no chão e nas plataformas.
class Bloco(arcade.SpriteSolidColor):

    def __init__(self, x, y, largura=64, altura=40):
        super().__init__(
            width=largura,
            height=altura,
            color=arcade.color.DARK_BROWN
        )

        self.center_x = x
        self.center_y = y


# Cria o personagem controlado pelo jogador.
class Player(arcade.Sprite):

    def __init__(self):
        super().__init__(
            asset_path("Homem-Aranha stand direita.png"),
            scale=1
        )

        self.center_x = 100
        self.center_y = 150

        self.i_frame = False
        self.i_frame_time = 0.0


# Cria os inimigos que perseguem ou se movimentam pelo mapa.
class Inimigo(arcade.Sprite):

    def __init__(self, x, y, pequeno=False):

        escala = 0.5 if pequeno else 1.0

        super().__init__(
            asset_path("fantasma_right.png"),
            scale=escala
        )

        self.center_x = x
        self.center_y = y

        self.pequeno = pequeno

        if pequeno:
            self.change_x = 3
            self.change_y = 3
        else:
            self.change_x = 2
            self.change_y = 2

        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture(
            asset_path("fantasma_left.png")
        )

    # Teleporta o inimigo para uma posição aleatória.
    def teleportar(self):

        self.center_x = random.randint(50, LARGURA - 50)
        self.center_y = random.randint(120, ALTURA - 50)

    # Atualiza o movimento do inimigo.
    def atualizar(self, player):

        if not self.pequeno:

            velocidade = 1.5

            if self.center_x < player.center_x:
                self.center_x += velocidade
                self.texture = self.textura_direita

            elif self.center_x > player.center_x:
                self.center_x -= velocidade
                self.texture = self.textura_esquerda

            if self.center_y < player.center_y:
                self.center_y += velocidade

            elif self.center_y > player.center_y:
                self.center_y -= velocidade

        else:

            self.center_x += self.change_x
            self.center_y += self.change_y

            if self.right >= LARGURA:
                self.right = LARGURA
                self.change_x *= -1
                self.texture = self.textura_esquerda

            if self.left <= 0:
                self.left = 0
                self.change_x *= -1
                self.texture = self.textura_direita

            if self.top >= ALTURA:
                self.top = ALTURA
                self.change_y *= -1

            if self.bottom <= 0:
                self.bottom = 0
                self.change_y *= -1


# Cria o inimigo que usa gravidade e pode pular.
class InimigoGravidade(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            asset_path("fantasma_right.png"),
            scale=0.9
        )

        self.center_x = x
        self.center_y = y

        self.velocidade = 2.2
        self.forca_pulo = 15

        self.pequeno = False

        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture(
            asset_path("fantasma_left.png")
        )

        self.color = arcade.color.PURPLE

    # Faz o inimigo escolher a direção em que deve andar.
    def decidir_direcao(self, player):

        if self.center_x < player.center_x - 2:

            self.change_x = self.velocidade
            self.texture = self.textura_direita

        elif self.center_x > player.center_x + 2:

            self.change_x = -self.velocidade
            self.texture = self.textura_esquerda

        else:

            self.change_x = 0


# Cria as moedas que o jogador pode coletar.
class Coin(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__(
            asset_path("coin.png"),
            scale=0.8
        )

        self.center_x = x
        self.center_y = y


# Efeito visual de explosao: toca a animacao uma vez e se remove sozinho.
class Explosao(arcade.Sprite):

    def __init__(self, x, y, quadros, scale=1.0):

        super().__init__(
            quadros[0],
            scale=scale
        )

        self.center_x = x
        self.center_y = y

        self.quadros = quadros
        self.quadro_atual = 0
        self.tempo_animacao = 0.0

    def update(self, delta_time=1 / 60):

        self.tempo_animacao += delta_time

        # Troca de quadro a cada 0,06 s.
        if self.tempo_animacao >= 0.06:

            self.tempo_animacao = 0.0
            self.quadro_atual += 1

            if self.quadro_atual >= len(self.quadros):

                self.remove_from_sprite_lists()
                return

            self.texture = self.quadros[self.quadro_atual]


# Tela principal do jogo.
class TelaInicial(arcade.View):

    def __init__(self):
        super().__init__()

    # Desenha os elementos na tela.
    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "COLETOR DE MOEDAS",
            LARGURA / 2,
            420,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [J] para Jogar",
            LARGURA / 2,
            330,
            arcade.color.LIGHT_SEA_GREEN,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [T] para Tutorial",
            LARGURA / 2,
            280,
            arcade.color.LIGHT_SEA_GREEN,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [D] para Desenvolvedores",
            LARGURA / 2,
            230,
            arcade.color.LIGHT_SEA_GREEN,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [ESC] para Sair",
            LARGURA / 2,
            140,
            arcade.color.LIGHT_SEA_GREEN,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [R] para ver o Top 10",
            LARGURA / 2,
            180,
            arcade.color.GOLD,
            18,
            anchor_x="center"
        )

    # Executa ações quando uma tecla é pressionada.
    def on_key_press(self, key, modifiers):

        if key == arcade.key.J:

            tela_jogo = JogoView()
            tela_jogo.setup()

            self.window.show_view(tela_jogo)

        elif key == arcade.key.T:

            tela_tutorial = TelaTutorial()
            self.window.show_view(tela_tutorial)

        elif key == arcade.key.D:

            tela_dev = TelaDesenvolvedores()
            self.window.show_view(tela_dev)

        elif key == arcade.key.R:

            self.window.show_view(TelaRanking())

        elif key == arcade.key.ESCAPE:

            arcade.close_window()


# Tela com os dez melhores tempos registrados.
class TelaRanking(arcade.View):

    def __init__(self):
        super().__init__()
        self.registros = list(
            Pontuacao.select().order_by(
                Pontuacao.tempo.asc(),
                Pontuacao.id.asc()
            ).limit(10)
        )

    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "TOP 10 MAIS RAPIDOS",
            LARGURA / 2,
            500,
            arcade.color.GOLD,
            30,
            anchor_x="center"
        )

        arcade.draw_text(
            "POS.       JOGADOR                         TEMPO",
            LARGURA / 2,
            440,
            arcade.color.LIGHT_SEA_GREEN,
            16,
            anchor_x="center"
        )

        if not self.registros:
            arcade.draw_text(
                "Ainda nao ha tempos registrados.",
                LARGURA / 2,
                350,
                arcade.color.LIGHT_GRAY,
                18,
                anchor_x="center"
            )

        for posicao, registro in enumerate(self.registros, start=1):
            arcade.draw_text(
                f"{posicao:>2}.          {registro.nome[:20]:<20}       {registro.tempo:.2f}s",
                LARGURA / 2,
                400 - (posicao - 1) * 30,
                arcade.color.WHITE,
                16,
                anchor_x="center"
            )

        arcade.draw_text(
            "Pressione [ESC] para voltar ao menu",
            LARGURA / 2,
            70,
            arcade.color.GRAY,
            14,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


# Tela que mostra as instruções do jogo.
class TelaTutorial(arcade.View):

    def __init__(self):
        super().__init__()

    # Desenha os elementos na tela.
    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "TUTORIAL",
            LARGURA / 2,
            450,
            arcade.color.WHITE,
            28,
            anchor_x="center"
        )

        arcade.draw_text(
            "Use as SETAS para mover para os lados.",
            LARGURA / 2,
            360,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center"
        )

        arcade.draw_text(
            "Use ESPAÇO ou SETA PARA CIMA para pular.",
            LARGURA / 2,
            310,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Colete {META_MOEDAS} moedas para vencer!",
            LARGURA / 2,
            260,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center"
        )

        arcade.draw_text(
            "Cuidado com os fantasmas!",
            LARGURA / 2,
            210,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [ESC] para voltar ao menu",
            LARGURA / 2,
            100,
            arcade.color.GRAY,
            14,
            anchor_x="center"
        )

    # Executa ações quando uma tecla é pressionada.
    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:

            self.window.show_view(TelaInicial())


# Tela com as informações do desenvolvedor.
class TelaDesenvolvedores(arcade.View):

    def __init__(self):

        super().__init__()

        self.lista_icones = arcade.SpriteList()

        self.fantasma_icon = arcade.Sprite(
            asset_path("fantasma_right.png"),
            scale=0.8
        )

        self.fantasma_icon.center_x = LARGURA / 2 - 130
        self.fantasma_icon.center_y = 330

        self.lista_icones.append(
            self.fantasma_icon
        )

    # Desenha os elementos na tela.
    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "DESENVOLVEDOR",
            LARGURA / 2,
            420,
            arcade.color.GOLD,
            28,
            anchor_x="center"
        )

        self.lista_icones.draw()

        arcade.draw_text(
            "Gustavo Regiani de Souza",
            LARGURA / 2 + 30,
            325,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [ESC] para voltar ao menu",
            LARGURA / 2,
            120,
            arcade.color.GRAY,
            14,
            anchor_x="center"
        )

    # Executa ações quando uma tecla é pressionada.
    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:

            self.window.show_view(TelaInicial())
def tile_to_px(tile_x, tile_y, map_height_tiles=25):
    px = tile_x * TILE_SIZE * 2
    py = (map_height_tiles - tile_y) * TILE_SIZE * 2
    return px, py

class GameView(arcade.View):
    def __init__(self, player_name: str, window=None):
        super().__init__(window)
        self.keys_pressed = set()
        self.tempo = 0.0
        self.collected_coins = 0
        self.alert_timer = 0.0

        self.player = Player(
            '../sprites/Frog/frog.png', PLAYER_SCALE, PLAYER_SPEED, PLAYER_MAX_HEALTH, player_name
        )
        self.player.center_x = 200
        self.player.center_y = 300
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # moedas
        self.coins = arcade.SpriteList()
        self.special_coins = arcade.SpriteList()

        # inimigos
        self.enemies = arcade.SpriteList()
        self.enemy_physics = []

        # tilemap
        self.tile_map = arcade.load_tilemap('../sprites/map/level_1.tmx', scaling=2.0)
        self.static_objects = self.tile_map.sprite_lists['Plataforms']
        self.background     = self.tile_map.sprite_lists['Background']

        # física do player
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.static_objects,
            gravity_constant=GRAVITY
        )

        self._spawn_static_coins()
        self._spawn_special_coin()
        self._spawn_enemies()

        # HUD
        self.score_label = arcade.Text(
            text='Score: 0',
            x=10, y=SCREEN_HEIGHT - 30,
            color=arcade.color.RED_DEVIL,
            font_size=16, bold=True
        )
        self.timer_label = arcade.Text(
            text='Tempo: 0s',
            x=10, y=SCREEN_HEIGHT - 60,
            color=arcade.color.WHITE,
            font_size=16,
        )
        self.alert_label = arcade.Text(
            text='',
            x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2,
            color=arcade.color.RED,
            font_size=28, bold=True,
            anchor_x='center',
        )

    def _spawn_static_coins(self):
        tentativas_max = 200
        geradas = 0
        tentativas = 0

        while geradas < TOTAL_STATIC_COINS and tentativas < tentativas_max:
            tentativas += 1
            coin = Coin('../sprites/Coin_tiles.png', COIN_SCALE, 1)
            coin.center_x = random.randint(50, SCREEN_WIDTH - 50)
            coin.center_y = random.randint(200, SCREEN_HEIGHT - 50)

            if not arcade.check_for_collision_with_list(coin, self.static_objects):
                self.coins.append(coin)
                geradas += 1

    def _spawn_special_coin(self):
        sc = SpecialCoin(scale=COIN_SCALE)
        sc.center_x = random.randint(100, SCREEN_WIDTH - 100)
        sc.center_y = random.randint(300, SCREEN_HEIGHT - 100)
        self.special_coins.append(sc)

    def _spawn_enemies(self):
        ninja = Enemy(scale=2.0, speed=2.0)
        ninja.center_x = 800
        ninja.center_y = 400
        self.enemies.append(ninja)
        self.enemy_physics.append(
            arcade.PhysicsEnginePlatformer(ninja, walls=self.static_objects, gravity_constant=GRAVITY)
        )

        pinkman = PinkMan(scale=2.0, speed=1.2)
        pinkman.center_x = 400
        pinkman.center_y = 400
        self.enemies.append(pinkman)
        self.enemy_physics.append(
            arcade.PhysicsEnginePlatformer(pinkman, walls=self.static_objects, gravity_constant=GRAVITY)
        )

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.player.on_key_press(key)
        if key == arcade.key.ESCAPE:
            from menu_view import MenuView
            self.window.show_view(MenuView())

    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)
        self.player.on_key_release(key)

    def on_draw(self):
        self.clear()
        self.background.draw()
        self.static_objects.draw()
        self.enemies.draw()
        self.player_list.draw()
        self.coins.draw()
        self.special_coins.draw()

        self.score_label.draw()
        self.timer_label.draw()

        if self.alert_timer > 0:
            self.alert_label.draw()

        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH - 210, SCREEN_WIDTH - 10,
            SCREEN_HEIGHT - 40, SCREEN_HEIGHT - 20,
            arcade.color.GRAY
        )
        hp_width = 200 * (self.player.health / self.player.max_health)
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH - 210, SCREEN_WIDTH - 210 + hp_width,
            SCREEN_HEIGHT - 40, SCREEN_HEIGHT - 20,
            arcade.color.RED
        )

    def on_update(self, delta_time):
        self.tempo += delta_time

        if self.alert_timer > 0:
            self.alert_timer -= delta_time

        self.player_list.update(delta_time, self.keys_pressed)
        self.physics_engine.update()
        on_ground = self.physics_engine.can_jump()
        self.player.is_on_ground = on_ground
        if on_ground:
            self.player.jumps_remaining = 2

        for i, enemy in enumerate(self.enemies):
            enemy.update(delta_time, player=self.player, walls=self.static_objects)
            self.enemy_physics[i].update()
            enemy.is_on_ground = self.enemy_physics[i].can_jump()
            if enemy.is_on_ground:
                enemy.jumps_remaining = 1

        self.coins.update(delta_time)
        self.special_coins.update(delta_time)

        for coin in arcade.check_for_collision_with_list(self.player, self.coins):
            self.player.score += coin.value
            self.collected_coins += 1
            coin.remove_from_sprite_lists()

        for sc in arcade.check_for_collision_with_list(self.player, self.special_coins):
            self.player.score += sc.value
            sc.remove_from_sprite_lists()
            self._spawn_special_coin()

        for enemy in arcade.check_for_collision_with_list(self.player, self.enemies):
            if enemy.on_hit_player(self.player):
                self.alert_label.text = '- 1 PONTO!'
                self.alert_timer = 1.0

        self.score_label.text = f'Score: {self.player.score}'
        self.timer_label.text = f'Tempo: {self.tempo:.1f}s'

        if self.collected_coins >= TOTAL_STATIC_COINS and len(self.coins) == 0:
            from game_over_view import GameOverView
            self.window.show_view(GameOverView(
                score=self.player.score,
                max_score=TOTAL_STATIC_COINS,
                tempo=self.tempo,
                nome=self.player.name
            ))

# Tela exibida quando o jogador vence.
# Tela exibida quando o jogador vence.
class TelaVitoria(arcade.View):

    def __init__(self, tempo_total=0, sem_dano=False, pontuacao=0):

        super().__init__()

        self.tempo_total = tempo_total
        self.sem_dano = sem_dano
        self.pontuacao = pontuacao

        # Texto que o jogador está digitando (começa vazio).
        self.nome_digitado = ""

    # Desenha os elementos na tela.
    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "VOCÊ VENCEU! PARABÉNS!",
            LARGURA / 2,
            ALTURA / 2 + 120,
            arcade.color.GOLD,
            30,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Você coletou {META_MOEDAS} moedas!",
            LARGURA / 2,
            ALTURA / 2 + 80,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        if self.sem_dano:

            arcade.draw_text(
                "Parabéns! Você não foi atingido nenhuma vez!",
                LARGURA / 2,
                ALTURA / 2 + 45,
                arcade.color.SPRING_GREEN,
                18,
                anchor_x="center"
            )

        else:

            arcade.draw_text(
                "Você foi atingido durante a partida.",
                LARGURA / 2,
                ALTURA / 2 + 45,
                arcade.color.RED,
                18,
                anchor_x="center"
            )

        pontuacao_final = self.pontuacao / self.tempo_total if self.tempo_total > 0 else 0

        tempo_formatado = f"{self.tempo_total:.2f}s"

        arcade.draw_text(
            f"Tempo total: {tempo_formatado}",
            LARGURA / 2,
            ALTURA / 2 + 10,
            arcade.color.GOLD,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Pontuação final: {pontuacao_final:.2f}",
            LARGURA / 2,
            ALTURA / 2 - 15,
            arcade.color.SKY_BLUE,
            18,
            anchor_x="center"
        )

        # Rótulo acima da caixa de texto.
        arcade.draw_text(
            "Digite seu nome e aperte ENTER:",
            LARGURA / 2,
            ALTURA / 2 - 40,
            arcade.color.WHITE,
            16,
            anchor_x="center"
        )

        # Contorno da caixa de texto.
        arcade.draw_rect_outline(
            arcade.XYWH(LARGURA / 2, ALTURA / 2 - 90, 360, 50),
            arcade.color.WHITE,
            border_width=2
        )

        # Nome digitado até agora (o "_" funciona como cursor).
        arcade.draw_text(
            self.nome_digitado + "_",
            LARGURA / 2,
            ALTURA / 2 - 90,
            arcade.color.YELLOW,
            22,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "[ESC] volta ao menu sem salvar",
            LARGURA / 2,
            ALTURA / 2 - 150,
            arcade.color.GRAY,
            14,
            anchor_x="center"
        )

    # Recebe cada caractere digitado (com maiúsculas, acentos e espaço).
    def on_text(self, text):

        if text.isprintable() and len(self.nome_digitado) < LIMITE_NOME:

            self.nome_digitado += text

    # Trata as teclas especiais.
    def on_key_press(self, key, modifiers):

        if key == arcade.key.BACKSPACE:

            self.nome_digitado = self.nome_digitado[:-1]

        elif key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:

            nome = self.nome_digitado.strip()

            if nome:

                tempo_salvo = round(float(self.tempo_total), 2)

                Pontuacao.create(
                    nome=nome,
                    tempo=tempo_salvo
                )

                self.window.show_view(TelaInicial())

        elif key == arcade.key.ESCAPE:

            self.window.show_view(TelaInicial())



# Tela exibida quando o jogador perde.
class TelaGameOver(arcade.View):

    def __init__(self):
        super().__init__()

    # Desenha os elementos na tela.
    def on_draw(self):

        self.clear()

        arcade.draw_text(
            "GAME OVER!",
            LARGURA / 2,
            ALTURA / 2 + 30,
            arcade.color.RED,
            30,
            anchor_x="center"
        )

        arcade.draw_text(
            "Você ficou devendo pros fantasmas!",
            LARGURA / 2,
            ALTURA / 2 - 20,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pressione [ESC] para voltar ao menu",
            LARGURA / 2,
            ALTURA / 2 - 80,
            arcade.color.GRAY,
            14,
            anchor_x="center"
        )

    # Executa ações quando uma tecla é pressionada.
    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:

            self.window.show_view(TelaInicial())


# Classe que controla a partida e toda a lógica do jogo.
class JogoView(arcade.View):

    def __init__(self):

        super().__init__()

        self.player = None

        self.lista_inimigos = None
        self.lista_player = None
        self.lista_plataformas = None
        self.lista_moedas = None

        self.fisica = None
        self.fisica_inimigo_gravidade = None

        self.inimigo_gravidade = None

        self.pontuacao = 0

        self.respawn_timer = 0
        self.aguardando_respawn = False

        self.tempo_inicio = 0

        self.timer_alerta = 0

        self.tomou_dano = False

        self.esquerda_pressionada = False
        self.direita_pressionada = False

        # Efeitos de colisao.
        self.lista_efeitos = arcade.SpriteList()
        self.tempo_flash = 0.0
        self.tempo_tremor = 0.0
        self.cooldown_explosao = 0.0
        self.timer_game_over = None
        self.camera = arcade.Camera2D()
        self.quadros_explosao = self.carregar_quadros_explosao()

    # Carrega e fatia a spritesheet da explosao (uma unica vez por partida).
    def carregar_quadros_explosao(self):

        caminho = asset_path("explosao.png")

        # Descobre a largura de cada quadro dividindo a folha em colunas.
        with Image.open(caminho) as imagem:
            largura_quadro = imagem.width // QUADROS_EXPLOSAO
            altura_quadro = imagem.height

        folha = arcade.load_spritesheet(caminho)

        return folha.get_texture_grid(
            size=(largura_quadro, altura_quadro),
            columns=QUADROS_EXPLOSAO,
            count=QUADROS_EXPLOSAO
        )

    # Cria a explosao no ponto de impacto (meio entre jogador e inimigo).
    def criar_explosao(self, inimigo):

        x = (self.player.center_x + inimigo.center_x) / 2
        y = (self.player.center_y + inimigo.center_y) / 2

        self.lista_efeitos.append(
            Explosao(
                x,
                y,
                self.quadros_explosao,
                scale=ESCALA_EXPLOSAO
            )
        )

        self.cooldown_explosao = TEMPO_ENTRE_EXPLOSOES

    # Cria e configura todos os elementos da partida.
    def setup(self):

        self.lista_efeitos = arcade.SpriteList()
        self.tempo_flash = 0.0
        self.tempo_tremor = 0.0
        self.cooldown_explosao = 0.0
        self.timer_game_over = None
        self.camera.position = (LARGURA / 2, ALTURA / 2)

        self.pontuacao = 0

        self.respawn_timer = 0
        self.aguardando_respawn = False

        self.tempo_inicio = time.time()

        self.timer_alerta = 0

        self.tomou_dano = False

        self.esquerda_pressionada = False
        self.direita_pressionada = False

        self.player = Player()

        # Lista que guarda o jogador.
        self.lista_player = arcade.SpriteList()

        self.lista_player.append(
            self.player
        )

        # Lista que guarda todos os inimigos da fase.
        self.lista_inimigos = arcade.SpriteList()

        inimigo_grande = Inimigo(
            500,
            300,
            False
        )

        inimigo_pequeno = Inimigo(
            400,
            250,
            True
        )

        self.inimigo_gravidade = InimigoGravidade(
            650,
            500
        )

        self.lista_inimigos.append(
            inimigo_grande
        )

        self.lista_inimigos.append(
            inimigo_pequeno
        )

        self.lista_inimigos.append(
            self.inimigo_gravidade
        )

        # Lista que guarda o chão e as plataformas.
        self.lista_plataformas = arcade.SpriteList(
            use_spatial_hash=True
        )

        for x in range(32, LARGURA + 32, 64):

            chao = Bloco(
                x=x,
                y=20,
                largura=64,
                altura=40
            )

            self.lista_plataformas.append(
                chao
            )

        plataformas = [
            (200, 150),
            (400, 250),
            (600, 200),
            (300, 400),
            (550, 400)
        ]

        for px, py in plataformas:

            plataforma = Bloco(
                px,
                py,
                100,
                30
            )

            self.lista_plataformas.append(
                plataforma
            )

        # Lista que guarda as moedas.
        self.lista_moedas = arcade.SpriteList(
            use_spatial_hash=True
        )

        moedas_pos = [
            (200, 200),
            (400, 300),
            (600, 250),
            (300, 450),
            (550, 450)
        ]

        for mx, my in moedas_pos:

            moeda = Coin(
                mx,
                my
            )

            self.lista_moedas.append(
                moeda
            )

        # Física responsável pelo movimento e pelos pulos do jogador.
        self.fisica = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.lista_plataformas,
            gravity_constant=GRAVIDADE
        )

        # Física usada pelo inimigo que sofre gravidade.
        self.fisica_inimigo_gravidade = arcade.PhysicsEnginePlatformer(
            self.inimigo_gravidade,
            walls=self.lista_plataformas,
            gravity_constant=GRAVIDADE
        )

    # Desenha os elementos na tela.
    def on_draw(self):

        self.clear()

        arcade.set_background_color(
            arcade.color.SKY_BLUE
        )

        # Mundo do jogo desenhado atraves da camera que pode tremer.
        self.camera.use()

        arcade.draw_circle_filled(
            120,
            530,
            30,
            arcade.color.WHITE
        )

        arcade.draw_circle_filled(
            150,
            530,
            40,
            arcade.color.WHITE
        )

        arcade.draw_circle_filled(
            185,
            530,
            30,
            arcade.color.WHITE
        )

        self.lista_plataformas.draw()

        self.lista_moedas.draw()

        self.lista_player.draw()

        self.lista_inimigos.draw()

        # Explosoes por cima de tudo.
        self.lista_efeitos.draw()

        # Camera fixa da janela: flash e HUD nao tremem.
        self.window.default_camera.use()

        if self.tempo_flash > 0:

            alpha = int(
                ALPHA_FLASH * self.tempo_flash / TEMPO_FLASH
            )

            arcade.draw_rect_filled(
                arcade.XYWH(
                    LARGURA / 2,
                    ALTURA / 2,
                    LARGURA,
                    ALTURA
                ),
                (255, 0, 0, alpha)
            )

        arcade.draw_text(
            f"Moedas: {self.pontuacao}/{META_MOEDAS}",
            10,
            ALTURA - 30,
            arcade.color.RED,
            20,
            bold=True
        )

        tempo_decorrido = int(
            time.time() - self.tempo_inicio
        )

        arcade.draw_text(
            f"Tempo: {tempo_decorrido}s",
            10,
            ALTURA - 60,
            arcade.color.WHITE,
            18,
            bold=True
        )

        if self.timer_alerta > 0:

            arcade.draw_text(
                "Você perdeu uma moeda!",
                LARGURA / 2,
                ALTURA - 40,
                arcade.color.RED,
                20,
                anchor_x="center",
                bold=True
            )

    # Recria as moedas do mapa.
    def resetar_moedas(self):

        self.lista_moedas.clear()
        self.aguardando_respawn = False
        self.respawn_timer = 0

        moedas_pos = [
            (200, 200),
            (400, 300),
            (600, 250),
            (300, 450),
            (550, 450)
        ]

        for mx, my in moedas_pos:

            moeda = Coin(
                mx,
                my
            )

            self.lista_moedas.append(
                moeda
            )

    # Atualiza a lógica do jogo a cada instante.
    def on_update(self, delta_time):

        if self.esquerda_pressionada:

            self.player.change_x = -VELOCIDADE

        elif self.direita_pressionada:

            self.player.change_x = VELOCIDADE

        else:

            self.player.change_x = 0

        self.fisica.update()

        if self.player.left < 0:

            self.player.left = 0

        if self.player.right > LARGURA:

            self.player.right = LARGURA

        for inimigo in self.lista_inimigos:

            if inimigo is self.inimigo_gravidade:
                continue

            inimigo.atualizar(
                self.player
            )

        self.inimigo_gravidade.decidir_direcao(
            self.player
        )

        no_chao = (
            self.fisica_inimigo_gravidade.can_jump()
        )

        if (
            no_chao
            and self.player.center_y >
            self.inimigo_gravidade.center_y + 30
        ):

            self.inimigo_gravidade.change_y = (
                self.inimigo_gravidade.forca_pulo
            )

        self.fisica_inimigo_gravidade.update()

        if self.inimigo_gravidade.left < 0:

            self.inimigo_gravidade.left = 0

        if self.inimigo_gravidade.right > LARGURA:

            self.inimigo_gravidade.right = LARGURA

        if self.timer_alerta > 0:

            self.timer_alerta -= delta_time

        # Desconta o tempo dos efeitos (nunca abaixo de zero).
        self.tempo_flash = max(0.0, self.tempo_flash - delta_time)
        self.tempo_tremor = max(0.0, self.tempo_tremor - delta_time)
        self.cooldown_explosao = max(
            0.0, self.cooldown_explosao - delta_time
        )

        self.lista_efeitos.update(delta_time)

        if self.player.i_frame:

            self.player.i_frame_time -= delta_time

            if self.player.i_frame_time <= 0:

                self.player.i_frame = False

        # Verifica se o jogador encostou em algum inimigo.
        colisao_inimigo = (
            arcade.check_for_collision_with_list(
                self.player,
                self.lista_inimigos
            )
        )

        for inimigo in colisao_inimigo:

            # A explosao aparece a cada toque do fantasma no jogador,
            # mesmo durante a imunidade (com um intervalo minimo).
            if self.cooldown_explosao <= 0:

                self.criar_explosao(inimigo)

            if not self.player.i_frame:

                self.pontuacao -= 1

                self.timer_alerta = 1.5

                self.tomou_dano = True

                # Flash e tremor so quando o jogador realmente leva dano.
                self.tempo_flash = TEMPO_FLASH
                self.tempo_tremor = TEMPO_TREMOR

                if inimigo.pequeno:

                    inimigo.teleportar()

                else:

                    self.player.i_frame = True
                    self.player.i_frame_time = 1.0

        # Piscar: alterna a transparencia enquanto o jogador esta imune.
        if self.player.i_frame:

            if int(self.player.i_frame_time * 10) % 2 == 0:

                self.player.alpha = 80

            else:

                self.player.alpha = 255

        else:

            self.player.alpha = 255

        # Tremor: camera sacode com forca decrescente e volta ao centro.
        if self.tempo_tremor > 0:

            forca = (
                INTENSIDADE_TREMOR
                * self.tempo_tremor / TEMPO_TREMOR
            )

            self.camera.position = (
                LARGURA / 2 + random.uniform(-forca, forca),
                ALTURA / 2 + random.uniform(-forca, forca)
            )

        else:

            self.camera.position = (LARGURA / 2, ALTURA / 2)

        # Verifica quais moedas foram coletadas pelo jogador.
        moedas_coletadas = (
            arcade.check_for_collision_with_list(
                self.player,
                self.lista_moedas
            )
        )

        for moeda in moedas_coletadas:

            moeda.remove_from_sprite_lists()

            self.pontuacao += 1

        # Verifica se o jogador atingiu a meta.
        if self.pontuacao >= META_MOEDAS:

            tempo_total = (
                time.time() - self.tempo_inicio
            )

            tela_vitoria = TelaVitoria(
                tempo_total,
                sem_dano=not self.tomou_dano, 
                pontuacao=self.pontuacao
            )

            self.window.show_view(
                tela_vitoria
            )

            return

        # Verifica se a pontuação chegou ao limite de derrota.
        if self.pontuacao <= -1:

            # Espera um instante para a explosao aparecer antes do Game Over.
            if self.timer_game_over is None:

                self.timer_game_over = ATRASO_GAME_OVER

            else:

                self.timer_game_over -= delta_time

            if self.timer_game_over <= 0:

                tela_game_over = TelaGameOver()

                self.window.show_view(
                    tela_game_over
                )

            return

        if len(self.lista_moedas) == 0:

            if not self.aguardando_respawn:

                self.aguardando_respawn = True

                self.respawn_timer = 0.5

            else:

                self.respawn_timer -= delta_time

                if self.respawn_timer <= 0:

                    self.resetar_moedas()

                    self.aguardando_respawn = False

        if self.player.top < 0:

            self.setup()

    # Executa ações quando uma tecla é pressionada.
    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:

            self.window.show_view(
                TelaInicial()
            )

        elif key == arcade.key.LEFT:

            self.esquerda_pressionada = True

            self.player.texture = arcade.load_texture(
                asset_path("Homem-Aranha andando esquerda 1.png")
            )

        elif key == arcade.key.RIGHT:

            self.direita_pressionada = True

            self.player.texture = arcade.load_texture(
                asset_path("Homem-Aranha andando direita 1.png")
            )

        elif key in (
            arcade.key.SPACE,
            arcade.key.UP
        ):

            if self.fisica.can_jump():

                self.player.change_y = VELOCIDADE_PULO

        elif key == arcade.key.L:

            self.resetar_moedas()

    # Executa ações quando uma tecla é solta.
    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT:

            self.esquerda_pressionada = False

            if self.direita_pressionada:

                self.player.change_x = VELOCIDADE

                self.player.texture = arcade.load_texture(
                    asset_path("Homem-Aranha andando direita 1.png")
                )

            else:

                self.player.change_x = 0

                self.player.texture = arcade.load_texture(
                    asset_path("Homem-Aranha stand direita.png")
                )

        elif key == arcade.key.RIGHT:

            self.direita_pressionada = False

            if self.esquerda_pressionada:

                self.player.change_x = -VELOCIDADE

                self.player.texture = arcade.load_texture(
                    asset_path("Homem-Aranha andando esquerda 1.png")
                )

            else:

                self.player.change_x = 0

                self.player.texture = arcade.load_texture(
                    asset_path("Homem-Aranha stand direita.png")
                )


# Cria a janela e inicia o jogo.
def main():

    janela = arcade.Window(
        LARGURA,
        ALTURA,
        TITULO
    )

    menu = TelaInicial()

    janela.show_view(menu)

    arcade.run()


if __name__ == "__main__":
    main()
