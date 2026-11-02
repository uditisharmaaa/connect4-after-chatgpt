import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "
WINNING_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[EMPTY_CELL for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + " ".join([chr(65 + i) for i in range(COLUMNS)]))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_column(col, board):
    if col < 0 or col >= COLUMNS:
        return False
    return board[0][col] == EMPTY_CELL

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == EMPTY_CELL:
            row[col] = checker
            return

def check_win(board, player):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - WINNING_COUNT + 1):
            if board[row][col] == player and all(board[row][col+i] == player for i in range(WINNING_COUNT)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - WINNING_COUNT + 1):
            if board[row][col] == player and all(board[row+i][col] == player for i in range(WINNING_COUNT)):
                return True

    # Diagonal \ check
    for row in range(ROWS - WINNING_COUNT + 1):
        for col in range(COLUMNS - WINNING_COUNT + 1):
            if board[row][col] == player and all(board[row+i][col+i] == player for i in range(WINNING_COUNT)):
                return True

    # Diagonal / check
    for row in range(WINNING_COUNT - 1, ROWS):
        for col in range(COLUMNS - WINNING_COUNT + 1):
            if board[row][col] == player and all(board[row-i][col+i] == player for i in range(WINNING_COUNT)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != EMPTY_CELL for col in range(COLUMNS))

def connect_four():
    board = create_board()
    current_player_idx = random.randint(0, PLAYERS - 1)
    players = CHECKERS[:PLAYERS]

    print_board(board)
    while True:
        player = players[current_player_idx]
        move_valid = False
        while not move_valid:
            try:
                col_input = input(f"Player {player}, please enter a column: ").strip().upper()
                col = ord(col_input) - 65
                if not is_valid_column(col, board):
                    print("Invalid move. Try again.")
                    continue
                move_valid = True
            except (ValueError, IndexError):
                print("Invalid input. Try again.")
        
        drop_checker(board, col, player)
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    connect_four()
