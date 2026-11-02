import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear')

def create_board(rows, cols):
    """Initialize the game board with spaces"""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board"""
    clear_screen()
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_move(board, column):
    """Check if the move is valid"""
    return column.isalpha() and ord(column) - 65 < len(board[0]) and ord(column) - 65 >= 0 and board[0][ord(column) - 65] == " "

def place_checker(board, column, checker):
    """Place checker in the specified column"""
    col_index = ord(column) - 65
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the current player has won"""
    # Check horizontal locations
    for row in board:
        for col in range(COLS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True

    # Check vertical locations
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check positive diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check negative diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full and thus the game is a draw"""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main function to play the game"""
    board = create_board(ROWS, COLS)
    players = PLAYERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        
        move = input("> ").strip().upper()
        while not is_valid_move(board, move):
            print(f"Invalid move. Player {current_player}, please enter a valid column:")
            move = input("> ").strip().upper()
        
        if not place_checker(board, move, current_player):
            print("Column is full. Turn is lost.")
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (players.index(current_player) + 1) % len(players)
        current_player = players[current_player_index]

if __name__ == "__main__":
    play_game()
