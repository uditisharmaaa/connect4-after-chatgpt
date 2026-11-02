import os
import random

# ---------------------- CONSTANTS ------------------------
ROWS = 6
COLUMNS = 7
MAX_COLS = 26   # For generalization (max columns = 26, 'A' to 'Z')
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# -------------------- FUNCTIONS --------------------------

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    cols = len(board[0])
    header = '  '
    for i in range(cols):
        header += chr(ord('A') + i) + '   '
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def select_first_player(num_players):
    return random.randint(0, num_players - 1)

def get_move(player_checker, valid_cols):
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").upper().strip()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        col = ord(move) - ord('A')
        if col not in valid_cols:
            print("Invalid column. Please select a valid, non-full column.")
            continue
        return col

def get_valid_columns(board):
    valid_cols = []
    for col in range(len(board[0])):
        if any(board[row][col] == ' ' for row in range(len(board))):
            valid_cols.append(col)
    return valid_cols

def place_checker(board, col, checker):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col  # Return position of placed checker
    return None, None  # Column is full

def check_win(board, player_checker):
    rows = len(board)
    cols = len(board[0])
    # Directions: (row_step, col_step)
    directions = [(0,1), (1,0), (1,1), (1,-1)] # horiz, vert, diag down-right, diag down-left
    for row in range(rows):
        for col in range(cols):
            if board[row][col] != player_checker:
                continue
            for dr, dc in directions:
                count = 0
                r, c = row, col
                for _ in range(4):
                    if 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
                        count += 1
                    else:
                        break
                    r += dr
                    c += dc
                if count == 4:
                    return True
    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = select_first_player(NUM_PLAYERS)
    print_board(board)
    print(f"Player {players[current_player]} goes first!")

    while True:
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print_board(board)
            print("It's a draw!")
            break

        print_board(board)
        col = get_move(players[current_player], valid_cols)
        row, _ = place_checker(board, col, players[current_player])
        if row is None:
            print(f"Column {chr(ord('A') + col)} is full. Turn lost!")
            # Skip to next player
        else:
            # Check win
            if check_win(board, players[current_player]):
                print_board(board)
                print(f"Player {players[current_player]} won!")
                break
            # Check draw
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
