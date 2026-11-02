import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty game board with specified rows and columns."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    # Print column labels
    print("  " + "   ".join(chr(65 + col) for col in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    # Print the rows of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(col, board):
    """Checks if the input column is valid and not full."""
    if col < 0 or col >= len(board[0]):
        return False
    return board[0][col] == " "

def get_column_choice(player, board):
    """Prompts the current player for a valid column choice."""
    while True:
        user_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or not ("A" <= user_input <= chr(65 + len(board[0]) - 1)):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = ord(user_input) - 65
        if not is_valid_column(col, board):
            print("Column is full or invalid. Try another column.")
            continue
        return col

def drop_checker(board, col, checker):
    """Drops the player's checker into the chosen column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break

def check_win(board, checker):
    """Checks if the given checker has achieved a win (horizontal, vertical, or diagonal)."""
    rows, cols = len(board), len(board[0])

    # Check horizontal win
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw (board is full)."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Game setup
    board = create_board(ROWS, COLS)
    num_players = 2  # Change to support more players if desired
    players = PLAYER_CHECKERS[:num_players]
    random.shuffle(players)
    current_player_index = 0

    # Print initial board
    print_board(board)

    # Main game loop
    while True:
        current_player = players[current_player_index]
        col = get_column_choice(current_player, board)
        drop_checker(board, col, current_player)
        
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
