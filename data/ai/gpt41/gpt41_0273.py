import os
import random
import string

# === Constants ===
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # in order

# === Helper Functions ===

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    col_labels = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(col_labels))
    print("+" + "---+"*cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+"*cols)

def get_valid_columns(board):
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid_cols.append(col)
    return valid_cols

def input_column(board, player_checker):
    cols = len(board[0])
    valid_col_letters = list(string.ascii_uppercase[:cols])
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_col_letters:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col_idx = valid_col_letters.index(inp)
        if board[0][col_idx] != " ":
            print("Column is full. You lose your turn.")
            return -1  # Special value to indicate loss of turn
        return col_idx

def place_checker(board, col, checker):
    # Find the bottom most open row in column col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Shouldn't reach here if checked before

def is_winner(board, last_row, last_col, checker):
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = last_row+dr, last_col+dc
        while 0<=r<len(board) and 0<=c<len(board[0]) and board[r][c]==checker:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = last_row-dr, last_col-dc
        while 0<=r<len(board) and 0<=c<len(board[0]) and board[r][c]==checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != " " for cell in board[0])

# === Main Game ===

def main():
    board = create_board(ROWS, COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS-1)

    clear_screen()
    print_board(board, COLS)
    print(f"Player {player_checkers[current_player]} is randomly selected to start.")

    winner_found = False
    while True:
        checker = player_checkers[current_player]
        col = input_column(board, checker)
        if col == -1:  # Full column, player loses turn
            current_player = (current_player+1)%NUM_PLAYERS
            continue

        row_col = place_checker(board, col, checker)
        clear_screen()
        print_board(board, COLS)

        # Check win
        if is_winner(board, row_col[0], row_col[1], checker):
            print(f"Player {checker} won!")
            winner_found = True
            break
        # Draw
        if is_draw(board):
            print("The game is a draw!")
            break
        # Next player
        current_player = (current_player+1)%NUM_PLAYERS

if __name__ == "__main__":
    main()
