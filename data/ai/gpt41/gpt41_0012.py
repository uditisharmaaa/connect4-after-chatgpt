import os
import random
import string

# Global Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 players for submission
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def select_first_player(num_players):
    return random.randint(0, num_players - 1)

def valid_column_input(col_letter, cols):
    if len(col_letter) != 1:
        return False
    if col_letter not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_available_row(board, col):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def is_board_full(board):
    # Top row filled means board full
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            return False
    return True

def place_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Helper to check a segment of 4
    def check_segment(segment):
        return all(cell == checker for cell in segment)

    # Check horizontal win
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if check_segment([board[r][c + i] for i in range(WIN_LENGTH)]):
                return True

    # Check vertical win
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if check_segment([board[r + i][c] for i in range(WIN_LENGTH)]):
                return True

    # Check '/' diagonals
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if check_segment([board[r - i][c + i] for i in range(WIN_LENGTH)]):
                return True

    # Check '\' diagonals
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if check_segment([board[r + i][c + i] for i in range(WIN_LENGTH)]):
                return True

    return False

def get_player_input(board, current_player, cols):
    while True:
        col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if not valid_column_input(col_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = string.ascii_uppercase.index(col_input)
        if board[0][col_idx] != ' ':
            print("Column is full. You lose your turn.")
            return None  # Turn is lost
        return col_idx

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = NUM_PLAYERS
    player_checkers = CHECKERS[:num_players]
    current_player = select_first_player(num_players)

    print_board(board)
    print(f"Player {player_checkers[current_player]} begins.")

    while True:
        print_board(board)
        col = get_player_input(board, current_player, NUM_COLS)
        if col is None:
            # Lose turn if column is full
            current_player = (current_player + 1) % num_players
            continue
        row = get_available_row(board, col)
        if row is not None:
            place_checker(board, row, col, player_checkers[current_player])
            if check_win(board, player_checkers[current_player]):
                print_board(board)
                print(f"Player {player_checkers[current_player]} won!")
                break
            elif is_board_full(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % num_players
        else:
            # Should not reach here since get_player_input checks column full
            print("An error occurred while placing the checker.")

if __name__ == "__main__":
    main()
