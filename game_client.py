import pygame
import socketio
import uuid
pygame.init()
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 30

sio = socketio.Client()
player_id = str(uuid.uuid4())
players = {}
font = pygame.font.SysFont(None, 20)
@sio.event
def connect():
    print('Connected to server')
    sio.emit('join', {'id': player_id})

@sio.on('update') # type: ignore
def on_update(data):
    global players
    players = data
    #print("Received update:", data)  # 👈 See what the server sends

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    sio.connect('http://localhost:8000')

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            sio.emit('move', {'id': player_id, 'direction': 'left'})
        if keys[pygame.K_RIGHT]:
            sio.emit('move', {'id': player_id, 'direction': 'right'})
        if keys[pygame.K_UP]:
            sio.emit('move', {'id': player_id, 'direction': 'up'})
        if keys[pygame.K_DOWN]:
            sio.emit('move', {'id': player_id, 'direction': 'down'})

        screen.fill((0, 0, 0))
        for pid, pos in players.items():
            color = (0, 255, 0) if pid == player_id else (255, 0, 0)
            pygame.draw.rect(screen, color, (pos['x'], pos['y'], PLAYER_SIZE, PLAYER_SIZE))
            name = pos.get('name', 'Unknown')
            screen.blit(font.render(name, True, (0, 128, 255)), (pos['x'],pos['y']-20))
        pygame.display.flip()

    pygame.quit()
    sio.disconnect()

if __name__ == '__main__':
    main()
