import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(columns)]
    print('  ' + '   '.join(labels))
    line = '+---' * columns + '+'
    for row in board:
        print(line)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(line)

def get_column_index(user_input, columns):
    if len(user_input) != 1:
        return -1
    col_char = user_input.upper()
    index = ord(col_char) - ord('A')
    if 0 <= index < columns:
        return index
    return -1

def place_checker(board, col, checker):
    """
    Places checker in the lowest empty row of column col.
    Returns True if placed successfully, False if column full.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal down-right
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal up-right
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    players = MAX_PLAYERS
    checkers = CHECKERS[:players]

    current_player_index = random.randint(0, players - 1)

    print_board(board)

    while True:
        checker = checkers[current_player_index]
        # Player input loop
        while True:
            print(f"Player {checker}, please enter a column:")
            user_input = input().strip()
            col = get_column_index(user_input, COLUMNS)
            if col == -1:
                print("Invalid input. Please enter a valid column letter.")
                continue
            if board[0][col] != ' ':
                # Column full, lose turn
                print(f"Column {user_input.upper()} is full. You lose your turn.")
                # no placement, break to next player
                break
            # Place checker, guaranteed success since col not full
            place_checker(board, col, checker)
            break

        print_board(board)

        # Check if current player won (only if placed checker)
        if col != -1 and board[0][col] == checker or board_full(board) == False:
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
        
        if board_full(board):
            print("Game is a draw!")
            break

        current_player_index = (current_player_index + 1) % players

if __name__ == "__main__":
    main()
