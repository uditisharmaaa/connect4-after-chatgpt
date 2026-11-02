import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board():
    """
    Initialize the game board with empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """
    Print the game board in a formatted manner.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(ord('A') + col)}  ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(COLS):
        print("---+", end="")
    print()
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(COLS):
            print("---+", end="")
        print()

def get_column_index(col_letter):
    """
    Convert column letter to index (A=0, B=1, etc.).
    Returns -1 if invalid.
    """
    col_letter = col_letter.upper()
    if len(col_letter) == 1 and 'A' <= col_letter <= chr(ord('A') + COLS - 1):
        return ord(col_letter) - ord('A')
    return -1

def is_valid_move(board, col_index):
    """
    Check if a move is valid (column exists and has space).
    """
    if col_index < 0 or col_index >= COLS:
        return False
    # Check if top cell is empty
    return board[0][col_index] == " "

def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_horizontal_win(board, checker):
    """
    Check if there's a horizontal win for the given checker.
    """
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_vertical_win(board, checker):
    """
    Check if there's a vertical win for the given checker.
    """
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_diagonal_win(board, checker):
    """
    Check if there's a diagonal win for the given checker.
    Checks both directions: / and \.
    """
    # Check \ diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check / diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_win(board, checker):
    """
    Check if the given checker has won the game.
    """
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))

def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    """
    return all(board[0][col] != " " for col in range(COLS))

def get_player_move(board, player_num):
    """
    Get a valid move from the player.
    Keeps asking until a valid move is provided.
    """
    while True:
        try:
            user_input = input(f"Player {CHECKERS[player_num]}, please enter a column: ").strip()
            col_index = get_column_index(user_input)
            
            if col_index == -1:
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
                continue
            
            if not is_valid_move(board, col_index):
                print(f"Column {user_input.upper()} is full or invalid. Please try another column.")
                continue
            
            return col_index
        except Exception as e:
            print("Invalid input. Please try again.")

def play_game():
    """
    Main game loop.
    """
    board = initialize_board()
    print_board(board)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        # Get player move
        col_index = get_player_move(board, current_player)
        
        # Place checker
        checker = CHECKERS[current_player]
        place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

def main():
    """
    Entry point of the program.
    """
    play_game()

if __name__ == "__main__":
    main()
