import pygame
import os
import subprocess
import glob
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT_SIZE = 36
PADDING = 20

def find_usb_path():
    mount_dir = "/media/pi"
    
    try:
        subdirs = [d for d in os.listdir(mount_dir) if os.path.isdir(os.path.join(mount_dir, d))]
        if subdirs:
            
            return os.path.join(mount_dir, subdirs[0])
        else:
            return None
    except FileNotFoundError:
        
        return None
    except Exception as e:
        
        print(f"Fehler beim Suchen des USB-Pfades: {e}")
        return None

def find_game_scripts(usb_path):
    
    search_pattern = os.path.join(usb_path, "*.py")
    script_paths = glob.glob(search_pattern)
    game_names = [os.path.basename(p) for p in script_paths]
    games = {name: path for name, path in zip(game_names, script_paths)}
    return games

def start_game(game_path):
    
    pygame.quit()
    print(f"Starte Spiel: {game_path}")
    
    try:
        subprocess.run([sys.executable, game_path], check=True, 
                       stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen des Spiels {game_path}: {e}")
        
    os.execv(sys.executable, ['python3'] + sys.argv)
    
def main():
    
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Pygame Game Menu")
    
    try:
        font = pygame.font.Font(None, FONT_SIZE)
    except:
        font = pygame.font.SysFont("dejavusans", FONT_SIZE) # Alternative für Linux

    usb_path = find_usb_path()

    if not usb_path:
        games = {'USB-Stick nicht gefunden!': None}
    else:
        games = find_game_scripts(usb_path)
        if not games:
            games = {'Keine Pygame-Dateien (*.py) auf Stick gefunden!': None}

    menu_items = list(games.keys()) + ["Menü beenden (ESC)"]
    selected_index = 0
    
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    selected_item = menu_items[selected_index]
                    if selected_item == "Menü beenden (ESC)":
                        running = False
                    elif games[selected_item] is not None:
                        start_game(games[selected_item])
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BLACK)
        title_text = font.render("PYGAME SPIEL MENÜ", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, PADDING))
        Menü-Einträge zeichnen
        y_offset = title_text.get_height() + PADDING * 3
        
        for i, item in enumerate(menu_items):
            color = RED if i == selected_index else WHITE
            if item.startswith("USB-Stick") or item.startswith("Keine Pygame-Dateien"):
                color = RED
            
            text_surface = font.render(item, True, color)
            x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
            screen.blit(text_surface, (x, y_offset))
            
            y_offset += text_surface.get_height() + PADDING

        pygame.display.flip()
        clock.tick(30) # Begrenzt die Framerate

    pygame.quit()
    sys.exit()

if __name__ == '__menu__':
    try:
        main()
    except Exception as e:
        print(f"Kritischer Fehler im Menü: {e}")
        pygame.quit()
        sys.exit(1)
