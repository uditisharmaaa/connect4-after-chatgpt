import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create the Connect 4 board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_player_input(player, board):
    """Get valid input from the player for their column choice."""
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1):
            col_index = ord(column) - 65
            if board[0][col_index] == ' ':
                return col_index
            else:
                print("Column is full, try another column.")
        else:
            print("Invalid input, please enter a letter from A to " + chr(65 + COLS - 1) + ".")

def place_checker(board, col_index, player):
    """Place the player's checker in the specified column."""
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player
            return True
    return False

def check_winner(board, player):
    """Check all win conditions for the specified player."""
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if (c + 3 < COLS and all(board[r][c + i] == player for i in range(4))) or \
                   (r + 3 < ROWS and all(board[r + i][c] == player for i in range(4))) or \
                   (r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4))) or \
                   (r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player for i in range(4))):
                    return True
    return False

def is_draw(board):
    """Check if the board is full."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_index = get_player_input(current_player, board)
        place_checker(board, col_index, current_player)
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
