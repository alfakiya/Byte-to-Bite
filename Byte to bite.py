import pygame
import sys

# Inisialisasi
pygame.init()
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption('Byte to bite')

# Warna
GRAY = (200, 200, 200)
BLUE = (52, 152, 219)    
GREEN = (46, 204, 113)   
RED = (231, 76, 60)   
BROWN = (209, 134, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#game state
INTRO_1 = 0
INTRO_2 = 1
INTRO_3 = 2
INTRO_4 = 3
MAIN_MENU = 4
GAME_1 = 5
GAME_2 = 6
GAME_3 = 7
GAME_4 = 8
GAME_5 = 9
CHOPPING = 10
MIXTURE = 11
TOAST = 12
NUTRI_CARD = 13
EARTH_END = 14

# class masak Banana French Toast

class ChoppingStage:
    def __init__(self):
        self.game_state = "PLAYING"
        #buat bar
        self.bar_x = 50       
        self.bar_y = 500      
        self.bar_width = 300  
        self.bar_height = 25
        self.target_width = 70  
        self.target_x = self.bar_x + (self.bar_width // 2) - (self.target_width // 2)
        self.indicator_x = self.bar_x
        self.indicator_speed = 6
        self.banana_index = 0  
        self.total_stages = 6  

        self.chopping_images = [
            pygame.image.load("chop 1.png").convert(),
            pygame.image.load("chop 2.png").convert(),
            pygame.image.load("chop 3.png").convert(),
            pygame.image.load("chop 4.png").convert(),
            pygame.image.load("chop 5.png").convert(),
            pygame.image.load("chop 6.png").convert() 
        ]
        self.chopping_images = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in self.chopping_images]

        self.feedback_text = ""
        self.feedback_color = GREEN
        self.feedback_timer = 0 

        self.font_main = pygame.font.SysFont("Arial Black", 18, bold=True)
        self.font_feedback = pygame.font.SysFont("Arial Black", 28, bold=True)

        self.img_next_button = pygame.image.load("next.png").convert_alpha()
        self.img_next_button = pygame.transform.scale(self.img_next_button, (200, 250))
        self.next_button_rect = self.img_next_button.get_rect(topleft=(100, 400))

    def handle_events(self, event):
        if self.game_state == "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.target_x <= self.indicator_x <= (self.target_x + self.target_width):
                    self.feedback_text = "PERFECT!"
                    self.feedback_color = GREEN
                    self.feedback_timer = 30
                    self.banana_index += 1
                    if self.banana_index >= self.total_stages - 1:
                        self.banana_index = self.total_stages - 1
                        self.game_state = "DONE_PLAYING"
                else:
                    self.feedback_text = "MISS!"
                    self.feedback_color = RED
                    self.feedback_timer = 30

        elif self.game_state == "DONE_PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.next_button_rect.collidepoint(event.pos):
                    self.game_state = "GO_NEXT"
                    

    def update(self):
        if self.game_state == "PLAYING":
            self.indicator_x += self.indicator_speed
            if self.indicator_x >= (self.bar_x + self.bar_width) or self.indicator_x <= self.bar_x:
                self.indicator_speed *= -1

            if self.feedback_timer > 0:
                self.feedback_timer -= 1
            else:
                self.feedback_text = ""
        elif self.game_state == "GO_NEXT":
            return "DONE"
        return "PLAYING"

    def draw(self, screen):
        screen.blit(self.chopping_images[self.banana_index], (0, 0))
        if self.game_state == "PLAYING":
            pygame.draw.rect(screen, GRAY, (self.bar_x, self.bar_y, self.bar_width, self.bar_height))
            pygame.draw.rect(screen, GREEN, (self.target_x, self.bar_y, self.target_width, self.bar_height))
            pygame.draw.rect(screen, RED, (self.indicator_x, self.bar_y - 5, 5, self.bar_height + 10))

            text_inst = self.font_main.render("PRESS SPACE AT THE GREEN BAR!", True, BLACK)
            screen.blit(text_inst, (20, 460))
            if self.feedback_text != "":
                text_feed = self.font_feedback.render(self.feedback_text, True, self.feedback_color)
                screen.blit(text_feed, (130, 200))
        elif self.game_state == "DONE_PLAYING":
             screen.blit(self.img_next_button, self.next_button_rect.topleft)


class Ingredient:
    def __init__(self, nama, nama_gambar, x, y, ukuran):
        self.nama = nama
        self.image = pygame.transform.scale(pygame.image.load(nama_gambar).convert_alpha(), ukuran)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_dragging = False
        self.is_inside_bowl = False

    def draw(self, screen):
        if not self.is_inside_bowl:
            screen.blit(self.image, self.rect)


class MixtureStage:
    def __init__(self):
        self.game_state = "DRAG_DROP" 
        self.bowl_rect = pygame.Rect(120, 340, 160, 140)
        self.ingredients = [
            Ingredient("Egg", "egg.png", 50, 100, (60, 150)),
            Ingredient("Milk", "milk.png", 165, 130, (100,100 )),
            Ingredient("Sugar", "sugar.png", 295, 140, (100, 100))
        ]
        self.mix_progress = 0
        self.target_mix = 100
        self.last_mouse_x = 0  

        self.roti_image = pygame.image.load("bread_0.png").convert_alpha()
        self.roti_image = pygame.transform.scale(self.roti_image, (200, 300))
        self.roti_rect = self.roti_image.get_rect(topleft=(155, 130))
        self.roti_is_dragging = False

        self.bg_images = {
            "kosong": pygame.transform.scale(pygame.image.load("bowl.png").convert(), (400, 600)),
            "belum_rata": pygame.transform.scale(pygame.image.load("mixing_0.png").convert(), (400, 600)),
            "rata": pygame.transform.scale(pygame.image.load("mixing_2.png").convert(), (400, 600)),
            "roti_basah": pygame.transform.scale(pygame.image.load("coating1.png").convert(), (400, 600))
        }
        self.img_next_button = pygame.image.load("next.png").convert_alpha()
        self.img_next_button = pygame.transform.scale(self.img_next_button, (200, 250))
        self.next_button_rect = self.img_next_button.get_rect(topleft=(100, 430))

        self.font_title = pygame.font.SysFont("Arial Black", 16, bold=True)
        self.font_desc = pygame.font.SysFont("Arial Black", 14, bold=True)

    def handle_events(self, event):
        if self.game_state == "DRAG_DROP":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for ing in self.ingredients:
                    if not ing.is_inside_bowl and ing.rect.collidepoint(event.pos):
                        ing.is_dragging = True
                        break
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for ing in self.ingredients:
                    if ing.is_dragging:
                        ing.is_dragging = False
                        if ing.rect.colliderect(self.bowl_rect):
                            ing.is_inside_bowl = True
            elif event.type == pygame.MOUSEMOTION:
                for ing in self.ingredients:
                    if ing.is_dragging:
                        ing.rect.center = event.pos

        elif self.game_state == "MIXING":
            if event.type == pygame.MOUSEMOTION:
                if self.bowl_rect.collidepoint(event.pos):
                    if abs(event.pos[0] - self.last_mouse_x) > 5:
                        self.mix_progress += 1
                    self.last_mouse_x = event.pos[0]

        elif self.game_state == "DIPPING":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.roti_rect.collidepoint(event.pos):
                    self.roti_is_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.roti_is_dragging:
                    self.roti_is_dragging = False
                    if self.roti_rect.colliderect(self.bowl_rect):
                        self.game_state = "DONE_PLAYING"
            elif event.type == pygame.MOUSEMOTION:
                if self.roti_is_dragging:
                    self.roti_rect.center = event.pos

        elif self.game_state == "DONE_PLAYING":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.next_button_rect.collidepoint(event.pos):
                    self.game_state = "GO_NEXT"

    def update(self):
        if self.game_state == "DRAG_DROP":
            if all(ing.is_inside_bowl for ing in self.ingredients):
                self.game_state = "MIXING"
        elif self.game_state == "MIXING":
            if self.mix_progress >= self.target_mix:
                self.game_state = "DIPPING"
        elif self.game_state == "GO_NEXT":
            return "DONE"
        return "PLAYING"

    def draw(self, screen):
        if self.game_state == "DRAG_DROP":
            screen.blit(self.bg_images["kosong"], (0, 0))
            txt_title = self.font_title.render("ADD THE INGREDIENTS!", True, (0, 0, 0))
            txt_desc = self.font_desc.render("Drag Egg, Milk and Sugar into the bowl", True, (80, 80, 80))
            screen.blit(txt_title, (80, 40))
            screen.blit(txt_desc, (50, 75))
            for ing in self.ingredients:
                ing.draw(screen)
        elif self.game_state == "MIXING":
            if self.mix_progress < 50:
                screen.blit(self.bg_images["belum_rata"], (0, 0))
            else:
                screen.blit(self.bg_images["rata"], (0, 0))
            txt_title = self.font_title.render("MIX THE INGEDIENTS!", True, (0, 0, 0))
            screen.blit(txt_title, (90, 40))
            pygame.draw.rect(screen, (189, 195, 199), (100, 280, 200, 15))
            pygame.draw.rect(screen, (46, 204, 113), (100, 280, int(self.mix_progress * 2), 15))
        elif self.game_state == "DIPPING":
            screen.blit(self.bg_images["rata"], (0, 0))
            screen.blit(self.roti_image, self.roti_rect)
        elif self.game_state == "DONE_PLAYING":
            screen.blit(self.bg_images["roti_basah"], (0, 0))
            screen.blit(self.img_next_button, self.next_button_rect.topleft)


class ToastStage:
    def __init__(self):
        self.temp_value = 50        
        self.heat_speed = 0.4       
        self.cool_power = 8         
        self.cook_progress = 0      
        self.max_cook = 100
        self.game_state = "PLAYING" 
        self.status_text = "SUHU IDEAL! Roti Memasak..."
        self.status_color = GREEN

        # Load gambar panggangan
        self.toast_images = [
            pygame.image.load("cook_1.png").convert(),  
            pygame.image.load("cook_2.png").convert(),  
            pygame.image.load("cook_3.png").convert(),  
            pygame.image.load("cook_4.png").convert()   
        ]
        self.toast_images = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in self.toast_images]

        self.bar_x = 30
        self.bar_width = 340
        self.bar_height = 20

        # Load Tombol Next & Tombol Play (Try Again)
        self.img_next_button = pygame.image.load("next.png").convert_alpha()
        self.img_next_button = pygame.transform.scale(self.img_next_button, (200, 250))
        self.next_button_rect = self.img_next_button.get_rect(topleft=(100, 430))

        self.img_play_button = pygame.image.load("start.png").convert_alpha()
        self.img_play_button = pygame.transform.scale(self.img_play_button, (200, 250))
        self.play_button_rect = self.img_play_button.get_rect(topleft=(100, 430)) 

        self.font_status = pygame.font.SysFont("Arial Black", 16, bold=True)
        self.font_test = pygame.font.SysFont("Arial Black", 14, bold=True)


    def handle_events(self, event):
        if self.game_state == "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.temp_value -= self.cool_power
                if self.temp_value < 0: self.temp_value = 0
                
        elif self.game_state == "WIN":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.next_button_rect.collidepoint(event.pos):
                    self.game_state = "GO_NEXT"
                    
        elif self.game_state == "GOSONG":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.play_button_rect.collidepoint(event.pos):
                    self.temp_value = 50
                    self.cook_progress = 0
                    self.status_text = "SUHU IDEAL! Roti Memasak..."
                    self.status_color = GREEN
                    self.game_state = "PLAYING"

    def update(self):
        if self.game_state == "PLAYING":
            self.temp_value += self.heat_speed
            if 30 <= self.temp_value <= 75:
                self.status_text = "PERFECT"
                self.status_color = GREEN
                self.cook_progress += 0.25
            elif self.temp_value < 30:
                self.status_text = "TOO COLD!"
                self.status_color = GRAY
            else:
                self.status_text = "TOO HOT!"
                self.status_color = RED

            if self.temp_value >= 100:
                self.temp_value = 100
                self.game_state = "GOSONG"
            if self.cook_progress >= self.max_cook:
                self.cook_progress = self.max_cook
                self.game_state = "WIN"
                
        elif self.game_state == "GO_NEXT":
            return "DONE"
        return "PLAYING"

    def draw(self, screen):
        if self.game_state == "GOSONG":
            screen.blit(self.toast_images[3], (0, 0)) # roti gosong
        elif self.game_state == "WIN":
            screen.blit(self.toast_images[2], (0, 0)) 
        else:
            if self.cook_progress < 50: screen.blit(self.toast_images[0], (0, 0))
            else: screen.blit(self.toast_images[1], (0, 0))

        
        if self.game_state == "PLAYING":
            pygame.draw.rect(screen, GRAY, (self.bar_x, 55, self.bar_width, self.bar_height)) 
            pygame.draw.rect(screen, GREEN, (self.bar_x, 55, int(self.cook_progress * 3.4), self.bar_height)) 
            pygame.draw.rect(screen, GRAY, (self.bar_x, 465, self.bar_width, self.bar_height)) 
            pygame.draw.rect(screen, self.status_color, (self.bar_x, 465, int(self.temp_value * 3.4), self.bar_height))
            txt_status = self.font_status.render(self.status_text, True, self.status_color)
            txt_test = self.font_test.render("PRESS SPACE TO KEEP THE HEAT", True, (80, 80, 80))
            screen.blit(txt_status, (60, 500))
            screen.blit(txt_test, (40, 100))
            
        elif self.game_state == "GOSONG":
            txt_fail = self.font_status.render("BURNT!", True, RED)
            screen.blit(txt_fail, (170, 220))
            screen.blit(self.img_play_button, self.play_button_rect.topleft)
            
        elif self.game_state == "WIN":
            screen.blit(self.img_next_button, self.next_button_rect.topleft)



class MainGameController:
    def __init__(self):
        self.current_stage = INTRO_1 

        # load gambar
        self.img_intro1 = pygame.transform.scale(pygame.image.load("intro_1.png").convert(), (400, 600))
        self.img_intro2 = pygame.transform.scale(pygame.image.load("intro_2.png").convert(), (400, 600))
        self.img_intro3 = pygame.transform.scale(pygame.image.load("intro3.png").convert(), (400, 600))
        self.img_intro4 = pygame.transform.scale(pygame.image.load("intro_4.png").convert(), (400, 600))
        self.img_menu   = pygame.transform.scale(pygame.image.load("start menu.png").convert(), (400, 600))
        
        self.img_game1  = pygame.transform.scale(pygame.image.load("game_1.png").convert(), (400, 600))
        self.img_game2  = pygame.transform.scale(pygame.image.load("game_2.png").convert(), (400, 600))
        self.img_game3  = pygame.transform.scale(pygame.image.load("game3.png").convert(), (400, 600))
        self.img_game4  = pygame.transform.scale(pygame.image.load("game_4.png").convert(), (400, 600))
        self.img_game5  = pygame.transform.scale(pygame.image.load("game_5.png").convert(), (400, 600))
        
        self.img_nutri_card = pygame.transform.scale(pygame.image.load("nutri card1.png").convert(), (400, 600))
        self.img_earth_end  = pygame.transform.scale(pygame.image.load("earth.png").convert(), (400, 600))

       #load buton
        self.img_next_button  = pygame.transform.scale(pygame.image.load("next.png").convert_alpha(), (100, 150))
        self.img_cook_button  = pygame.transform.scale(pygame.image.load("cook.png").convert_alpha(), (200, 250))
        self.img_play_button  = pygame.transform.scale(pygame.image.load("start.png").convert_alpha(), (300, 350)) 
        self.img_quit_button  = pygame.transform.scale(pygame.image.load("quit.png").convert_alpha(), (200, 300 ))
        self.img_start_button  = pygame.transform.scale(pygame.image.load("play.png").convert_alpha(), (200, 300))

        # Tombol Next (Intro & Story awal)
        self.next_btn_rect = self.img_next_button.get_rect(topleft=(290, 350))
        
        # Main Menu
        self.menu_start_rect = self.img_play_button.get_rect(topleft=(50, 250))
       
        # Banana French Toast yang bisa diklik
        self.fridge_french_toast_rect = pygame.Rect(200, 300, 300, 330) 
        
        # Resep: Tombol Cook 
        self.recipe_cook_rect = self.img_cook_button.get_rect(topleft=(90, 400))

        # Nutri Card
        self.nutri_next_rect = self.img_next_button.get_rect(topleft=(150, 450))

        # Earth
        self.earth_quit_rect  = self.img_quit_button.get_rect(topleft=(100, 270))
        self.earth_start_rect = self.img_start_button.get_rect(topleft=(230, 250))

        self.stage_chopping = ChoppingStage()
        self.stage_mixture  = MixtureStage()
        self.stage_toast    = ToastStage()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                
                # Intro 1 - 4
                if self.current_stage in [INTRO_1, INTRO_2, INTRO_3, INTRO_4]:
                    if self.next_btn_rect.collidepoint(pos):
                        if self.current_stage == INTRO_1: self.current_stage = INTRO_2
                        elif self.current_stage == INTRO_2: self.current_stage = INTRO_3
                        elif self.current_stage == INTRO_3: self.current_stage = INTRO_4
                        elif self.current_stage == INTRO_4: self.current_stage = MAIN_MENU

                # Main Menu
                elif self.current_stage == MAIN_MENU:
                    if self.menu_start_rect.collidepoint(pos):
                        self.current_stage = GAME_1
             
                # Game 1 - 3
                elif self.current_stage in [GAME_1, GAME_2, GAME_3]:
                    if self.next_btn_rect.collidepoint(pos):
                        if self.current_stage == GAME_1: self.current_stage = GAME_2
                        elif self.current_stage == GAME_2: self.current_stage = GAME_3
                        elif self.current_stage == GAME_3: self.current_stage = GAME_4

                # Game 4 (Isi Kulkas)
                elif self.current_stage == GAME_4:
                    if self.fridge_french_toast_rect.collidepoint(pos):
                        self.current_stage = GAME_5

                # Game 5 (Resep)
                elif self.current_stage == GAME_5:
                    if self.recipe_cook_rect.collidepoint(pos):
                        self.stage_chopping = ChoppingStage()
                        self.current_stage = CHOPPING

                # Nutri Card
                elif self.current_stage == NUTRI_CARD:
                    if self.nutri_next_rect.collidepoint(pos):
                        self.current_stage = EARTH_END

                # Earth End
                elif self.current_stage == EARTH_END:
                    if self.earth_start_rect.collidepoint(pos):
                        self.current_stage = GAME_4 
                    elif self.earth_quit_rect.collidepoint(pos):
                        pygame.quit()
                        sys.exit()

            # event game masak
            if self.current_stage == CHOPPING:
                self.stage_chopping.handle_events(event)
            elif self.current_stage == MIXTURE:
                self.stage_mixture.handle_events(event)
            elif self.current_stage == TOAST:
                self.stage_toast.handle_events(event)

    def update(self):
        if self.current_stage == CHOPPING:
            if self.stage_chopping.update() == "DONE":
                self.stage_mixture = MixtureStage()
                self.current_stage = MIXTURE 
        elif self.current_stage == MIXTURE:
            if self.stage_mixture.update() == "DONE":
                self.stage_toast = ToastStage()
                self.current_stage = TOAST 
        elif self.current_stage == TOAST:
            if self.stage_toast.update() == "DONE":
                self.current_stage = NUTRI_CARD

    def draw(self):
        if self.current_stage == INTRO_1:
            screen.blit(self.img_intro1, (0, 0))
            screen.blit(self.img_next_button, self.next_btn_rect.topleft)
        elif self.current_stage == INTRO_2:
            screen.blit(self.img_intro2, (0, 0))
            screen.blit(self.img_next_button, self.next_btn_rect.topleft)
        elif self.current_stage == INTRO_3:
            screen.blit(self.img_intro3, (0, 0))
            screen.blit(self.img_next_button, self.next_btn_rect.topleft)
        elif self.current_stage == INTRO_4:
            screen.blit(self.img_intro4, (0, 0))
            screen.blit(self.img_next_button, self.next_btn_rect.topleft)
            
        elif self.current_stage == MAIN_MENU:
            screen.blit(self.img_menu, (0, 0))
            screen.blit(self.img_play_button, self.menu_start_rect.topleft)
          

        elif self.current_stage == GAME_1:
            screen.blit(self.img_game1, (0, 0))
            screen.blit(self.img_next_button, self.next_btn_rect.topleft)
        elif self.current_stage == GAME_2:
            screen.blit(self.img_game2, (0, 0))
            screen.blit(self.img_next_button, self.next_btn_rect.topleft)
        elif self.current_stage == GAME_3:
            screen.blit(self.img_game3, (0, 0))
            screen.blit(self.img_next_button, self.next_btn_rect.topleft)
            
        elif self.current_stage == GAME_4:
            screen.blit(self.img_game4, (0, 0))
            
        elif self.current_stage == GAME_5:
            screen.blit(self.img_game5, (0, 0))
            screen.blit(self.img_cook_button, self.recipe_cook_rect.topleft)

        elif self.current_stage == CHOPPING:
            self.stage_chopping.draw(screen)
        elif self.current_stage == MIXTURE:
            self.stage_mixture.draw(screen)
        elif self.current_stage == TOAST:
            self.stage_toast.draw(screen)
            
        elif self.current_stage == NUTRI_CARD:
            screen.blit(self.img_nutri_card, (0, 0))
            screen.blit(self.img_next_button, self.nutri_next_rect.topleft)
            
        elif self.current_stage == EARTH_END:
            screen.blit(self.img_earth_end, (0, 0))
            screen.blit(self.img_quit_button, self.earth_quit_rect.topleft)
            screen.blit(self.img_start_button, self.earth_start_rect.topleft)

        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

if __name__ == "__main__":
    game = MainGameController()
    game.run()