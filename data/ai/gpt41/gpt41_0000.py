import os
import random
import sys

# ----------------------- Constants -----------------------
ROWS = 6                     # Number of rows (height)
COLUMNS = 7                  # Number of columns (width)
MAX_COLUMNS = 26             # Max columns (for alphabet labeling)
PLAYER_SIGNS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2              # Set this to 2 for submission

# ---------------------- Functions ------------------------

def clear_screen():
    # Clear terminal screen
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    # Creates an empty board (list of lists) filled with whitespace
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)

    # Print column headers (A, B, ...)
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(cols)])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * cols)

def get_player_order(num_players):
    # Chooses a random player to start and returns player signs list rotated appropriately
    signs = PLAYER_SIGNS[:num_players]
    start = random.randint(0, num_players - 1)
    return signs[start:] + signs[:start]

def get_col_index(col_letter, cols):
    # Convert column letter to column index if valid
    if len(col_letter) != 1 or not col_letter.isalpha():
        return -1
    idx = ord(col_letter.upper()) - ord('A')
    if 0 <= idx < cols:
        return idx
    return -1

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, player_sign):
    rows = len(board)
    # Places the checker in the lowest available row
    for row in reversed(range(rows)):
        if board[row][col] == ' ':
            board[row][col] = player_sign
            return row, col
    return None, None

def is_valid_column_input(board, col_input):
    cols = len(board[0])
    idx = get_col_index(col_input, cols)
    if idx == -1:
        return False
    if is_column_full(board, idx):
        return False
    return True

def check_winner(board, player_sign):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player_sign for i in range(4)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == player_sign for i in range(4)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player_sign for i in range(4)):
                return True

    # Check diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == player_sign for i in range(4)):
                return True

    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    # Initialize board and players
    board = create_board(ROWS, COLUMNS)
    player_signs = get_player_order(NUM_PLAYERS)
    current_turn = 0
    game_over = False

    # Show initial board and state
    print_board(board)
    print("Players: " + ', '.join(player_signs))
    print("Player {} starts!".format(player_signs[0]))
    input("Press Enter to start...")

    while not game_over:
        print_board(board)
        cols = len(board[0])
        current_player = player_signs[current_turn % NUM_PLAYERS]
        print(f"Player {current_player}, please enter a column:")

        col_input = input().strip().upper()
        if not col_input:
            continue
        
        col_idx = get_col_index(col_input, cols)

        # Input validation
        if len(col_input) != 1 or col_idx == -1 or not col_input.isalpha():
            print("Invalid input. Please enter a column letter within range.")
            input("Press Enter to continue...")
            continue
        
        if is_column_full(board, col_idx):
            print("Column is full! You lose your turn.")
            input("Press Enter to continue...")
            current_turn += 1
            continue
        
        # Place checker
        row_placed, col_placed = place_checker(board, col_idx, current_player)
        # If no placement possible, column is full (shouldn't happen due to validation above)
        if row_placed is None:
            print("Column is full! You lose your turn.")
            input("Press Enter to continue...")
            current_turn += 1
            continue
        
        # Check for winner
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
            continue
        
        # Check for draw
        if board_full(board):
            print_board(board)
            print("Game is a draw!")
            game_over = True
            continue
        
        # Next player's turn
        current_turn += 1

if __name__ == '__main__':
    main()
