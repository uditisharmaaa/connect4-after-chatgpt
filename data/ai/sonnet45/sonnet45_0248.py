import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_move(board, col):
    """Check if a move is valid (column exists and has space)."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def get_next_open_row(board, col):
    """Find the next open row in a column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def drop_piece(board, row, col, checker):
    """Place a checker on the board."""
    board[row][col] = checker

def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(COLS))

def get_player_move(board, player_checker):
    """Get and validate player input."""
    while True:
        try:
            move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            
            if len(move) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            if not move.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            col = ord(move) - ord('A')
            
            if col < 0 or col >= COLS:
                print(f"Invalid column. Please choose between A and {chr(65 + COLS - 1)}.")
                continue
            
            if not is_valid_move(board, col):
                print("Column is full. Please choose another column.")
                continue
            
            return col
        except Exception:
            print("Invalid input. Please try again.")

def play_game():
    """Main game loop."""
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        player_checker = players[current_player]
        
        col = get_player_move(board, player_checker)
        row = get_next_open_row(board, col)
        
        drop_piece(board, row, col, player_checker)
        print_board(board)
        
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
