import random
import os

# Constants
NUM_COLUMNS = 7
NUM_ROWS = 6
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def create_board():
    """Initialize the board with empty spaces"""
    board = [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the game board"""
    os.system('clear')  # Use 'clear' for Unix/Linux or 'cls' for Windows
    print("  " + "   ".join(chr(65 + i) for i in range(NUM_COLUMNS)))
    print("+---" * NUM_COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLUMNS + "+")

def is_valid_input(column, board):
    """Check if the column input is valid"""
    if not column.isalpha() or not column.isupper():
        return False
    col_index = ord(column) - 65
    if col_index < 0 or col_index >= NUM_COLUMNS:
        return False
    if board[0][col_index] != ' ':
        return False
    return True

def place_checker(column, player_symbol, board):
    """Place the player's checker in the given column"""
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player_symbol
            break

def check_for_win(board, player_symbol):
    """Check if the player has won the game"""
    # Check horizontal, vertical and diagonal conditions
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row][col + i] == player_symbol for i in range(4)):
                return True

    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

            if all(board[row + 3 - i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Check if the game is a draw"""
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    print_board(board)

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        current_player = players[current_player_index]
        column = input(f"Player {current_player}, please enter a column: ").strip()

        while not is_valid_input(column, board):
            column = input(f"Invalid input. Player {current_player}, please enter a valid column: ").strip()

        place_checker(column, current_player, board)
        print_board(board)

        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_for_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
