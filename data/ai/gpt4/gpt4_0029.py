import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols

def create_board():
    """Create an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Clear the screen and print the current board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(col, board):
    """Check if the column is valid and not full."""
    return 0 <= col < COLS and board[0][col] == ' '

def place_checker(col, player, board):
    """Place the checker in the lowest available row in the column."""
    for row in range(ROWS-1, -1, -1):  # Start from the bottom of the column
        if board[row][col] == ' ':
            board[row][col] = player
            break

def check_win(player, board):
    """Check if the player has a winning condition."""
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Vertical Check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Diagonal (\) Check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Diagonal (/) Check
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the board is full and the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    # Initialization
    board = create_board()
    num_players = 2  # Set number of players
    players = PLAYERS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        current_player = players[current_player_idx]
        print(f"Player {current_player}, please enter a column: ", end="")
        col_input = input().upper()
        if len(col_input) != 1 or not col_input.isalpha():
            continue
        col = ord(col_input) - 65
        if not is_valid_column(col, board):
            continue
        
        place_checker(col, current_player, board)
        print_board(board)
        
        if check_win(current_player, board):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
