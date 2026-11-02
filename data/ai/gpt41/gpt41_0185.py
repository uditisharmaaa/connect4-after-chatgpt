import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
MAX_COLS = 26    # Max columns, labeled A-Z
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')  # For Unix/Linux. For Windows, use 'cls'.

def print_board(board):
    cols = len(board[0])
    # Print column labels (A, B, ...)
    col_labels = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(col_labels)
    print('+' + '---+' * cols)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    valid = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            valid.append(col)
    return valid

def column_from_input(input_letter, cols):
    input_letter = input_letter.upper()
    if len(input_letter) != 1 or input_letter not in string.ascii_uppercase[:cols]:
        return None
    return ord(input_letter) - ord('A')

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, checker, col):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal and Vertical
    for r in range(rows):
        for c in range(cols):
            # Horizontal
            if c + 3 < cols and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Vertical
            if r + 3 < rows and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Diagonal down-right
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Diagonal up-right
            if r - 3 >= 0 and c + 3 < cols and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def is_board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    # Randomly pick starting player
    current_player_idx = random.randint(0, NUM_PLAYERS-1)
    game_over = False
    winner = None
    
    clear_screen()
    print_board(board)
    
    while not game_over:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        valid_move = False
        col = None
        
        while not valid_move:
            player_input = input('> ').strip()
            col = column_from_input(player_input, BOARD_COLS)
            if col is None:
                print("Invalid input. Please enter a valid column letter.")
                continue
            if is_column_full(board, col):
                print("Column is full. You lose your turn.")
                valid_move = True  # Lose turn
                col = None
                break
            valid_move = True
        
        if col is not None:
            place_checker(board, current_checker, col)
            clear_screen()
            print_board(board)
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
                break
            if is_board_full(board):
                print("It's a draw!")
                break
        
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
