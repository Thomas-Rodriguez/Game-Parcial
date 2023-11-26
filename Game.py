import pygame
import sys
import sqlite3
import os

from Scripts.utils import load_image, load_images, Animation
from Scripts.entities import Player, Enemy
from Scripts.tilemap import Tilemap
from Scripts.clouds import Clouds
from Scripts.text_menu import MenuItem
from reference import *


class Tittle:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode([640, 480])
        pygame.display.set_caption("GAME")

        self.background = pygame.image.load("data/images/pixel_night_art.jpg")
        self.background = pygame.transform.scale(self.background, (640, 480))
        
        self.font = pygame.font.Font("PressStart2P-Regular.ttf", 20)

        self.info_text = self.font.render("UTN Parcial 2 @ 2023", True, BLACK)

        self.image_title = pygame.image.load("data/images/titlecard.png").convert()
        self.image_title.set_colorkey((0, 0, 0))
        self.image_title = pygame.transform.scale(self.image_title, (250, 150))

        self.main_menu = MenuItem("Play Game", WHITE, 210, 220, 200, 50, self.screen, self.font, spacing=(10, 20))
        self.high_score = MenuItem("High Score", WHITE, 210, 270, 200, 50, self.screen, self.font, spacing=(10, 20))
        self.credits = MenuItem("Credits", WHITE, 210, 320, 200, 50, self.screen, self.font, spacing=(35, 20))
        self.exit_txt = MenuItem("Exit", WHITE, 210, 370, 200, 50, self.screen, self.font, spacing=(60, 20))


        self.click_pos = [0,0]

        self.transparency = 0
        self.fading = 10
        self.max_trans = 255
        self.circle_radius = 30

        self.flag_run = True
        self.fade_in = True
        self.flag_appear_text = False
        self.clock = pygame.time.Clock()

        #Timer
        self.five_ticks = pygame.USEREVENT
        pygame.time.set_timer(self.five_ticks, 1500)

        # self.music_on_off = True

    def run(self):

        if self.flag_run:
            # if self.music_on_off:
            pygame.mixer.music.load("data/music.wav")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            # else:
            #     pygame.mixer.music.stop()


        while self.flag_run:
            list_event = pygame.event.get()
            for event in list_event:
                if event.type == pygame.QUIT:
                   self.flag_run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_pos = list(event.pos)
                    if (self.click_pos[0] > 210 and self.click_pos[0] < 410) and (self.click_pos[1] > 220 and self.click_pos[1] < 270):
                        pygame.mixer.music.stop()
                        Game().run()
                    if (self.click_pos[0] > 210 and self.click_pos[0] < 410) and (self.click_pos[1] > 270 and self.click_pos[1] < 320):
                        HighScores().run()
                    if (self.click_pos[0] > 210 and self.click_pos[0] < 410) and (self.click_pos[1] > 320 and self.click_pos[1] < 370):
                        Credits().run()
                    if (self.click_pos[0] > 210 and self.click_pos[0] < 410) and (self.click_pos[1] > 370 and self.click_pos[1] < 420):
                        self.flag_run = False
                
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_m:
                #         self.music_on_off = False

                if event.type == pygame.USEREVENT:
                    if event.type == self.five_ticks:
                        self.flag_appear_text = True

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.info_text,(240, 460))
            self.screen.blit(self.image_title, (180, 65))

            if self.flag_appear_text:
                if self.fade_in:
                    if self.transparency < self.max_trans:
                        self.transparency += self.fading
                    else:
                        self.fade_in = False
                else:
                    if self.transparency > 25:
                        self.transparency -= self.fading
                    else:
                        self.fade_in = True

            self.main_menu.draw_text(self.transparency)
            self.high_score.draw_text(self.transparency)
            self.credits.draw_text(self.transparency)
            self.exit_txt.draw_text(self.transparency)

            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()

class AskName:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Enter Your Name")

    def get_player_name(self):
        input_active = True
        player_name = ""
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode.isalpha() and len(player_name) < 3:
                        player_name += event.unicode

            self.screen.fill((0, 0, 0))  # Set the background color

            font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
            text_enter_name = font.render("Enter your name (3 letters):", True, (255, 255, 255))
            text_name = font.render(player_name, True, (255, 255, 255)) 

            rect_enter_name = text_enter_name.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
            rect_name = text_name.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))

            self.screen.blit(text_enter_name, rect_enter_name.topleft)
            self.screen.blit(text_name, rect_name.topleft)

            pygame.display.flip()
            pygame.time.Clock().tick(30)

        return player_name.upper()

import random
import string

class Game:
    def __init__(self):
        self.ask_name = AskName()
        self.player_name = self.ask_name.get_player_name()

        pygame.init()

        pygame.display.set_caption("PLat game")
        self.screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320,240)) 
        
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font("PressStart2P-Regular.ttf", 20)

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), duration=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), duration=4),
            'player/idle': Animation(load_images('entities/player/idle'), duration=6),
            'player/run': Animation(load_images('entities/player/run'), duration=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        self.sound = {
            "jump": pygame.mixer.Sound("data/sfx/jump.wav"),
            "dash": pygame.mixer.Sound("data/sfx/dash.wav"),
            "ambience": pygame.mixer.Sound("data/sfx/ambience.wav"),
            "megalovania": pygame.mixer.Sound("data/sfx/megalovania.wav")
        }

        self.sound["jump"].set_volume(1)
        self.sound["dash"].set_volume(0.1)
        self.sound["ambience"].set_volume(0.2)
        self.sound["megalovania"].set_volume(0.5)
        
        self.clouds = Clouds(self.assets['clouds'], count=16)
        
        self.player = Player(self, (50, 50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.movement = [False, False]

        self.score = self.player.score 
        self.timer = 0
        self.score_decrement_interval = 30 

        self.level = 0
        self.load_level(self.level)

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.airtime = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
            
        self.projectiles = []        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition_l = -30

    def update_score(self, player_name, new_score):
        with sqlite3.connect("High_score_sqlite/bd_btf.db") as connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO score (name, score) VALUES (?, ?)", (player_name, new_score))
                connection.commit()
            except sqlite3.OperationalError as e:
                print("Error updating score:", e)
        
    def run(self):
        self.sound["ambience"].play(-1)
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            if self.timer % self.score_decrement_interval == 0:
                self.score -= 1
                self.update_score(self.player_name, self.player.score)
                self.timer = 0  # Reset the timer after updating the score

 
            if not len(self.enemies):
                self.transition_l += 1
                if self.transition_l > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    if self.level > 3:
                        # Player has completed level 3, end the game and go back to the title screen
                        self.update_score(self.player_name, self.player.score)
                        self.sound["ambience"].stop()
                        Tittle().run()
                        return  # Exit the game loop
                    self.load_level(self.level)
                    self.update_score(self.player_name, self.player.score)
            if self.transition_l < 0:
                self.transition_l += 1
            
            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition_l = min(30, self.transition_l + 1)
                if self.dead > 40:
                    self.load_level(self.level)
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
                    self.player.score += 100
                    self.update_score(self.player_name, self.player.score)
            
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
            
            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
            
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jump():
                            self.sound["jump"].play()
                    if event.key == pygame.K_x:
                        self.player.dash()
                    if event.key == pygame.K_ESCAPE:
                        self.sound["ambience"].stop()
                        self.update_score(self.player_name, self.player.score)
                        Tittle().run()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            if self.transition_l:
                transition_surface = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surface, (255,255,255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition_l))* 8)
                transition_surface.set_colorkey((255,255,255))
                self.display.blit(transition_surface, (0,0))
            
            score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
            self.display.blit(score_text, (10, 10))
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))    
            pygame.display.update()  # updates the screen
            self.clock.tick(60)  # dynamic sleep to run at 60fps
            self.timer += 1
    pygame.quit()

class Credits:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode([640, 480])
        pygame.display.set_caption("CREDITS")

        self.background = pygame.image.load("data/images/Bee3.png") 
        self.background = pygame.transform.scale(self.background, (640, 480))
        
        self.font = pygame.font.Font("PressStart2P-Regular.ttf", 10)
        self.txt = [("NARRATOR:(Black screen with text; The sound of buzzing bees",15),
            ("can be heard) According to all known laws of aviation, : there", 30),
            ("is no way a beeshould be able to fly: Its wings are too", 45),
            ("small to get its fat little body off the ground. The bee,", 60),
            ("of course, flies anyway because bees don't care what humans think is impossible.", 75),
            ("BARRY BENSON: (Barry is picking out a shirt) Yellow, black. Yellow, black.", 90),
            ("Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little.", 105),
            ("JANET BENSON: Barry! Breakfast is ready! BARRY:", 120),
            ("Coming! Hang on a second. (Barry uses his antenna like a phone)", 135),
            ("Hello? ADAM FLAYMAN: (Through phone)- Barry?", 150),
            ("BARRY:- Adam? ADAM: - Can you believe this is happening?", 165),
            ("BARRY:- I can't. I'll pick you up. (Barry flies down the stairs) MARTIN BENSON",180),
            ("Looking sharp. JANET: Use the stairs. Your father paid good money for those.",195),
            ("BARRY: Sorry. I'm excited. MARTIN: Here's the graduate. We're very proud of you, son.",210),
            ("A perfect report card, all B's. JANET: Very proud.",225),
            ("Rubs Barry's hair) BARRY: Ma! I got a thing going here.",240),
            ("JANET: - You got lint on your fuzz. BARRY: - Ow! That's me!",255),
            ("JANET: - Wave to us! We'll be in row 118,000. - Bye! (Barry flies out the door)",270),
            ("JANET: Barry, I told you, stop flying in the house! (Barry drives through",285),
            ("the hive,and is waved at by Adam who is reading a newspaper",300),
            ("BARRY= - Hey, Adam. ADAM: - Hey, Barry. (Adam gets in Barry's car)",315)]
        self.credits = [MenuItem(line, BLACK, 1, y, 0, 0, self.screen, self.font, spacing=(10, 20)) for line, y in self.txt]
        self.click_pos = [0,0]
        self.flag_cred = True
        self.transparency = 500

        self.back = pygame.image.load("data/images/Back.jpg")
        self.back = pygame.transform.scale(self.back, (50, 50))

    def run(self):
        while self.flag_cred:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.back, (500, 376))

            for credit_item in self.credits:
                credit_item.draw_text(self.transparency)

            list_event = pygame.event.get()
            for event in list_event:
                if event.type == pygame.QUIT:
                    self.flag_cred = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_pos = list(event.pos)
                    if (50 < self.click_pos[0] < 550) and (50 < self.click_pos[1] < 426):
                        self.flag_cred = False
                        Tittle().run()

            pygame.display.flip()
        pygame.quit()

class HighScores:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("HIGH SCORES")

        self.background = pygame.image.load("data/images/peaksundown.jpg") 
        self.background = pygame.transform.scale(self.background, (640, 480))

        self.popup_message = None

        self.random_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        self.random_score = f"{random.randint(0, 2000):03d}"

        with sqlite3.connect("High_score_sqlite/bd_btf.db") as conexion:
            try:
                sentencia = '''CREATE TABLE IF NOT EXISTS score
              (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    score TEXT
                )
                '''
                conexion.execute(sentencia)

                insert_sentencia = "INSERT INTO score (name, score) VALUES (?, ?)"
                values = (self.random_letters, " " + self.random_score)
                conexion.execute(insert_sentencia, values)

                conexion.commit()

            except sqlite3.OperationalError as e:
                print("Error creating table:", e)

        self.font = pygame.font.Font("PressStart2P-Regular.ttf", 20)

    def show_popup_message(self, text):
        self.popup_message = {'text': text, 'timer': 1000}

    def get_scores(self):
        with sqlite3.connect("High_score_sqlite/bd_btf.db") as connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT name, score FROM score ORDER BY score DESC")
                scores = cursor.fetchall()
                return scores
            except sqlite3.OperationalError as e:
                print("Error retrieving scores:", e)
                return []
            
    def delete_scores(self):        
        with sqlite3.connect("High_score_sqlite/bd_btf.db") as conexion:
            try:
                table_name = 'score'

                select_statement = f'SELECT id FROM {table_name} ORDER BY score DESC LIMIT 1'
                result = conexion.execute(select_statement).fetchone()

                if result:
                    id_to_keep = result[0]

                    delete_statement = f'DELETE FROM {table_name} WHERE id != ?'
                    conexion.execute(delete_statement, (id_to_keep,))

                    conexion.commit()

                    print(f"Records deleted successfully, keeping only the record with ID {id_to_keep}")
                else:
                    print("No records found.")
            except sqlite3.OperationalError as e:
                print("Error deleting records:", e)


    def run(self):
        scores = self.get_scores()

        running = True
        while running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Tittle().run()
                    if event.key == pygame.K_r:
                        self.delete_scores()
                        scores = self.get_scores()
                        self.show_popup_message("Data erased :3")
                    if event.key == pygame.K_PLUS:
                        scores = self.get_scores()
                        print("pushed")

            if self.popup_message:
                transparency = 255
                text = MenuItem(self.popup_message['text'], PURPLE, 320, 240, 200, 50, self.screen, self.font)
                text.draw_text(transparency)
                self.popup_message['timer'] -= 1
                if self.popup_message['timer'] <= 0:
                    self.popup_message = None 

            info_text = self.font.render("NAME - SCORE", True, (0, 0, 0))
            self.screen.blit(info_text, (50, 100))
            y_pos = 110
            for name, score in scores:
                transparency = 100
                text =self.main_menu = MenuItem(f"{name}: {score}", BLACK, 200, y_pos, 200, 50, self.screen, self.font, spacing=(10, 20))
                text.draw_text(transparency)
                y_pos += 40
                

            pygame.display.flip()

        pygame.quit()

Tittle().run()