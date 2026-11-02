import os
import random
import sys

# ======== CONSTANTS ======== #
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_COUNT = 4

# ======== FUNCTIONS ======== #

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([' ' for _ in range(cols)])
    return board

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(labels))
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_player_input(current_player, board):
    cols = len(board[0])
    valid_cols = [chr(ord('A') + i) for i in range(cols)]
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ")
        user_input = user_input.strip().upper()
        if len(user_input) != 1 or user_input not in valid_cols:
            print("Invalid column. Please enter a valid column letter (A-G).")
            continue
        col_number = ord(user_input) - ord('A')
        if board[0][col_number] != ' ':
            print("Column is full! You lose your turn.")
            return None  # Lose turn if column is full
        return col_number

def place_checker(board, col, symbol):
    # Start from bottom row and go up
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = symbol
            return True
    return False  # Should not occur if validated earlier

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == symbol for i in range(WIN_COUNT)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == symbol for i in range(WIN_COUNT)):
                return True

    # Check diagonal /
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == symbol for i in range(WIN_COUNT)):
                return True

    # Check diagonal \
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == symbol for i in range(WIN_COUNT)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    # Board dimensions and number of players are set to required values
    rows = NUM_ROWS
    cols = NUM_COLS
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(rows, cols)
    first_player = random.randint(0, NUM_PLAYERS - 1)
    current_player_index = first_player

    print_board(board)
    print(f"Player {players[current_player_index]} starts!\nPress Enter to begin...")
    input()

    while True:
        print_board(board)
        current_player = players[current_player_index]
        col_choice = get_player_input(current_player, board)
        if col_choice is None:
            # Lose turn if column is full
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        placed = place_checker(board, col_choice, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
