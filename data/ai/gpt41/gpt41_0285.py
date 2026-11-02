import os
import random

# ====== Constants ======
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

# ====== Board Initialization ======
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system("clear")
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")
        
# ====== Validation ======
def column_from_input(user_input):
    if len(user_input) != 1:
        return -1
    ch = user_input.upper()
    if ch < "A" or ch >= chr(ord("A") + COLUMNS):
        return -1
    return ord(ch) - ord("A")

def valid_move(board, col):
    return board[0][col] == " "

# ====== Game Mechanics ======
def place_checker(board, col, checker):
    for r in reversed(range(len(board))):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None, None  # Should not happen if move is validated

def check_win(board, row, col, checker):
    def count(r_step, c_step):
        cnt = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            cnt += 1
            r += r_step
            c += c_step
        return cnt
    
    # 4 directions: Horizontal, Vertical, Diagonal /
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        total = 1
        total += count(dr, dc)
        total += count(-dr, -dc)
        if total >= WIN_COUNT:
            return True
    return False

def is_board_full(board):
    return all(cell != " " for cell in board[0])

# ====== Main Game Loop ======
def main():
    board = create_board(ROWS, COLUMNS)
    player_tokens = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {player_tokens[current_player]} begins!")

    while True:
        print_board(board)
        checker = player_tokens[current_player]
        col = -1
        while True:
            user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            col = column_from_input(user_input)
            if col == -1:
                print("Invalid column, please enter a letter for a valid column.")
                continue
            if not valid_move(board, col):
                print("Column is full. You lose your turn!")
                col = -1
            break  # Exit loop on a valid (even if full) input
        
        if col != -1 and valid_move(board, col):
            row, _ = place_checker(board, col, checker)
            if check_win(board, row, col, checker):
                print_board(board)
                print(f"Player {checker} won!")
                break
            if is_board_full(board):
                print_board(board)
                print("It's a draw!")
                break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
