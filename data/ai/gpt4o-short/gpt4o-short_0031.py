import os
import random

# Game Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Remove unused players for a current game
NUMBER_OF_PLAYERS = min(5, max(2, len(PLAYERS)))
PLAYERS = PLAYERS[:NUMBER_OF_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("=" * (COLUMNS*2 + 1))

def validate_input(col, board):
    if col not in COLUMN_LABELS:
        return False
    index = COLUMN_LABELS.index(col)
    return any(row[index] == ' ' for row in board)

def drop_piece(board, player, col):
    index = COLUMN_LABELS.index(col)
    for row in reversed(board):
        if row[index] == ' ':
            row[index] = player
            return

def check_winner(board, player):
    def check_direction(x_step, y_step, start_x, start_y):
        count = 0
        x, y = start_x, start_y
        while 0 <= x < ROWS and 0 <= y < COLUMNS and board[x][y] == player:
            count += 1
            if count >= 4:
                return True
            x += x_step
            y += y_step
        return False

    for x in range(ROWS):
        for y in range(COLUMNS):
            if board[x][y] == player:
                if (check_direction(1, 0, x, y) or  # Vertical
                    check_direction(0, 1, x, y) or  # Horizontal
                    check_direction(1, 1, x, y) or  # Diagonal down-right
                    check_direction(-1, 1, x, y)):  # Diagonal up-right
                    return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        print(f"Player {current_player}'s turn.")
        col = input(f"Choose a column ({COLUMN_LABELS}): ").upper().strip()

        if validate_input(col, board):
            drop_piece(board, current_player, col)
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} wins!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
            
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUMBER_OF_PLAYERS]
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    play_game()
