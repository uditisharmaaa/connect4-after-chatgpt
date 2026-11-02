import os
import random

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYER_COUNT]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear screen for Unix/Linux
    column_labels = ' '.join([chr(65 + i) for i in range(len(board[0]))])
    print("  " + column_labels)
    for row in board:
        print("+---" * COLUMN_COUNT + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMN_COUNT + "+")

def is_valid_input(input_char, col_count):
    if len(input_char) == 1 and input_char.isalpha() and 'A' <= input_char <= chr(65 + col_count - 1):
        return True
    return False

def get_next_open_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker):
    # Horizontal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Positive diagonal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Negative diagonal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def is_board_full(board):
    return all(board[0][c] != " " for c in range(COLUMN_COUNT))

def play_game():
    board = create_board(ROW_COUNT, COLUMN_COUNT)
    print_board(board)
    
    game_over = False
    turn = random.randint(0, PLAYER_COUNT - 1)

    while not game_over:
        print_board(board)
        player = CHECKERS[turn]
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        
        if is_valid_input(choice, COLUMN_COUNT):
            col = ord(choice) - 65
            row = get_next_open_row(board, col)
            if row is not None:
                drop_checker(board, row, col, player)
                if check_win(board, player):
                    print_board(board)
                    print(f"Player {player} won!")
                    game_over = True
                elif is_board_full(board):
                    print_board(board)
                    print("The game is a draw!")
                    game_over = True
                turn = (turn + 1) % PLAYER_COUNT
            else:
                print("Column is full. Turn is lost.")
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    play_game()
