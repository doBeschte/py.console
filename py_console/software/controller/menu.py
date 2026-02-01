import pygame
import os
import subprocess
import glob
import sys

# --- KONSTANTEN ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT_SIZE = 36
PADDING = 20

# --- FUNKTIONEN ---

def find_usb_path():
    """Sucht nach dem Mount-Pfad des USB-Sticks unter /media/pi/"""
    mount_dir = "/media/pi"
    
    # Durchsuche alle Unterordner in /media/pi. Der erste gefundene ist wahrscheinlich der Stick.
    try:
        subdirs = [d for d in os.listdir(mount_dir) if os.path.isdir(os.path.join(mount_dir, d))]
        if subdirs:
            # Gib den vollständigen Pfad zum Stick zurück
            return os.path.join(mount_dir, subdirs[0])
        else:
            return None
    except FileNotFoundError:
        # Falls /media/pi nicht existiert (unwahrscheinlich auf Pi OS)
        return None
    except Exception as e:
        # Bei anderen Fehlern (z.B. Berechtigungen)
        print(f"Fehler beim Suchen des USB-Pfades: {e}")
        return None

def find_game_scripts(usb_path):
    """Sucht alle *.py Dateien (außer dem Menü selbst) auf dem USB-Stick."""
    
    # Suchmuster für .py-Dateien im Stammverzeichnis des Sticks
    search_pattern = os.path.join(usb_path, "*.py")
    
    # Liste der gefundenen Pfade
    script_paths = glob.glob(search_pattern)
    
    # Extrahiere nur den Dateinamen für das Menü (ohne Pfad)
    game_names = [os.path.basename(p) for p in script_paths]
    
    # Erstellt ein Dictionary: {'Spielname': 'Pfad'}
    games = {name: path for name, path in zip(game_names, script_paths)}
    
    return games

def start_game(game_path):
    """Startet das ausgewählte Python-Skript als externen Prozess."""
    
    # Beendet Pygame ordentlich, damit das Spiel den Bildschirm übernehmen kann
    pygame.quit()
    
    # Führt das Spiel mit dem Python-Interpreter aus
    # 'sys.executable' stellt sicher, dass der gleiche Interpreter verwendet wird
    # Dies ist für den Kiosk-Modus entscheidend!
    print(f"Starte Spiel: {game_path}")
    
    # subprocess.run wartet, bis das Spiel beendet ist
    # stdout/stderr wird zur Fehlerdiagnose in die Konsole umgeleitet
    try:
        subprocess.run([sys.executable, game_path], check=True, 
                       stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen des Spiels {game_path}: {e}")
        
    # Nach Beendigung des Spiels muss das Menü neu initialisiert werden
    # (Dies hängt davon ab, ob das Spiel den X-Server beendet oder nicht.
    # Im Kiosk-Modus starten wir das Menü meistens neu.)
    # Starte das Menü neu, indem wir uns selbst neu starten:
    os.execv(sys.executable, ['python3'] + sys.argv)
    

def main():
    """Hauptlogik des Pygame-Menüs"""
    
    pygame.init()

    # Vollbildmodus, nimmt die native Auflösung des Monitors an
    screen_info = pygame.display.Info()
    
    # Versuche, die größtmögliche Auflösung zu verwenden
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Pygame Game Menu")
    
    # Schriftart initialisieren
    try:
        font = pygame.font.Font(None, FONT_SIZE)
    except:
        font = pygame.font.SysFont("dejavusans", FONT_SIZE) # Alternative für Linux

    # USB-Stick Pfad finden
    usb_path = find_usb_path()

    if not usb_path:
        # Kein Stick gefunden: Zeige Fehlermeldung
        games = {'USB-Stick nicht gefunden!': None}
    else:
        # Spiele-Skripte finden
        games = find_game_scripts(usb_path)
        if not games:
            games = {'Keine Pygame-Dateien (*.py) auf Stick gefunden!': None}

    # Liste der Menü-Einträge und Auswahl-Index
    menu_items = list(games.keys()) + ["Menü beenden (ESC)"]
    selected_index = 0
    
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Tastensteuerung (Raspberry Pi OS Lite) ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    # ENTER gedrückt
                    selected_item = menu_items[selected_index]
                    if selected_item == "Menü beenden (ESC)":
                        running = False
                    elif games[selected_item] is not None:
                        # Spiel starten und diese Pygame-Instanz beenden
                        start_game(games[selected_item])
                        # Der Aufruf von os.execv() beendet das aktuelle Programm und startet das Menü neu
                        # Wenn wir hier ankommen, ist etwas beim Neustart schiefgelaufen, daher beenden wir:
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    # ESC gedrückt
                    running = False

        # --- Zeichnen ---
        screen.fill(BLACK)
        
        # Titel
        title_text = font.render("PYGAME SPIEL MENÜ", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, PADDING))

        # Menü-Einträge zeichnen
        y_offset = title_text.get_height() + PADDING * 3
        
        for i, item in enumerate(menu_items):
            color = RED if i == selected_index else WHITE
            
            # Fehler/Statusmeldungen hervorheben
            if item.startswith("USB-Stick") or item.startswith("Keine Pygame-Dateien"):
                color = RED
            
            text_surface = font.render(item, True, color)
            
            # Zentriert zeichnen
            x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
            screen.blit(text_surface, (x, y_offset))
            
            y_offset += text_surface.get_height() + PADDING

        pygame.display.flip()
        clock.tick(30) # Begrenzt die Framerate

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    # Behebt das Problem, dass der Pygame-Loop nicht neu startet, nachdem ein externes
    # Skript beendet wurde, indem das Skript bei Erfolg neu gestartet wird.
    # Dies ist die einfachste Lösung für den Kiosk-Modus-Neustart.
    try:
        main()
    except Exception as e:
        print(f"Kritischer Fehler im Menü: {e}")
        # Notfall-Exit:
        pygame.quit()
        sys.exit(1)