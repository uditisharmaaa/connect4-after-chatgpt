import os
import random

# Constants for players and game settings
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Adjust the number of players here (2 to 5)
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  ".join(COLUMN_LABELS))
    for row in board:
        print(" | ".join(row))
        print('-' * (COLS * 4 - 1))

# Get user move
def get_move(player):
    while True:
        move = input(f"Player {player}, choose a column (A-G): ").upper()
        if move in COLUMN_LABELS:
            index = COLUMN_LABELS.index(move)
            if board[0][index] == ' ':
                return index
            else:
                print("Column is full, choose another one.")
        else:
            print("Invalid move. Choose a column labeled A-G.")

# Drop piece in column
def drop_piece(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

# Check for win
def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][c] == player for c in range(col, col + 4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[r][col] == player for r in range(row, row + 4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Main game loop
def play_game():
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        current_player = players[current_player_index]
        
        move = get_move(current_player)
        drop_piece(board, move, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
