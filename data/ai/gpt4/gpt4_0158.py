import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
EMPTY_SLOT = " "

def clear_screen():
    os.system('clear')

def create_board():
    return [[EMPTY_SLOT for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(col, board):
    return col.isalpha() and col.upper() in [chr(65 + i) for i in range(COLUMNS)] and board[0][ord(col.upper()) - 65] == EMPTY_SLOT

def place_checker(col, player, board):
    col_idx = ord(col.upper()) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == EMPTY_SLOT:
            board[row][col_idx] = player
            return row, col_idx

def check_winner(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != EMPTY_SLOT for col in range(COLUMNS))

def main():
    clear_screen()
    
    # Initialization
    board = create_board()
    num_players = 2  # Change this to 3-5 for more players
    players = PLAYER_CHECKERS[:num_players]
    current_player = random.choice(players)

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        col = input().strip()

        # Validate input
        if not is_valid_column(col, board):
            print("Invalid input. Please try again.")
            continue

        # Place checker
        _, _ = place_checker(col, current_player, board)
        
        clear_screen()
        print_board(board)

        # Check for win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = players.index(current_player)
        current_player = players[(current_player_index + 1) % num_players]

if __name__ == "__main__":
    main()
