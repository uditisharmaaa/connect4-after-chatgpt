import os
import random

# Constants - You can change here for other dimensions and number of players
ROWS = 6
COLS = 7
PLAYERS = 2  # from 2 up to 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    return [[" " for _ in range(cols)] for __ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers (A-G for 7 columns)
    header = "  "
    for i in range(cols):
        header += "  " + chr(ord('A') + i) + " "
    print(header)

    # Print top line
    line = "+"
    for _ in range(cols):
        line += "---+"
    # Print rows
    for row in board:
        print(line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(line)

def valid_column_input(inp, board):
    if len(inp) != 1:
        return False
    col = inp.upper()
    if col < 'A' or col > chr(ord('A') + len(board[0]) - 1):
        return False
    col_idx = ord(col) - ord('A')
    # Check if column is full
    if board[0][col_idx] != " ":
        return False
    return True

def place_checker(board, col_idx, checker):
    # Place checker in the lowest empty spot in the given column
    for row_i in range(len(board)-1, -1, -1):
        if board[row_i][col_idx] == " ":
            board[row_i][col_idx] = checker
            return row_i, col_idx
    # Column full
    return None, None

def check_line(board, start_r, start_c, dr, dc, checker):
    count = 0
    r, c = start_r, start_c
    rows = len(board)
    cols = len(board[0])
    # Count consecutive checkers in direction (dr, dc)
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, last_r, last_c, checker):
    # Check four directions for 4 in a row:
    # Horizontal, Vertical, Diagonal /
    # Diagonal \
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # Count consecutive checkers in the negative direction
        neg_count = check_line(board, last_r - dr, last_c - dc, -dr, -dc, checker)
        # Count consecutive checkers in the positive direction
        pos_count = check_line(board, last_r, last_c, dr, dc, checker)
        # 1 overlap at last position so subtract 1
        total = neg_count + pos_count - 1
        if total >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    for cell in board[0]:  # Top row
        if cell == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        # Input loop to get valid input
        while True:
            inp = input(prompt).strip().upper()
            if not valid_column_input(inp, board):
                # If column full, lose turn and break input loop
                col_candidate = inp if len(inp)==1 and 'A' <= inp <= chr(ord('A') + COLS -1) else None
                if col_candidate is not None:
                    col_idx_candidate = ord(col_candidate) - ord('A')
                    if board[0][col_idx_candidate] != " ":
                        # Column full, lose turn
                        last_r, last_c = None, None
                        break
                print("Invalid input. Please enter a valid column (A-G) that is not full.")
                continue
            else:
                col_idx = ord(inp) - ord('A')
                last_r, last_c = place_checker(board, col_idx, checker)
                break

        print_board(board)
        if last_r is not None and last_c is not None:
            # Check win after a successful placement
            if check_win(board, last_r, last_c, checker):
                print(f"Player {checker} won!")
                break
            elif board_full(board):
                print("Game is a draw!")
                break
        else:
            # player loses turn due to full column input
            pass

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
