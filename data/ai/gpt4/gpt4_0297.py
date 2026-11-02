import os
import random

# Global constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create and return an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    # Print column headers
    headers = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(headers)
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_column_choice(player, board):
    """Get a valid column choice from the player."""
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col) != 1 or not 'A' <= col <= chr(65 + COLUMNS - 1):
            print("Invalid input. Enter a valid column letter (e.g., A-G).")
            continue
        col_index = ord(col) - 65  # Convert letter to index
        if board[0][col_index] != " ":
            print("Column is full. Choose another one.")
            continue
        return col_index

def place_checker(board, col, checker):
    """Place a checker in the chosen column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break

def check_win(board, player_checker):
    """Check if the player has won horizontally, vertically or diagonally."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == player_checker:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if (board[row][col] == board[row+1][col] == 
                board[row+2][col] == board[row+3][col] == player_checker):
                return True

    # Check diagonals (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if (board[row][col] == board[row+1][col+1] == 
                board[row+2][col+2] == board[row+3][col+3] == player_checker):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == board[row-1][col+1] == 
                board[row-2][col+2] == board[row-3][col+3] == player_checker):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    # Initialize board
    board = create_board(ROWS, COLUMNS)
    print_board(board)

    # Initialize players
    players = CHECKERS[:MAX_PLAYERS]
    random.shuffle(players)
    print(f"The players are: {', '.join(players)}")
    print(f"Randomly selecting first player: Player {players[0]}")

    # Game loop
    current_player_index = 0
    while True:
        print_board(board)

        # Get the current player
        current_player = players[current_player_index]

        # Get and validate column choice
        col = get_column_choice(current_player, board)

        # Place the checker
        place_checker(board, col, current_player)

        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % len(players)

if __name__ == "__main__":
    main()
