import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    # Print top border
    print('+' + '---+' * COLS)
    # Print rows
    for row in board:
        print('|' + '|'.join(' ' + cell + ' ' for cell in row) + '|')
        print('+' + '---+' * COLS)


def valid_input(inp, board):
    if len(inp) != 1:
        return False
    if inp not in COLUMN_LABELS:
        return False
    col = COLUMN_LABELS.index(inp)
    # Check if column is full
    return board[0][col] == ' '


def place_checker(board, col, checker):
    # Start from bottom row and find first empty cell
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False  # column full


def check_winner(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal down-right check
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal up-right check
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_COUNT)):
                return True
    return False


def board_full(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True


def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().upper()

        if not valid_input(user_input, board):
            print("Invalid input or column full, please try again.")
            continue

        col = COLUMN_LABELS.index(user_input)
        placed = place_checker(board, col, current_checker)
        if not placed:
            # According to assignment, player loses turn if column full
            current_player_index = (current_player_index + 1) % PLAYERS
            print(f"Column {user_input} is full, you lose your turn.")
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
