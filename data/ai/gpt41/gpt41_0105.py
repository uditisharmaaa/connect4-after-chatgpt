import os
import random

# Constants (change if you want to test with different board sizes or more players)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change between 2 to 5

CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

COLUMN_LABELS = [chr(ord("A") + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_column(col):
    return col in COLUMN_LABELS

def is_column_full(board, col):
    col_index = COLUMN_LABELS.index(col)
    return board[0][col_index] != " "

def place_checker(board, col, checker):
    col_index = COLUMN_LABELS.index(col)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None, None  # Column is full

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Including the just placed checker
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(current_checker, board):
    while True:
        move = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(move) != 1 or not is_valid_column(move):
            print("Invalid column. Please enter a valid column letter.")
            continue
        if is_column_full(board, move):
            print("That column is full. You lose your turn!")
            return None   # Player loses their turn
        return move

def main():
    board = create_board()
    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    while True:
        checker = PLAYER_CHECKERS[current_player]
        move = get_player_move(checker, board)
        if move is not None:
            row, col = place_checker(board, move, checker)
            clear_screen()
            print_board(board)
            if check_win(board, row, col, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
        else:
            # Print the latest board, but skip their move
            clear_screen()
            print_board(board)
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
