import pygame
import random
import socket
import pickle
import threading

SERVER_IP = "localhost"  # Listen on all network interfaces
SERVER_PORT = 5555

pygame.init()

WIDTH, HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
player_size = 50
player_speed = 5

projectile_speed = 7
projectiles = []

enemy_size = 40
enemy_speed = 3
enemies = []
enemy_spawn_delay = 60
enemy_spawn_counter = 0

teams = {
    "team_red": {"players": [], "color": RED},
    "team_blue": {"players": [], "color": BLUE},
}

players = {}
player_id_counter = 0

def handle_client(conn, addr):
    global player_id_counter
    player_id = f"player{player_id_counter}"
    player_id_counter += 1

    # Assign player to a team
    if len(teams["team_red"]["players"]) < 2:
        team = "team_red"
    else:
        team = "team_blue"
    teams[team]["players"].append(player_id)

    players[player_id] = {
        "x": WIDTH // 4 if team == "team_red" else 3 * WIDTH // 4,
        "y": HEIGHT // 2,
        "team": team,
    }

    print(f"Player {player_id} connected to {team}")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            # Receive player input from the client
            player_input = pickle.loads(data)
            update_player_position(player_id, player_input)
        except:
            break

    print(f"Player {player_id} disconnected")
    teams[team]["players"].remove(player_id)
    del players[player_id]
    conn.close()

def update_player_position(player_id, player_input):
    player = players[player_id]
    if player_input["left"] and player["x"] > 0:
        player["x"] -= player_speed
    if player_input["right"] and player["x"] < WIDTH - player_size:
        player["x"] += player_speed
    if player_input["up"] and player["y"] > 0:
        player["y"] -= player_speed
    if player_input["down"] and player["y"] < HEIGHT - player_size:
        player["y"] += player_speed

    if player_input["shoot"]:
        projectiles.append({
            "x": player["x"] + player_size // 2 - 5,
            "y": player["y"],
            "team": player["team"],
        })

def spawn_enemies():
    global enemy_spawn_counter
    enemy_spawn_counter += 1
    if enemy_spawn_counter >= enemy_spawn_delay:
        enemy_x = random.randint(0, WIDTH - enemy_size)
        enemies.append({"x": enemy_x, "y": 0, "width": enemy_size, "height": enemy_size})
        enemy_spawn_counter = 0

def move_projectiles():
    for projectile in projectiles:
        projectile["y"] -= projectile_speed
        if projectile["y"] < 0:
            projectiles.remove(projectile)

def move_enemies():
    for enemy in enemies:
        enemy["y"] += enemy_speed
        if enemy["y"] > HEIGHT:
            enemies.remove(enemy)

def check_collisions():
    for enemy in enemies:
        for projectile in projectiles:
            if (projectile["x"] < enemy["x"] + enemy_size and
                    projectile["x"] + 10 > enemy["x"] and
                    projectile["y"] < enemy["y"] + enemy_size and
                    projectile["y"] + 20 > enemy["y"]):
                enemies.remove(enemy)
                projectiles.remove(projectile)
                break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()