import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_CHECKERS_TO_WIN = 4

def create_board():
    """Create a 2D board with whitespace cells"""
    board = []
    for _ in range(NUM_ROWS):
        row = [" " for _ in range(NUM_COLS)]
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  " + " ".join([chr(65 + i) for i in range(NUM_COLS)]))
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLS + "+")

def get_player_checker(player_num):
    """Get the checker symbol for the given player number"""
    return CHECKERS[player_num - 1]

def get_random_first_player(num_players):
    """Randomly select the first player"""
    return random.randint(1, num_players)

def is_valid_input(col, num_cols):
    """Check if the input column is valid"""
    if not col.isalpha():
        return False
    col_num = ord(col.upper()) - 65
    return 0 <= col_num < num_cols

def get_next_available_row(board, col):
    """Get the next available row in the given column"""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def is_win(board, player_checker):
    """Check if the given player has won"""
    # Check horizontal locations for win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - NUM_CHECKERS_TO_WIN + 1):
            if all([board[row][col + i] == player_checker for i in range(NUM_CHECKERS_TO_WIN)]):
                return True

    # Check vertical locations for win
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - NUM_CHECKERS_TO_WIN + 1):
            if all([board[row + i][col] == player_checker for i in range(NUM_CHECKERS_TO_WIN)]):
                return True

    # Check positively sloped diagonals
    for row in range(NUM_ROWS - NUM_CHECKERS_TO_WIN + 1):
        for col in range(NUM_COLS - NUM_CHECKERS_TO_WIN + 1):
            if all([board[row + i][col + i] == player_checker for i in range(NUM_CHECKERS_TO_WIN)]):
                return True

    # Check negatively sloped diagonals
    for row in range(NUM_ROWS - NUM_CHECKERS_TO_WIN + 1):
        for col in range(NUM_CHECKERS_TO_WIN - 1, NUM_COLS):
            if all([board[row + i][col - i] == player_checker for i in range(NUM_CHECKERS_TO_WIN)]):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw"""
    return all([all([cell!= " " for cell in row]) for row in board])

def main():
    num_players = MIN_PLAYERS
    board = create_board()
    current_player = get_random_first_player(num_players)

    while True:
        print_board(board)
        print(f"Player {get_player_checker(current_player)}, please enter a column:")
        col = input().upper()
        if not is_valid_input(col, NUM_COLS):
            print("Invalid input. Please try again.")
            continue

        col_num = ord(col) - 65
        row = get_next_available_row(board, col_num)
        if row == -1:
            print("Column is full. Please try again.")
            continue

        board[row][col_num] = get_player_checker(current_player)
        if is_win(board, get_player_checker(current_player)):
            print_board(board)
            print(f"Player {get_player_checker(current_player)} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player % num_players) + 1

if __name__ == "__main__":
    main()
