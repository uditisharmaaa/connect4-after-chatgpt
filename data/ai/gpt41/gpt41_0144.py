import os
import random
import string

# --------------------- Constants ---------------------
NUM_ROWS = 6
NUM_COLS = 7  # Must not exceed 26
NUM_PLAYERS = 2  # Can be 2-5

CHECKERS = ['X', 'O', 'V', 'H', 'M']

# --------------------- Functions ---------------------

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column labels
    letters = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(letters)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_column_index(col_letter, cols):
    try:
        idx = string.ascii_uppercase.index(col_letter)
        if idx < cols:
            return idx
    except ValueError:
        return None
    return None

def is_column_full(board, col_idx):
    return board[0][col_idx] != ' '

def drop_checker(board, col_idx, checker):
    # Drop checker in the lowest empty spot (from bottom up)
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return True
    return False

def get_valid_input(board, cols):
    while True:
        move = input().strip().upper()
        if len(move) != 1 or move not in string.ascii_uppercase[:cols]:
            print(f"Invalid input! Please enter a valid column letter (A-{string.ascii_uppercase[cols-1]}):")
            continue
        col_idx = get_column_index(move, cols)
        if col_idx is None:
            print("Invalid column! Try again:")
            continue
        if is_column_full(board, col_idx):
            print("Column is full! You lose your turn.")
            return None  # Player loses turn
        return col_idx

def has_won(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

# --------------------- Main Game Loop ---------------------

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly pick a starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    clear_screen()
    print_board(board)
    print(f"Player {checkers[current_player_idx]}, please enter a column:")

    while True:
        col_idx = get_valid_input(board, NUM_COLS)
        if col_idx is not None:
            placed = drop_checker(board, col_idx, checkers[current_player_idx])
            # Should always succeed since we check for full column before
            clear_screen()
            print_board(board)
            # Check for win
            if has_won(board, checkers[current_player_idx]):
                print(f"Player {checkers[current_player_idx]} won!")
                break
            # Check for draw
            if is_draw(board):
                print("It's a draw!")
                break
        else:
            # Column full: lose turn, just skip
            clear_screen()
            print_board(board)
        # Swap to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        print(f"Player {checkers[current_player_idx]}, please enter a column:")

if __name__ == "__main__":
    main()
