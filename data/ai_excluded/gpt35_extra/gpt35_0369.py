import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players, we'll use first PLAYERS of them
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print rows
    for row in range(ROWS):
        print("+" + "---+" * COLUMNS)
        line = "|"
        for col in range(COLUMNS):
            line += " " + board[row][col] + " |"
        print(line)
    print("+" + "---+" * COLUMNS)

def is_valid_column(col_letter):
    return col_letter in COLUMN_LABELS

def column_to_index(col_letter):
    return COLUMN_LABELS.index(col_letter)

def place_checker(board, col_idx, checker):
    # Place checker in lowest empty row in column col_idx
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # If column full
    return None, None

def check_winner(board, row, col, checker):
    # Check all directions for 4 in a row

    def count_in_direction(r, c, dr, dc):
        count = 0
        rr, cc = r + dr, c + dc
        while 0 <= rr < ROWS and 0 <= cc < COLUMNS and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        return count

    # Directions: horizontal, vertical, diagonal /, diagonal \
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]
    for dr, dc in directions:
        # Count how many checkers in a row including current one
        count = 1
        count += count_in_direction(row, col, dr, dc)
        count += count_in_direction(row, col, -dr, -dc)
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def get_player_input(checker):
    while True:
        inp = input(f"Player {checker}, please enter a column: ")
        if len(inp) != 1:
            # Must be single character
            continue
        inp = inp.upper()
        if not is_valid_column(inp):
            continue
        yield inp

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        checker = players_checkers[current_player_idx]
        # Input validation
        valid_move = False
        lose_turn = False
        while not valid_move and not lose_turn:
            col_letter = input(f"Player {checker}, please enter a column: ").strip().upper()
            if len(col_letter) != 1:
                continue
            if not is_valid_column(col_letter):
                continue
            col_idx = column_to_index(col_letter)
            row, col = place_checker(board, col_idx, checker)
            if row is None:
                # Column full, lose turn
                lose_turn = True
                break
            else:
                valid_move = True

        if lose_turn:
            # Player loses turn, no checker placed
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check win
        if check_winner(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
