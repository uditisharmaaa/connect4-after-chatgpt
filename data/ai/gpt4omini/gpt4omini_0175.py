import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates a 2D board initialized with whitespaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clears the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def get_column_input(player):
    """Prompts the player to enter a valid column."""
    while True:
        try:
            column = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
            if column < 'A' or column >= chr(65 + COLS) or len(column) != 1:
                raise ValueError("Invalid column input!")
            col_index = ord(column) - 65
            return col_index
        except ValueError as e:
            print(e)

def place_checker(board, col, player):
    """Places the player's checker in the specified column."""
    for row in reversed(board):  # Start from the bottom of the column
        if row[col] == ' ':
            row[col] = player
            return True
    return False  # Column is full

def check_winner(board, player):
    """Checks if the current player has won the game."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                # Check horizontally
                if c + 3 < COLS and all(board[r][c+i] == player for i in range(4)):
                    return True
                # Check vertically
                if r + 3 < ROWS and all(board[r+i][c] == player for i in range(4)):
                    return True
                # Check positively sloped diagonal
                if r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == player for i in range(4)):
                    return True
                # Check negatively sloped diagonal
                if r - 3 >= 0 and c + 3 < COLS and all(board[r-i][c+i] == player for i in range(4)):
                    return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    random_player = random.choice(PLAYERS[:2])  # Randomly select the first player among X and O
    current_player = random_player
    game_over = False

    print_board(board)

    while not game_over:
        col = get_column_input(current_player)
        
        if not place_checker(board, col, current_player):
            print("Column is full, try another column.")
            continue

        print_board(board)
        
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch players
            current_index = PLAYERS.index(current_player)
            current_player = PLAYERS[(current_index + 1) % 2]  # Only switch between X and O

if __name__ == "__main__":
    main()
