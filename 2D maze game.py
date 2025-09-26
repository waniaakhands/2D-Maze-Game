import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 30  
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# colors for maze ground and variables
PATH_COLOR = "#ECF0F1"  # Light grey
WALL_COLOR = "#2C3E50"     # dark blue walls
PLAYER_COLOR =  "#E74C3C" # Red
GOAL_COLOR = "#FFD700"   # Yellow
TEXT_COLOR = "#2C3E50"    # Dark text

# game variables
maze = []
player_pos = [0, 0]
goal_pos = [0, 0]
moves_taken = 0
game_over = False
game_won = False

# Maze Ground 
def generate_maze():
    global maze, player_pos, goal_pos
    
    #  maze walls
    maze = [[1 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
    
    def carve(x, y):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 1:
                # Break wall between 2 cells
                maze[y + dy//2][x + dx//2] = 0
                maze[ny][nx] = 0
                carve(nx, ny)

    #carving from center
    carve(MAZE_WIDTH // 2, MAZE_HEIGHT // 2)
    
    # Setting start position 
    player_pos = [0, 0]
    maze[player_pos[1]][player_pos[0]] = 0
    
    # farthest point from start for goal 
    frontier = [(player_pos[0], player_pos[1])]
    visited = set(frontier)
    
    while frontier:
        x, y = frontier.pop(0)
        goal_pos = [x, y]  
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and 
                maze[ny][nx] == 0 and (nx, ny) not in visited):
                visited.add((nx, ny))
                frontier.append((nx, ny))

# Player Movement 
def move_player(dx, dy):
    global player_pos, moves_taken, game_over, game_won
    if game_over:
        return

    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    # Checking boundaries and walls
    if (0 <= new_x < MAZE_WIDTH and 
        0 <= new_y < MAZE_HEIGHT and 
        maze[new_y][new_x] == 0):
        
        player_pos[0] = new_x
        player_pos[1] = new_y
        moves_taken += 1

        # Checking if goal is reached
        if player_pos == goal_pos:
            game_won = True
            game_over = True

# Drawing Functions
def draw_maze(screen):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1: 
                pygame.draw.rect(screen, WALL_COLOR, rect)
            else: 
                pygame.draw.rect(screen, PATH_COLOR, rect)

def draw_player(screen):
    center_x = player_pos[0] * CELL_SIZE + CELL_SIZE // 2
    center_y = player_pos[1] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, PLAYER_COLOR, (center_x, center_y), CELL_SIZE // 3)

def draw_goal(screen):
    center_x = goal_pos[0] * CELL_SIZE + CELL_SIZE // 2
    center_y = goal_pos[1] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.rect(screen, GOAL_COLOR, (center_x - CELL_SIZE // 4, center_y - CELL_SIZE // 4, CELL_SIZE // 2, CELL_SIZE // 2))

def display_message(screen, message, color=TEXT_COLOR, offset_y=0):
    font = pygame.font.Font(None, 74)
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + offset_y))
    screen.blit(text_surface, text_rect)

def display_hud(screen):
    font = pygame.font.Font(None, 36)
    moves_text = font.render(f"Moves: {moves_taken}", True, TEXT_COLOR)
    screen.blit(moves_text, (10, 10))

#  Main Body
def main():
    global game_over, game_won, moves_taken
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Maze Game")
    clock = pygame.time.Clock()
    
    generate_maze()
    
    running = True
    while running:
        screen.fill(PATH_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        move_player(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        move_player(1, 0)
                    elif event.key == pygame.K_UP:
                        move_player(0, -1)
                    elif event.key == pygame.K_DOWN:
                        move_player(0, 1)
                else:  # Game over or restart
                    if event.key == pygame.K_r:
                        game_over = False
                        game_won = False
                        moves_taken = 0
                        generate_maze()
                    elif event.key == pygame.K_q:
                        running = False
        
        draw_maze(screen)
        draw_player(screen)
        draw_goal(screen)
        display_hud(screen)
        
        if game_over:
            if game_won:
                display_message(screen, "YOU WIN!", (0, 180, 0))
            else:
                display_message(screen, "GAME OVER!", (220, 50, 50))
            display_message(screen, "Press 'R' to Restart or 'Q' to Quit", TEXT_COLOR, 50)
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
