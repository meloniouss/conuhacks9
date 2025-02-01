import pygame
import socket
import pickle

SERVER_IP = "localhost"  # Replace with the server's IP address
SERVER_PORT = 5555

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter - Client")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server!")
        return client
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return None

def send_player_input(client, player_input):
    try:
        data = pickle.dumps(player_input)
        client.send(data)
    except Exception as e:
        print(f"Error sending player input: {e}")

def receive_game_state(client):
    try:
        data = client.recv(4096)
        if not data:
            print("No data received from server.")
            return None
        return pickle.loads(data)
    except Exception as e:
        print(f"Error receiving game state: {e}")
        return None

def draw_game_state(game_state):
    if not game_state:
        print("No game state to render.")
        return

    screen.fill(WHITE)
    for player_id, player in game_state["players"].items():
        color = RED if player["team"] == "team_red" else BLUE
        pygame.draw.rect(screen, color, (player["x"], player["y"], 50, 50))
    for projectile in game_state["projectiles"]:
        color = RED if projectile["team"] == "team_red" else BLUE
        pygame.draw.rect(screen, color, (projectile["x"], projectile["y"], 10, 20))
    for enemy in game_state["enemies"]:
        pygame.draw.rect(screen, BLACK, (enemy["x"], enemy["y"], 40, 40))
    pygame.display.flip()

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def start_menu():
    menu = True
    while menu:
        screen.fill(WHITE)
        draw_text("Top-Down Shooter", font, BLACK, WIDTH // 2, HEIGHT // 4)
        draw_text("Press SPACE to Start", small_font, BLACK, WIDTH // 2, HEIGHT // 2)
        draw_text("Press Q to Quit", small_font, BLACK, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q:
                    return False

def main():
    if not start_menu():
        pygame.quit()
        return

    client = connect_to_server()
    if not client:
        print("Failed to connect to server. Exiting.")
        pygame.quit()
        return

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        # Handle input
        keys = pygame.key.get_pressed()
        player_input = {
            "left": keys[pygame.K_LEFT],
            "right": keys[pygame.K_RIGHT],
            "up": keys[pygame.K_UP],
            "down": keys[pygame.K_DOWN],
            "shoot": keys[pygame.K_SPACE],
        }

        # Send input to server
        send_player_input(client, player_input)

        # Receive game state from server
        game_state = receive_game_state(client)
        if not game_state:
            print("No game state received. Exiting.")
            break

        draw_game_state(game_state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    client.close()
    pygame.quit()

if __name__ == "__main__":
    main()