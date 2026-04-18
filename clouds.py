
import pygame
import random

class Cloud:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        self.image = pygame.image.load("Assets/clouds.jpg").convert()
        self.image.set_colorkey((0, 0, 0)) 
        self.image = pygame.transform.scale(self.image, (180, 100))

        self.reset()
        
        self.x = random.randint(0, screen_w)

    def reset(self):
        #dito mag spawn yung clouds
        self.x = self.screen_w + random.randint(50, 400)
        
        # dito nililimit yung position ng clouds na sa taas lang dapat siya ng screen
        self.y = random.randint(0, int(self.screen_h * 0.4))
        
        # Randomize speed ng clouds
        self.speed = random.uniform(0.5, 2.0)

    def update(self):
        self.x -= self.speed # Binabawasan ang 'x' position ng ulap base sa bilis (speed) nito.
        if self.x < -200: #Tinitingnan kung lumabas na ba ang ulap sa kaliwang bahagi ng screen.
            self.reset() # 3. Kapag lumabas na, tatawagin ang reset() para bumalik ang ulap sa kanan.

# I-do-draw ang image ng ulap sa kasalukuyang x at y nito.
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Gagawa ito ng 'count' (halimbawa: 6) na Cloud objects.
class CloudManager:
    def __init__(self, count, screen_w, screen_h):
        self.clouds = [Cloud(screen_w, screen_h) for _ in range(count)]

# 2. Isang command na lang para sa lahat ng ulap
    def update_and_draw(self, screen):
        for cloud in self.clouds: # Gagamit ng loop para isa-isang utusan ang bawat ulap sa listahan.
            cloud.update() # Utusang gumalaw
            cloud.draw(screen) # Utusang magpakita sa screen