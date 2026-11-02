import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Column labels (A, B, C, ...)
    labels = '  ' + '   '.join(string.ascii_uppercase[:columns])
    print(labels)
    horizontal_line = '+' + '---+' * columns
    rows = len(board)
    for row in range(rows):
        print(horizontal_line)
        # Print each cell in row
        print('|' + '|'.join(f' {board[row][col]} ' for col in range(columns)) + '|')
    print(horizontal_line)

def is_valid_column(input_str, columns):
    # Validates if input_str is one uppercase letter within board columns
    if len(input_str) != 1:
        return False
    if input_str not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_column_index(column_letter):
    return ord(column_letter) - ord('A')

def place_checker(board, column_index, checker):
    # Places checker in lowest empty row in the column
    # Returns True if placed, False if column is full
    for row in range(len(board)-1, -1, -1):
        if board[row][column_index] == ' ':
            board[row][column_index] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    columns = len(board[0])
    length = WIN_LENGTH

    # Horizontal check
    for r in range(rows):
        for c in range(columns - length + 1):
            if all(board[r][c + i] == checker for i in range(length)):
                return True

    # Vertical check
    for c in range(columns):
        for r in range(rows - length + 1):
            if all(board[r + i][c] == checker for i in range(length)):
                return True

    # Diagonal down-right check
    for r in range(rows - length + 1):
        for c in range(columns - length + 1):
            if all(board[r + i][c + i] == checker for i in range(length)):
                return True

    # Diagonal up-right check
    for r in range(length - 1, rows):
        for c in range(columns - length + 1):
            if all(board[r - i][c + i] == checker for i in range(length)):
                return True

    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    rows = ROWS
    columns = COLUMNS
    num_players = 2
    players = PLAYERS[:num_players]

    board = create_board(rows, columns)

    current_player_idx = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {players[current_player_idx]} goes first!")

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, columns):
                print(f"Invalid input. Please enter a single uppercase letter between A and {chr(ord('A') + columns - 1)}.")
                continue
            col_idx = get_column_index(user_input)
            # Check if column is full
            if board[0][col_idx] != ' ':
                print("Column is full. You lose your turn.")
                placed = False
                break
            placed = place_checker(board, col_idx, checker)
            if placed:
                break
            else:
                # This shouldn't occur here because we check full by top row
                print("Column is full. You lose your turn.")
                break

        print_board(board)

        if placed:
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if is_board_full(board):
                print("The game is a draw!")
                break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == '__main__':
    main()
