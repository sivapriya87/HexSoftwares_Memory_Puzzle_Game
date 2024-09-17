import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
CARD_SIZE = (100, 100)
GRID_SIZE = (4, 4)
TIME_LIMIT = 60  # seconds

# Colors
WHITE = (255, 255, 255)
CARD_COLOR = (184, 222, 227)  # #b8dee3 in RGB
SYMBOL_COLOR = (108, 163, 171)  # #6ca3ab in RGB
BLACK = (0, 0, 0)

# Define symbols for card faces
SYMBOLS = ['*', '#', '@', '&', '+', '-', '/', '\\', '■', '□', '●', '○', '▲', '△', '★']

# Define the number of symbols used in the grid
NUM_SYMBOLS = GRID_SIZE[0] * GRID_SIZE[1] // 2  # half the grid size for pairs
assert NUM_SYMBOLS <= len(SYMBOLS), "Not enough symbols for the grid size"

def create_card_grid():
    pairs = SYMBOLS[:NUM_SYMBOLS] * 2
    random.shuffle(pairs)
    return [pairs[i:i + GRID_SIZE[0]] for i in range(0, len(pairs), GRID_SIZE[0])]

def draw_grid(screen, grid, revealed, matched_message=None, time_remaining=None):
    font = pygame.font.SysFont(None, 72)  # Use default font
    
    for row in range(GRID_SIZE[0]):
        for col in range(GRID_SIZE[1]):
            x = col * CARD_SIZE[0]
            y = row * CARD_SIZE[1]
            rect = pygame.Rect(x, y, CARD_SIZE[0], CARD_SIZE[1])
            
            if revealed[row][col]:
                text = font.render(grid[row][col], True, SYMBOL_COLOR)
                screen.blit(text, rect.topleft)
            else:
                pygame.draw.rect(screen, CARD_COLOR, rect)  # Draw card background color
                pygame.draw.rect(screen, WHITE, rect, 2)  # Draw white border
    
    if matched_message:
        # Draw a white background for the message
        message_font = pygame.font.SysFont(None, 48)
        message_text = message_font.render(matched_message, True, BLACK)
        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Draw the white background for the message
        pygame.draw.rect(screen, WHITE, message_rect.inflate(20, 20))  # White background with padding
        screen.blit(message_text, message_rect)
    
    if time_remaining is not None:
        # Display the timer in the top-left corner
        timer_font = pygame.font.SysFont(None, 48)
        timer_text = timer_font.render(f"Time Left: {int(time_remaining)}", True, BLACK)
        screen.blit(timer_text, (10, 10))  # Display timer in the top-left corner

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Memory Puzzle Game')

    clock = pygame.time.Clock()

    # Game setup
    grid = create_card_grid()
    revealed = [[False] * GRID_SIZE[1] for _ in range(GRID_SIZE[0])]
    first_choice = None
    second_choice = None
    start_time = time.time()
    game_over = False
    matched_message = None
    message_start_time = None

    while not game_over:
        screen.fill(WHITE)  # Background for the game window
        elapsed_time = time.time() - start_time
        time_remaining = max(TIME_LIMIT - elapsed_time, 0)  # Calculate remaining time

        if matched_message:
            draw_grid(screen, grid, revealed, matched_message, time_remaining)
            elapsed_message_time = time.time() - message_start_time
            if elapsed_message_time > 1:  # Display message for 1 second
                matched_message = None
        else:
            draw_grid(screen, grid, revealed, time_remaining=time_remaining)

        if first_choice and second_choice:
            if grid[first_choice[0]][first_choice[1]] == grid[second_choice[0]][second_choice[1]]:
                matched_message = "Matched!"
                message_start_time = time.time()
            else:
                pygame.time.wait(1000)  # Pause for a second if no match
                revealed[first_choice[0]][first_choice[1]] = False
                revealed[second_choice[0]][second_choice[1]] = False
            first_choice = None
            second_choice = None

        if time_remaining <= 0:
            game_over = True
            result_text = "Time's up! You lost!"
        elif all(all(row) for row in revealed):
            game_over = True
            result_text = "Congratulations! You won!"

        if game_over:
            font = pygame.font.SysFont(None, 72)
            text = font.render(result_text, True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        else:
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not first_choice or not second_choice:
                    x, y = event.pos
                    row, col = y // CARD_SIZE[1], x // CARD_SIZE[0]
                    if not revealed[row][col]:
                        revealed[row][col] = True
                        if not first_choice:
                            first_choice = (row, col)
                        elif not second_choice:
                            second_choice = (row, col)

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
