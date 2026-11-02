import os
import random
import string

# ========== Constants ==========
ROWS = 6                       # Number of rows in the board
COLS = 7                       # Number of columns in the board (max 26)
NUM_PLAYERS = 2                # Number of players (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players

# ========== Helper Functions ==========

def clear_screen():
    # Clear the terminal screen
    os.system('clear')

def init_board(rows, cols):
    # Create the initial board with ALL empty cells
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print the board in the required format
    clear_screen()
    cols = len(board[0])
    # Header
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    # Returns list of columns (indices) that are not full
    cols = []
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            cols.append(c)
    return cols

def letter_to_col(letter):
    # Convert column letter to index (A -> 0, B -> 1, ...)
    letter = letter.upper()
    if letter in string.ascii_uppercase:
        col = ord(letter) - ord('A')
        return col
    return None

def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the specified column
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Should not happen if column checked before

def is_full(board):
    # Check if the entire board is full (no empty cell in top row)
    return all(cell != ' ' for cell in board[0])

def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def get_player_input(board, player_checker):
    valid_letters = string.ascii_uppercase[:len(board[0])]
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_letters:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = letter_to_col(inp)
        if col is None or not (0 <= col < len(board[0])):
            print("Invalid column letter. Please choose between A and", valid_letters[-1])
            continue
        if board[0][col] != ' ':
            print("That column is full. You lose your turn!")
            return None  # Return None to indicate a lost turn
        return col

# ========== Main Game Loop ==========

def main():
    # Choose checkers for NUM_PLAYERS
    checkers = CHECKERS[:NUM_PLAYERS]

    board = init_board(ROWS, COLS)

    # Randomly choose first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {checkers[current_player]} will start!")

    while True:
        print_board(board)
        col = get_player_input(board, checkers[current_player])

        if col is not None:
            drop_checker(board, col, checkers[current_player])
            if check_win(board, checkers[current_player]):
                print_board(board)
                print(f"Player {checkers[current_player]} won!")
                break
            if is_full(board):
                print_board(board)
                print("Game is a draw!")
                break
        # If player loses turn (column full), just switch to next player.

        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
