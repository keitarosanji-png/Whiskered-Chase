import pygame # Import ang library para sa graphics.
import random # Para sa random directions ng mga daga.

# Mga constants para sa physics at boundaries ng bahay.
FLOORS_Y = [190, 320, 455, 600] # Listahan ng Y-axis positions ng bawat floor (0 hanggang 3).
STAIRS_X = (880, 980) # Range ng X-axis kung nasaan ang hagdanan.
HOUSE_LIMITS = (35, 955) # Hangganan ng pader (kaliwa at kanan).
WALL_POSITIONS = [300, 565, 840] # Pwesto ng mga vertical walls sa loob ng bahay.
WALL_WIDTH = 40 # Kapal ng pader para sa transparency logic.

class SpriteEntity:
    # Dito nakalagay ang properties ng bawat character (pusa o daga).
    def __init__(self, run_frames, idle_frame=None, is_cat=True):
        self.run_frames = run_frames # List ng images para sa animation ng pagtakbo.
        self.idle_frame = idle_frame # Image kapag nakatigil (para sa pusa).
        self.frame_idx = 0 # Index para malaman kung anong frame ang id-draw.
        self.is_cat = is_cat # Boolean kung pusa ba ito o daga.
        self.floor = 3 # Default floor sa simula (pinakababa).
        self.pos = pygame.Vector2(100, FLOORS_Y[self.floor]) # Current (X, Y) position.
        self.flip = False # Para malaman kung dapat bang i-mirror ang image.
        self.anim_speed = 0 # Counter para sa bilis ng pagpalit ng frames.
        self.is_moving = False # Status kung gumagalaw ba ang character.
        # Random na direksyon (1 para sa kanan, -1 para sa kaliwa).
        self.dir = 1 if random.random() > 0.5 else -1

    def move(self, dx, dy=0):
        self.is_moving = False # I-reset ang status sa simula ng move function.
        
        # Stair Logic - Check kung nasa area ng hagdan para makapanhik o makababa.
        if dy != 0 and STAIRS_X[0] < self.pos.x < STAIRS_X[1]:
            if dy < 0 and self.floor > 0: self.floor -= 1 # Taas ng floor.
            if dy > 0 and self.floor < 3: self.floor += 1 # Baba ng floor.
            self.pos.y = FLOORS_Y[self.floor] # I-update ang Y position base sa floor.
            self.is_moving = True

        # Horizontal movement - Paggalaw pakaliwa o pakanan.
        new_x = self.pos.x + dx
        # Check kung hindi lalampas sa pader ng bahay.
        if HOUSE_LIMITS[0] < new_x < HOUSE_LIMITS[1]:
            if dx != 0:
                self.pos.x = new_x # I-update ang X position.
                self.is_moving = True # Sabihing gumagalaw ang sprite.
                self.flip = (dx > 0) # I-flip ang image base sa direksyon (facing right/left).
                self.animate() # Tawagin ang animation function.
        else:
            # Kung daga ito at tumama sa pader, mag-reverse ng direksyon.
            if not self.is_cat: self.dir *= -1

    def animate(self):
        # Logic para sa pagpapalit-palit ng frames (running animation).
        self.anim_speed += 1
        if self.anim_speed > 8: # Pagkatapos ng 8 ticks, palit ng frame.
            self.frame_idx = (self.frame_idx + 1) % 2 # Salitang 0 at 1.
            self.anim_speed = 0

    def draw(self, surf):
        # Triple Wall Transparency Logic - nag-a-adjust ng linaw (alpha).
        alpha = 255 # Default: solid ang kulay.
        for wall_x in WALL_POSITIONS:
            # Kung ang character ay nasa likod ng pader, gawin itong semi-transparent.
            if wall_x - WALL_WIDTH < self.pos.x < wall_x + WALL_WIDTH:
                alpha = 130 # Gawing medyo aninag.
                break 
            
        # Piliin kung anong image ang gagamitin (idle vs running).
        if not self.is_moving and self.idle_frame and self.is_cat:
            img = self.idle_frame.copy()
        else:
            img = self.run_frames[self.frame_idx].copy()

        # I-flip ang image kung kailangan (depende sa `self.flip`).
        if self.flip:
             img = pygame.transform.flip(img, True, False)
            
        img.set_alpha(alpha) # I-apply ang transparency value.
        # I-display sa screen (Y position minus height para tumapak sa sahig).
        surf.blit(img, (self.pos.x, self.pos.y - img.get_height()))

    def reset(self):
        # Ibalik ang character sa starting position kapag nag-restart ang game.
        self.floor = 3
        self.pos = pygame.Vector2(100, FLOORS_Y[self.floor])
        self.is_moving = False