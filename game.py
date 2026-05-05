import pygame # Import ang main library para sa game development.
import sys # Gagamitin para sa pag-exit ng system or program.
import random # Para sa random numbers, tulad ng pag-spawn ng daga.
import time # Para sa functions na may kinalaman sa oras.
from clouds import CloudManager # Import ng custom module para sa ulap.
from sprite_entity import SpriteEntity, FLOORS_Y, HOUSE_LIMITS # Import ng custom logic para sa characters at floor positions.

""" 1. INITIALIZATION & SCREEN SETUP
Dito sinisimulan ang makina ng laro."""

pygame.init() # Initialize lahat ng modules ng Pygame. (new: Sinimulan ang engine)
width= 1024 # Lapad ng game window.
height = 600 # Taas ng game window.
screen = pygame.display.set_mode((width, height)) # Gawa ng main game window base sa width at height.
pygame.display.set_caption("Whiskered Chase") # Title na makikita sa taas ng window.
clock = pygame.time.Clock() # Tool para ma-control kung gaano kabilis ang game (FPS).

""" 2. Image Loading Helper """
def load_cat_image (path, scale=None, alpha=True): # Helper function para sa pag-load ng images.
        img = pygame.image.load(path) # I-load ang image file mula sa folder path.
        img = img.convert_alpha() if alpha else img.convert() # I-convert para mas mabilis i-render (alpha = transparent).
        if scale: # Kung may ibinigay na size, i-resize ang image.
            img = pygame.transform.smoothscale(img, scale)
        return img # Ibalik ang ready-to-use image.

cloud_system = CloudManager(6, width, height) # Gawa ng manager para sa 6 na gumagalaw na ulap.

# Characters (Cat and Rat)
cat_idle_img = load_cat_image("Assets/cat_idle.png", (80, 60)) # Image ng pusa kapag nakatigil lang.
cat_run = [load_cat_image("Assets/cat_run1.png", (80, 60)), load_cat_image("Assets/cat_run2.png", (80, 60))] # List ng images para sa animation ng pagtakbo ng pusa.
rat_run = [load_cat_image("Assets/rat_run1.png", (40, 30)), load_cat_image("Assets/rat_run2.png", (40, 30))] # List ng images para sa animation ng daga.

# Backgrounds at Buttons
house_img = load_cat_image("Assets/house.png", (width, height)) # Background ng loob ng bahay.
ui_bg = load_cat_image("Assets/background_game.png", (220, 60)) # Background para sa Score at Timer UI.

win_screen_img = load_cat_image("Assets/win.png", (700, 500)) # Image na lalabas kapag nanalo.
lose_screen_img = load_cat_image("Assets/lose.png", (700, 500)) # Image na lalabas kapag natalo.
play_again_btn_img = load_cat_image("Assets/play_again_button.png", (150, 80)) # Button para umulit ng laro.
quit_btn_img = load_cat_image("Assets/quit_button.png", (150, 80)) # Button para lumabas sa game.

cat_image = load_cat_image("Assets/cat.png", (500, 600)) # Malaking image ng pusa para sa title/menu screen.
bg_image = load_cat_image("Assets/background_surface.png", (width, height), alpha=False) # Background image para sa menu.
title_img = load_cat_image("Assets/title.png", (650, 300)) # Main logo ng game.
title_logo = load_cat_image("Assets/title.png", (450, 200)) # Mas maliit na logo para sa name input screen.

btn_original = load_cat_image("Assets/continue_button.png") # Original na kopya ng continue button.
btn_idle = pygame.transform.smoothscale(btn_original, (150, 80)) if btn_original else None # Normal size ng button.
btn_small = pygame.transform.smoothscale(btn_original, (120, 60)) if btn_original else None # Maliit na size ng button para sa ibang screen.

play_btn_original = load_cat_image("Assets/play_button.png") # Original play button image.
play_btn_idle = pygame.transform.smoothscale(play_btn_original, (320, 200)) if play_btn_original else None # Size ng play button sa main menu.

# Fonts
pixel_font = pygame.font.SysFont("Consolas", 40, bold=True) # Font para sa pangalan ng player.
label_font = pygame.font.SysFont("Consolas", 24, bold=True) # Maliit na font para sa UI labels.
welcome_font = pygame.font.SysFont("Consolas", 40, bold=True) # Font para sa welcome message.

""" 3. GAME STATES & VARIABLES
Ang logic ng progression ng laro. """
current_state = 'TITLE' # Variable para malaman kung anong screen ang dapat ipakita (Title, Game, etc.).
player_name = "" # Dito ise-save ang tinype na pangalan ng user.
title_alpha = 0 # Para sa fade-in effect ng title logo.
fade_alpha = 0 # Para sa transition effect (puting screen na nag-fa-fade).
start_ticks = pygame.time.get_ticks() # Simula ng timer mula nung binuksan ang game.

score = 0 # Points ng player.
game_timer = 120 # Total time na 120 seconds (2 minutes).
start_game_ticks = 0 # Timer para sa actual gameplay.

fade_surface = pygame.Surface((width, height)) # Isang extra layer para sa fading effects.
fade_surface.fill("White") # Gawing puti ang transition layer.

#Sprite Creation
cat = SpriteEntity(cat_run, cat_idle_img) # Gawa ng 'cat' object gamit ang SpriteEntity class.
rats = [] # Empty list kung saan ilalagay ang mga daga.

def spawn_rat(): # Function para gumawa ng bagong daga sa random na pwesto.
    r = SpriteEntity(rat_run, None, False) # Instance ng daga.
    r.floor = random.randint(0, 3) # Random floor kung saan lalabas ang daga (0-3 floors).
    r.pos = pygame.Vector2(random.randint(HOUSE_LIMITS[0], 800), FLOORS_Y[r.floor]) # Random position sa X-axis at Y-axis base sa floor.
    return r # Ibalik ang bagong dagang ginawa.

def init_rats(): # Function para simulan ang list ng mga daga.
    global rats # Gamitin ang global rats list.
    rats = [] # I-clear muna ang list.
    for i in range(3): rats.append(spawn_rat()) # Mag-spawn ng tatlong daga sa simula.

init_rats() # Tawagin ang function para i-setup ang mga daga.

""" 4. MAIN GAME LOOP
Dito umiikot ang buong takbo ng program."""
while True: # Main Game Loop - dito tumatakbo ang laro nang paulit-ulit.
    
    current_time = pygame.time.get_ticks() # Kunin ang current time sa bawat frame.
    mouse_pos = pygame.mouse.get_pos() # Kunin ang pwesto ng mouse cursor.
    seconds_passed = (current_time - start_ticks) / 1000 # Kalkulahin kung ilang segundo na ang nakalipas mula nung nag-start.

     # EVENT HANDLING BLOCK (Ang "Tenga" ng laro) Dito pinoproseso lahat ng aksyon na galing sa iyo (Player).
    for event in pygame.event.get(): # Check ang bawat user input (pindot sa keyboard/mouse).
        if event.type == pygame.QUIT: # Kapag clinick ang 'X' sa window.
            pygame.quit() # Isara ang pygame.
            sys.exit() # Patayin ang program.
        

        # TITLE STATE LOGIC
        # Kung nasa Title screen, tinitignan natin kung 5 seconds na ang nakalipas at kung pinindot ba ang 'Enter' o clinick ang 'Start' button.
        if current_state == 'TITLE' and seconds_passed >= 5: # Kapag nasa Title screen at lumampas na ng 5 seconds.
            if btn_idle: 
                btn_rect = btn_idle.get_rect(center=(512, 410)) # I-set ang pwesto ng button.
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or \
                   (event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(event.pos)): # Kapag pinindot ang Enter o clinick ang button.
                    current_state = 'FADING_OUT' # Mag-proceed sa susunod na screen.
        
        # NAME INPUT STATE LOGIC
        # Dito natin binabasa ang bawat titik na itini-type mo.
        elif current_state == 'NAME_INPUT': # Kapag screen na ng pag-type ng pangalan.
            if event.type == pygame.KEYDOWN: # Kung may pinindot sa keyboard.
                if event.key == pygame.K_BACKSPACE: # Burahin ang huling letter.
                    player_name = player_name[:-1]
                elif len(player_name) < 15 and (event.unicode.isalnum() or event.unicode == " "): # Magdagdag ng letter (limit 15 chars).
                    player_name += event.unicode
                elif event.key == pygame.K_RETURN and player_name.strip(): # Kapag pinindot ang Enter at may pangalan na.
                    current_state = 'PLAY_FRAME' 
            
            # Check kung clinick ang 'Continue' button gamit ang mouse.
            if event.type == pygame.MOUSEBUTTONDOWN: # Kapag clinick ang mouse.
                input_btn_rect = btn_small.get_rect(center=(292, 490)) # Check kung sa button clinick.
                if input_btn_rect.collidepoint(event.pos) and player_name.strip():
                    current_state = 'PLAY_FRAME' 

        # PLAY FRAME (WELCOME SCREEN)
        # Isang huling click sa 'Play' button bago magsimula ang chase.
        elif current_state == 'PLAY_FRAME': # Screen bago magsimula ang actual chase.
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_rect = play_btn_idle.get_rect(center=(734, 380))
                if play_rect.collidepoint(event.pos): # Kapag clinick ang Play button.
                    current_state = 'GAME_PLAY' # Simulan na ang laro.
                    start_game_ticks = pygame.time.get_ticks() # Simulan ang countdown ng game timer.

        # ACTUAL GAMEPLAY CONTROLS 
        # Habang naghahabulan, dito nakikinig ang computer kung itataas o ibababa mo ang pusa sa ibang floors.
        elif current_state == 'GAME_PLAY': # Screen habang naglalaro.
            if event.type == pygame.KEYDOWN: # Kapag pinindot ang Up o Down.
                if event.key == pygame.K_UP: cat.move(0, -1) # Tumaas ng floor.
                if event.key == pygame.K_DOWN: cat.move(0, 1) # Bumaba ng floor.

        # --- END SCREEN (WIN/LOSE) ---
        # Kapag tapos na ang laro, dito natin hinihintay kung gusto mo bang mag-ulit (Play Again) o bumalik sa simula (Quit).
        elif current_state in ['WIN', 'GAMEOVER']: # Kapag tapos na ang laro.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Gumagawa tayo ng 'invisible box' (Rect) sa paligid ng popup para malaman kung saan banda sa screen ang pinindot mo.
                if current_state == 'WIN': # Set position ng win popup.
                    popup_rect = win_screen_img.get_rect(center=(512, 300))
                else: # Set position ng lose popup.
                    popup_rect = lose_screen_img.get_rect(center=(512, 300))
                
                again_rect = play_again_btn_img.get_rect(bottomleft=(popup_rect.left + 100, popup_rect.bottom - 80)) # Pwesto ng Play Again.
                quit_rect = quit_btn_img.get_rect(bottomright=(popup_rect.right - 100, popup_rect.bottom - 80)) # Pwesto ng Quit.
                
                if again_rect.collidepoint(event.pos): # Kung pinindot ang Play Again.
                    # I-re-reset lahat ng values sa zero para back to start.
                    score = 0 # Reset ang score.
                    start_game_ticks = pygame.time.get_ticks() # Reset ang timer.
                    current_state = 'GAME_PLAY' # Balik sa game.
                    cat.reset() # Reset pwesto ng pusa.
                    init_rats() # Reset mga daga.
                
                elif quit_rect.collidepoint(event.pos): # Kung pinindot ang Quit.
                    score = 0
                    current_state = 'PLAY_FRAME' # Balik sa Welcome screen.
                    cat.reset()
                    init_rats()
                    
    """5. GAMEPLAY LOGIC BLOCK
       Dito tumatakbo ang main mechanics: movement, AI, at scoring."""
    if current_state == 'GAME_PLAY': # Logics sa loob ng gameplay.
        screen.blit(house_img, (0,0)) # I-draw ang background ng bahay.
        
        # TIMER CALCULATION
        # Kinukuha ang difference ng oras ngayon at nung nagsimula ang game. Ginagamit ang // 1000 para maging "whole seconds" ang bilang.
        total_seconds_left = max(0, game_timer - (current_time - start_game_ticks) // 1000) # Kalkulahin ang natitirang oras.
        minutes = total_seconds_left // 60 # Kunin ang minutes.
        seconds = total_seconds_left % 60 # Kunin ang seconds.
        timer_string = f"TIME: {minutes:02}:{seconds:02}" # Format ng timer text.
        
        # SMOOTH HORIZONTAL MOVEMENT
        # Kakaiba ito sa 'event' loop kanina. Ang 'get_pressed' ay tinitignan kung NAKADIIN pa rin ang key, kaya tuloy-tuloy ang takbo ng pusa.
        keys = pygame.key.get_pressed() # Check kung anong key ang nakadiin (held down).
        dx = 0
        if keys[pygame.K_LEFT]: dx = -7 # Move left kapag nakadiin ang Left arrow.
        if keys[pygame.K_RIGHT]: dx = 7 # Move right kapag nakadiin ang Right arrow.
        cat.move(dx, 0) # I-apply ang movement sa pusa.
        
        # RAT AI & INTERACTION
        # Dito natin binibigyan ng "isip" ang bawat daga sa listahan.
        for r in rats[:]: # I-loop ang bawat daga.
            # Distance check. 'abs' (absolute) ang ginagamit para distansya lang ang makuha, 
            # walang pakialam kung nasa negative o positive side ang daga.
            distance = r.pos.x - cat.pos.x # Check distansya ng pusa at daga.

            # "Panic Logic" - Kung nasa parehong floor at malapit ang pusa (200 pixels),
            # magpapalit ng direksyon ang daga para tumakbo palayo.
            if r.floor == cat.floor and abs(distance) < 200: # Kung magkapantay ng floor at malapit ang pusa.
                r.dir = 1 if distance > 0 else -1 # Mag-set ng direksyon para lumayo sa pusa.
                r.move(r.dir * 6) # Takbo ng mabilis palayo.
            else:
                r.move(r.dir * 3) # Normal na lakad lang.

                
            r.draw(screen) # I-display ang daga sa screen.
            
            # COLLISION DETECTION (ANG HULI)
            # Gumagawa tayo ng pansamantalang boxes para tignan kung nag-overlap sila.
            cat_rect = pygame.Rect(cat.pos.x, cat.pos.y-60, 80, 60) # Rectangle ng pusa para sa collision.
            rat_rect = pygame.Rect(r.pos.x, r.pos.y-30, 40, 30) # Rectangle ng daga para sa collision.
            if cat_rect.colliderect(rat_rect): # Kapag nagpang-abot ang pusa at daga.
                rats.remove(r) # Tanggalin ang daga.
                score += 1 # Dagdag 1 point.
                if score < 23: rats.append(spawn_rat()) # Mag-spawn uli hanggang hindi pa 23 ang score.
        
        cat.draw(screen) # I-display ang pusa.

        if ui_bg: # Draw ang UI backgrounds para sa Score at Timer.
            screen.blit(ui_bg, (10, 10)) # Score background.
            screen.blit(ui_bg, (795, 10)) # Timer background.
        
        # I-convert ang text into an image (render) para ma-display.
        score_text = label_font.render(f"SCORE: {score}/25", False, "Yellow") # Render ng score text.
        timer_text = label_font.render(timer_string, False, "Yellow") # Render ng timer text.
        screen.blit(score_text, (45, 30)) # Display sa screen.
        screen.blit(timer_text, (835, 30)) # Display sa screen.

        if score >= 25: current_state = 'WIN' # Kapag naka-25 points, win!
        elif total_seconds_left <= 0: current_state = 'GAMEOVER' # Kapag ubos na ang oras, game over.

        """ 6. RESULT SCREEN RENDERING (WIN/GAMEOVER)
        Dito ipapakita ang final popup at buttons pagkatapos ng laro."""
    elif current_state in ['WIN', 'GAMEOVER']: # Rendering para sa win/loss screens.

        # DARK OVERLAY 
        # Gumagawa ng semi-transparent black layer para mag-pop up yung result.
        screen.blit(house_img, (0, 0)) 
        overlay = pygame.Surface((width, height)) # Gawa ng madilim na layer.
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150) # Gawing semi-transparent.
        screen.blit(overlay, (0, 0))
        
        # Piliin ang tamang image (Win o Lose) base sa state.
        popup_img = win_screen_img if current_state == 'WIN' else lose_screen_img # Piliin kung win o lose image ang gagamitin.
        
        # RESULT POPUP & BUTTON ALIGNMENT
        # Dito natin inaayos ang itsura ng final screen.
        if popup_img:
            # nInilalagay natin ang 'Win' o 'Lose' image sa eksaktong gitna.
            # Ang center=(512, 300) ay ang middle point ng iyong 1024x600 screen.
            popup_rect = popup_img.get_rect(center=(512, 300)) # Pwesto sa gitna.
            screen.blit(popup_img, popup_rect)
            
            # BUTTON LOGIC 
            # Sinisigurado muna natin na na-load ang images ng buttons para hindi mag-crash.
            if play_again_btn_img and quit_btn_img:
                # DYNAMIC POSITIONING.
                # Imbes na hulaan ang pixels, ginagamit natin ang edges ng 'popup_rect'.
                # again_pos = 100 pixels mula sa kaliwang gilid ng popup.
                # quit_pos = 100 pixels mula sa kanang gilid ng popup.
                again_pos = (popup_rect.left + 100, popup_rect.bottom - 80)
                quit_pos = (popup_rect.right - 100, popup_rect.bottom - 80)
                
                # PLAY AGAIN BUTTON & HOVER EFFECT 
                # 'bottomleft' ang ginagamit nating anchor para lapat sa baba ng popup.
                again_rect = play_again_btn_img.get_rect(bottomleft=again_pos)
                draw_again_btn = play_again_btn_img

                # INTERACTIVE HOVER.
                # Kapag ang 'mouse_pos' ay nasa loob ng 'again_rect', lalakihan natin ang button.
                if again_rect.collidepoint(mouse_pos): # Hover effect: lumalaki yung button pag tinapatan ng mouse.
                    draw_again_btn = pygame.transform.smoothscale(play_again_btn_img, (165, 88))
                    again_rect = draw_again_btn.get_rect(center=again_rect.center)
                
                # QUIT BUTTON & HOVER EFFECT 
                # 'bottomright' naman ang anchor dito para sa kabilang side.
                quit_rect = quit_btn_img.get_rect(bottomright=quit_pos)
                draw_quit_btn = quit_btn_img
                # new: Katulad ng sa Play Again, lalakihan din ang Quit button pag tinapatan.
                if quit_rect.collidepoint(mouse_pos): # Hover effect para sa quit button.
                    draw_quit_btn = pygame.transform.smoothscale(quit_btn_img, (165, 88))
                    quit_rect = draw_quit_btn.get_rect(center=quit_rect.center)
                
                # FINAL RENDERING
                # I-blit (i-draw) na ang mga buttons gamit ang kanilang updated na Rect.
                screen.blit(draw_again_btn, again_rect) # Draw ang Play Again button.
                screen.blit(draw_quit_btn, quit_rect) # Draw ang Quit button.


        """ 7. TITLE & FADE-OUT LOGIC
          Dito pinapatakbo ang main menu at ang transition papuntang Name Input."""
    elif current_state in ['TITLE', 'FADING_OUT']: # Rendering para sa starting screens.
        screen.fill("Sky Blue") # Background color habang wala pang image.

        if bg_image: screen.blit(bg_image, (0, 0)) # Draw ang menu background.
        cloud_system.update_and_draw(screen) # Galawin at i-draw ang mga ulap.

        # 'seconds_passed >= 5' - Binibigyan natin ng 5 segundong intro ang player 
        # bago ipakita ang pangalan ng laro (Title) para maging cinematic ang dating.
        if title_img and seconds_passed >= 5: # Ipakita ang logo pagkatapos ng 5 seconds.
            title_alpha = min(255, title_alpha + 4) # Dahan-dahang paglitaw (fade-in).
            title_img.set_alpha(title_alpha) 
            t_rect = title_img.get_rect(center=(width // 2, height // 2 - 80)) 
            screen.blit(title_img, t_rect) 
            btn_rect = btn_idle.get_rect(center=(width // 2, height // 2 + 110)) 
            draw_btn = btn_idle

        # HOVER CHECK - Kung ang mouse ay nakatapat sa button (collidepoint),
         # papalitan natin ang 'draw_btn' ng mas malaking version (smoothscale).
            if btn_rect.collidepoint(mouse_pos) and current_state != 'FADING_OUT': # Hover effect para sa start button.
                draw_btn = pygame.transform.smoothscale(btn_original, (165, 88))
                btn_rect = draw_btn.get_rect(center=(width // 2, height // 2 + 110))
            draw_btn.set_alpha(title_alpha)
            screen.blit(draw_btn, btn_rect)

        # TRANSITION LOGIC: WHITE FADE-OUT
        # Ang block na ito ang "kurtina" na nagtatakip sa lumang screen.
        if current_state == 'FADING_OUT': # Effect kapag lilipat na ng screen.
            fade_alpha = min(255, fade_alpha + 5) 
            fade_surface.set_alpha(int(fade_alpha)) 
            screen.blit(fade_surface, (0, 0)) # I-draw ang puting layer.
            if fade_alpha >= 255: current_state = 'NAME_INPUT' # Lipat na sa name input.

        """ 8. NAME INPUT SCREEN LOGIC
            Ang block na ito ang namamahala sa pagkuha ng pangalan ng player."""
    elif current_state == 'NAME_INPUT': # Rendering ng screen para sa name input.
        screen.fill("Sky Blue")
        if bg_image: screen.blit(bg_image, (0, 0)) # Background ng langit/ulap.
        cloud_system.update_and_draw(screen)

    # REVERSE FADE - Dito naman binabawasan ang 'fade_alpha' (-7).
    # Matatandaan na galing tayo sa solid white screen. Habang bumababa ang 
    # alpha, dahan-dahang "nabubunyag" ang Name Input UI.
        if fade_alpha > 0: # Fade out ang puting layer para makita yung screen.
            fade_alpha = max(0, fade_alpha - 7) 
            fade_surface.set_alpha(int(fade_alpha))
        ui_center_x = width - 220 

        # UI LAYOUT & CAT DECORATION 
        # para hindi magmukhang bakante ang kaliwang bahagi ng screen.
        if cat_image: # Draw ang malaking pusa sa gilid.
            cat_rect = cat_image.get_rect(bottomleft=(-20, 650))
            screen.blit(cat_image, cat_rect)

        # THE INPUT BOX (ANG KAHON)
        # sa inputing ng name
        box_rect = pygame.Rect(0, 0, 360, 130) # Rectangle para sa input box.
        box_rect.center = (ui_center_x, height // 2 + 60)

        if title_logo: # Draw logo sa taas ng input box.
            l_rect = title_logo.get_rect(center=(ui_center_x, box_rect.top - 100))
            screen.blit(title_logo, l_rect)

        # SEMI-TRANSPARENT BOX BACKGROUND
        # Gumagawa tayo ng Surface na may 'SRCALPHA' para maging 
        # semi-transparent lang ang background ng box (kitang-kita pa rin ang likod).
        box_bg = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(box_bg, (0, 0, 0, 130), box_bg.get_rect(), border_radius=12) # Itim na semi-transparent background ng box.
        screen.blit(box_bg, box_rect.topleft) 

         # Border ng box (Yellow line). Ang '2' sa dulo ay ang kapal ng linya.
        pygame.draw.rect(screen, "yellow", box_rect, 2, border_radius=12) # Yellow na border ng box.

        # TYPING TEXT RENDERING 
         # Render ng instruction label.
        name_label = label_font.render("ENTER YOUR NAME", True, "Yellow") 
        screen.blit(name_label, (box_rect.left + 15, box_rect.top + 12))
        # Render ng pangalan habang itina-type ng player.
        name_surf = pixel_font.render(player_name, True, "Orange") # Pangalan na tinitype ng player.
        name_rect = name_surf.get_rect(center=(box_rect.centerx, box_rect.top + 80))
        screen.blit(name_surf, name_rect)
        
        # Interactive Continue Button Logic
        # Heto ang logic para sa button na lumalabas sa ilalim ng input box.
        if btn_small: # Continue button.
            btn_input_rect = btn_small.get_rect(center=(ui_center_x, box_rect.bottom + 50)) 
            final_btn = btn_small 

        # Kung ang mouse_pos (cursor) ay nasa loob ng button area (collidepoint),
         # palalakihin natin ang button gamit ang smoothscale para magmukhang "highlighted" o active.
            if btn_input_rect.collidepoint(mouse_pos):
                final_btn = pygame.transform.smoothscale(btn_original, (130, 70)) 
                btn_input_rect = final_btn.get_rect(center=btn_input_rect.center) 
            screen.blit(final_btn, btn_input_rect) 


        # Blinking Cursor Logic
        # Para magmukhang totoong text input, kailangan ng cursor (yung '_') na kumukurap.
        # Ginagamit ang modulo (%) sa time ticks para mag-alternate ang output (True/False).
        # Kapag ang resulta ay 1 (True), idodraw ang cursor; kapag 0, hindi ito makikita.
        if (pygame.time.get_ticks() // 400) % 2: # Kurap-kurap na cursor (yung '_').
            cursor = pixel_font.render("_", True, "White") 
            cx = name_rect.right + 2 if player_name else box_rect.centerx - 8 
            screen.blit(cursor, (cx, name_rect.top)) 

        # 5. Screen Fade Overlay
        # Ginagamit ito para sa mga smooth transitions (halimbawa, pagpapakita o pagtatago ng menu).
        if fade_alpha > 0:
            screen.blit(fade_surface, (0, 0))


        """ 9. PLAY FRAME RENDERING (WELCOME SCREEN)
        "Ready Screen" o "Lobby" ng laro"""
    elif current_state == 'PLAY_FRAME': # Rendering ng Welcome Screen bago ang chase.
        screen.blit(bg_image, (0,0)) # 1. Background Rendering
        
        # Cat Character Decoration
        # Kung may naka-load na cat_image, ipapakita ito sa screen.
        if cat_image:
            cat_rect = cat_image.get_rect(bottomleft=(-20, height + 50))
            screen.blit(cat_image, cat_rect)

        # Interactive Play Button Logic
       # Dito kinokontrol ang itsura ng Play button, kasama na ang hover effect nito.
        if play_btn_idle:
            play_pos = (734, 380)
            play_rect = play_btn_idle.get_rect(center=play_pos)
            draw_play_btn = play_btn_idle

            # Hover logic: Kapag tumama ang mouse cursor sa play_rect (collidepoint),
            # gagamit tayo ng smoothscale para palakihin ang button.
            if play_rect.collidepoint(mouse_pos): # Hover effect sa Play button.
                draw_play_btn = pygame.transform.smoothscale(play_btn_original, (340, 220))
                play_rect = draw_play_btn.get_rect(center=play_pos)
            screen.blit(draw_play_btn, play_rect)
        welcome_surf = welcome_font.render(f"PRESS PLAY, {player_name}…\nTHE HUNT IS ON.", False, "brown") # Welcome message.
        welcome_rect = welcome_surf.get_rect(center=(734, 220))
        screen.blit(welcome_surf, welcome_rect)

    pygame.display.flip() # Update ang buong display sa screen.
    clock.tick(60) # Lock ang game sa 60 frames per second (smoothness).