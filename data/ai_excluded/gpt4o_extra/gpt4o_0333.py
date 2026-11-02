import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(i) for i in range(65, 65 + COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def check_for_win(board, checker):
    # Check horizontal
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == checker and all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == checker and all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == checker and all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    game_over = False

    print_board(board)

    while not game_over:
        col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a letter corresponding to a column.")
            continue

        col = ord(col_input) - 65
        if not is_valid_move(board, col):
            print("Invalid move. Column full or out of bounds.")
            continue

        row = get_next_open_row(board, col)
        drop_checker(board, row, col, CHECKERS[current_player])

        print_board(board)

        if check_for_win(board, CHECKERS[current_player]):
            game_over = True
            print(f"Player {CHECKERS[current_player]} won!")
        elif check_for_draw(board):
            game_over = True
            print("The game is a draw!")

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
