import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print top border
    top_border = '+' + ('---+' * COLS)
    print(top_border)
    
    # Print each row
    for row in board:
        row_str = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(row_str)
        print(top_border)

def is_valid_move(board, col):
    # Check if column is within bounds and has at least one empty slot
    return 0 <= col < COLS and board[0][col] == ' '

def place_checker(board, col, checker):
    # Place checker at the lowest available row in the specified column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and two diagonal directions
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    
    for dr, dc in directions:
        for r in range(ROWS):
            for c in range(COLS):
                if (0 <= r + 3 * dr < ROWS and 
                    0 <= c + 3 * dc < COLS and 
                    all(board[r + i * dr][c + i * dc] == checker for i in range(4))):
                    return True
    return False

def is_draw(board):
    # Check if all top row cells are occupied
    return all(cell != ' ' for cell in board[0])

def get_player_move(player):
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        if not move or len(move) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col = ord(move) - ord('A')
        if 0 <= col < COLS:
            return col
        print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")

def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        clear_screen()
        print_board(board)
        
        # Get valid move
        while True:
            col = get_player_move(current_player)
            if is_valid_move(board, col):
                break
            print(f"Column {chr(65 + col)} is full. Please choose another column.")
        
        # Place checker and check for win/draw
        if place_checker(board, col, current_player):
            if check_win(board, current_player):
                clear_screen()
                print_board(board)
                print(f"Player {current_player} won!")
                return
            if is_draw(board):
                clear_screen()
                print_board(board)
                print("Game ended in a draw.")
                return
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
