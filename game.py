import pygame
import sys
from clouds import CloudManager

# --- INITIAL SETTINGS ---
pygame.init()
Width, Height = 1024, 600
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Whiskered Chase")
clock = pygame.time.Clock()

#HELPER FUNCTIONS

def load_cat_image (path, scale=None, alpha=True):
    img = pygame.image.load(path) #kinukuha ang image gamit ang path
    img = img.convert_alpha() if alpha else img.convert() #I-ooptimize ang image para mabilis i-render ng Pygame

    if scale:
        #kung gaano kalaki yung image para mas magandang tignan sa screen
        img = pygame.transform.smoothscale(img, scale)
    return img

# Assets loading
cloud_system = CloudManager(6, Width, Height)


# Binigyan ng scale na (500, 600) para sakto ang laki sa screen
cat_image = load_cat_image("Assets/cat.png", (500, 600)) 

#nagload ng background surface. sa "alpha=flase", kasi solid yung background at hindi na kailangan ng transparency
bg_image = load_cat_image("Assets/background_surface.png", (Width, Height), alpha=False)

title_img = load_cat_image("Assets/title.png", (650, 300)) #ito yung mag pop sa start
title_logo = load_cat_image("Assets/title.png", (450, 200)) # ito naman yung sa taas ng input name

#ito yung sa continue button    
btn_original = load_cat_image("Assets/continue_button.png")
#Gagawa ng version ng button para sa Title Screen (150x80). May 'if' check para hindi mag-crash ang game kung sakaling nawawala ang image file.
btn_idle = pygame.transform.smoothscale(btn_original, (150, 80)) if btn_original else None
#Gagawa ng mas maliit na version ng button (120x60) para sa Name Input screen.
btn_small = pygame.transform.smoothscale(btn_original, (120, 60)) if btn_original else None

# Ito ang gagamiting font para sa pangalan ng player
pixel_font = pygame.font.SysFont("Consolas", 40, bold=True) 

#Pangalawang font style pero mas maliit (size 24) para sa mga labels o instructions.
label_font = pygame.font.SysFont("Consolas", 24, bold=True)

# GAME STATE VARIABLES
current_state = 'TITLE' #dito sinasabi kung anong screen ang unang dapat makita
player_name = "" #name ng player
title_alpha = 0 #ito yung fade in effect ng title. Nagsisimula sa 0 (invisible) at unti-unting tataas hanggang 255 (full color).
fade_alpha = 0 #Ginagamit ito para sa "Fade-out" effect kapag lilipat na ng scene.
start_ticks = pygame.time.get_ticks() # Ginagamit ito para malaman kung ilang segundo na ang nakalipas mula nung binuksan ang app.

# Ito ang gagamiting "overlay" para sa fade effects.
fade_surface = pygame.Surface((Width, Height)) 
fade_surface.fill("White")


# MAIN LOOP
while True:
    current_time = pygame.time.get_ticks() #Kinukuha nito ang kabuuang oras (sa milliseconds) mula nung nag-start ang pygame.init().
    mouse_pos = pygame.mouse.get_pos() #Kinukuha nito ang kasalukuyang (x, y) coordinates ng mouse pointer sa loob ng window.
    seconds_passed = (current_time - start_ticks) / 1000 #Kinakalkula nito kung ilang segundo na ang nakalipas simula nung nakuha ang 'start_ticks'.

    #para makapag quit sa game pag clinick ang X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Sinisiguro muna na nasa 'TITLE' screen tayo at nakalipas na ang 5 seconds.
        if current_state == 'TITLE' and seconds_passed >= 5: 
            if btn_idle: #tinitingnan kung nalo-load ba nang tama ang button image.
                btn_rect = btn_idle.get_rect(center=(Width // 2, Height // 2 + 110)) #Gumagawa ng invisible na box (Rect) sa paligid ng button.
            # Dito tinitingnan kung may ginawa ang player:
            # A. Pinindot ba ang 'ENTER' sa keyboard? (K_RETURN)
            # B. O clinick ba ang mouse (MOUSEBUTTONDOWN) habang ang cursor ay nasa loob ng button (collidepoint)?
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or \
                   (event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(event.pos)):
                    current_state = 'FADING_OUT' # Kapag totoo ang isa sa itaas, babaguhin ang state ng laro. Titigil na ang Title Screen at magsisimula na ang 'FADING_OUT'.
        
        elif current_state == 'NAME_INPUT': #Tinitingnan kung ang laro ay nasa 'NAME_INPUT' state na. Ibig sabihin, tapos na ang title screen at fade effect.
            if event.type == pygame.KEYDOWN: #Inaabangan kung may pinindot na key sa keyboard ang player.
                # Kung ang pinindot ay 'BACKSPACE', buburahin ang huling letter.
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                #Dito tinitingnan kung pwede pang magdagdag ng letra. 15 letters lang
                elif len(player_name) < 15 and (event.unicode.isalnum() or event.unicode == " "):
                    player_name += event.unicode
                #Kung pinindot ang 'ENTER' (K_RETURN) at HINDI empty ang pangalan.
                elif event.key == pygame.K_RETURN and player_name.strip():
                    print(f"Starting game for: {player_name}") #print muna kasi wala pa yung laro.
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_btn_rect = btn_small.get_rect(center=(Width - 220, Height // 2 + 190))
                if input_btn_rect.collidepoint(event.pos) and player_name.strip():
                    print(f"Button Clicked! Starting: {player_name}")

    screen.fill("Sky Blue") # Pinipintahan ang buong screen ng sky blue.
    if bg_image: screen.blit(bg_image, (0, 0)) # I-draw ang background image kung meron.
    cloud_system.update_and_draw(screen) # Pinapagalaw at pinapakita ang mga ulap.

# Chine-check kung ang laro ay nasa Title Screen o kasalukuyang nag-a-alis (fading out)
    if current_state in ['TITLE', 'FADING_OUT']:
        if title_img and seconds_passed >= 5: # Dito sinasabi: "Wait lang ng 5 seconds bago natin ipakita ang logo."
            title_alpha = min(255, title_alpha + 4) # Ito ang nagpapa-fade in: "Dagdagan mo ng konting linaw 'yung logo bawat segundo."
            title_img.set_alpha(title_alpha) # Dito natin ina-apply: "Isuot mo na itong bagong linaw (alpha) sa logo."
            t_rect = title_img.get_rect(center=(Width // 2, Height // 2 - 80)) # pwesto ng logo
            screen.blit(title_img, t_rect) #dito na ilalagay ang logo sa screen sa pwesto na nilagay
            
            btn_rect = btn_idle.get_rect(center=(Width // 2, Height // 2 + 110)) # Ito ang pwesto ng button "Maglagay tayo ng box para sa button sa baba lang ng logo."
            draw_btn = btn_idle
            # Dito titingnan ang mouse: "Nakatapat ba ang cursor sa button? At hindi pa ba tayo nag-e-exit?"
            if btn_rect.collidepoint(mouse_pos) and current_state != 'FADING_OUT':
                # Ito ang 'hover' effect: "Lalakihan natin ng konti ang button para malaman ng player na clickable ito."
                draw_btn = pygame.transform.smoothscale(btn_original, (165, 88))
                # Dito ina-adjust ang sukat: "Siguraduhin mong nasa gitna pa rin ang malaking button."
                btn_rect = draw_btn.get_rect(center=(Width // 2, Height // 2 + 110))
            
            # Dito sinasabay ang button: "Kung gaano kalinaw ang logo, dapat ganoon din ang button."
            draw_btn.set_alpha(title_alpha)
            # Dito ididikit ang button
            screen.blit(draw_btn, btn_rect)

# Dito ang transition: "Kung pinindot na ang button at papaalis na tayo sa scene..."
        if current_state == 'FADING_OUT': 
            fade_alpha = min(255, fade_alpha + 5) #ito yung white fade out
            fade_surface.set_alpha(int(fade_alpha)) # Dito natin gagamitin: "Gawin mong mas malabo ang screen gamit itong puting surface."
            screen.blit(fade_surface, (0, 0))
            if fade_alpha >= 255: current_state = 'NAME_INPUT'

    # SCENE: NAME INPUT
    elif current_state == 'NAME_INPUT': # Dito natin sinasabi: "Kung tapos na ang Title at nasa Name Input na tayo..."
        if fade_alpha > 0: # Ito ang 'Fade-In' effect:
            fade_alpha = max(0, fade_alpha - 7) # Binabawasan ang kapal ng puti
            fade_surface.set_alpha(int(fade_alpha))
        
        # Cat imgae
        if cat_image:
            #pwesto ng pusa
            cat_rect = cat_image.get_rect(bottomleft=(-50, Height + 50))
            screen.blit(cat_image, cat_rect)
        
        # UI Box logic
        ui_center_x = Width - 220
        box_rect = pygame.Rect(0, 0, 360, 130)
        box_rect.center = (ui_center_x, Height // 2 + 60)
        
        #ito yung logo
        if title_logo:
            l_rect = title_logo.get_rect(center=(ui_center_x, box_rect.top - 100))
            screen.blit(title_logo, l_rect)

        # Dito sa background ng box: "Gumawa tayo ng medyo transparent na itim na rectangle."
        box_bg = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(box_bg, (0, 0, 0, 130), box_bg.get_rect(), border_radius=12)
        screen.blit(box_bg, box_rect.topleft)# Dito ididikit 'yung itim na background
        pygame.draw.rect(screen, "yellow", box_rect, 2, border_radius=12) #color border ng box background

        #ito yung sa input name shaka yung color ng text
        name_label = label_font.render("ENTER YOUR NAME", True, "Yellow") 
        screen.blit(name_label, (box_rect.left + 15, box_rect.top + 12))
        
        # Ito ang pangalan: "Dito natin iguguhit 'yung tina-type na pangalan ng player."
        name_surf = pixel_font.render(player_name, True, "Orange")
        name_rect = name_surf.get_rect(center=(box_rect.centerx, box_rect.top + 80))
        screen.blit(name_surf, name_rect)

        #initingnan kung matagumpay na na-load ang 'btn_small' image.
        if btn_small:
            btn_input_rect = btn_small.get_rect(center=(ui_center_x, box_rect.bottom + 50)) #Gumagawa ng rectangle (box) para sa button.
            final_btn = btn_small #'final_btn' bilang yung maliit na button (btn_small).
            #Tinitingnan kung ang mouse_pos (cursor) ay nasa loob ng button box
            if btn_input_rect.collidepoint(mouse_pos):
                final_btn = pygame.transform.smoothscale(btn_original, (130, 70)) #Kapag naka-hover ang mouse, lalakihan natin ng konti ang button (130x70).
                btn_input_rect = final_btn.get_rect(center=btn_input_rect.center) #Dahil nagbago ang laki, kailangang kunin ulit ang 'rect' nito.
            screen.blit(final_btn, btn_input_rect) #I-papakita na sa screen ang tamang version ng button (idle o hover).

# Ginagamit ang math para gumawa ng 'blinking' effect.
# Ang ticks ay hinahati sa 400ms. Ang '% 2' ay nagbibigay lang ng sagot na 0 o 1.
# Kapag 1 (True), ipapakita ang cursor. Kapag 0 (False), itatago ito.
        if (pygame.time.get_ticks() // 400) % 2:
            #Ginagawa ang image ng cursor gamit ang pixel_font.
            cursor = pixel_font.render("_", True, "White") 
            cx = name_rect.right + 2 if player_name else box_rect.centerx - 8 # Kung may nasulat nang pangalan, ilalagay ang cursor sa dulo ng text (name_rect.right).
            screen.blit(cursor, (cx, name_rect.top)) # I-draw ang cursor sa screen gamit ang nakuha nating 'cx' at 'y' position.

        #Kung ang fade_alpha ay higit sa 0, ibig sabihin may "opacity" pa ang fade surface.  
        if fade_alpha > 0:
            screen.blit(fade_surface, (0, 0)) #I-draw ang fade_surface (puting rectangle) sa ibabaw ng lahat.

    pygame.display.flip()
    clock.tick(60)