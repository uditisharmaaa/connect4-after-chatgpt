import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(COLS)]
    print('  ' + '   '.join(labels))
    # Print board rows with borders
    border = '+---' * COLS + '+'
    for row in board:
        print(border)
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
    print(border)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if col_char < 'A' or col_char >= chr(ord('A') + COLS):
        return False
    return True

def column_to_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col_index, checker):
    # Place checker in lowest available spot in column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index
    return None  # Column full

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal up-right
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    # If no empty spaces left, it's a draw
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True

def get_player_input(current_player):
    while True:
        inp = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if not is_valid_column(inp):
            continue
        return inp

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        col_char = get_player_input(current_player)
        col_index = column_to_index(col_char)

        placed = place_checker(board, col_index, players[current_player])
        if placed is None:
            # Column full, loses turn
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check for win
        if check_winner(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if check_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYERS


if __name__ == "__main__":
    main()
