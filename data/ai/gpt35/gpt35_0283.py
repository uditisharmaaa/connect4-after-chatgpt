import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    separator = "+" + "---+" * len(board[0])
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column(col_char):
    return col_char in COLUMN_LABELS

def get_column_index(col_char):
    return COLUMN_LABELS.index(col_char)

def is_column_full(board, col_idx):
    # If top cell is occupied, column full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker in lowest available row in column col_idx
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None  # Column full

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, last_row, last_col, checker):
    # Check 4 directions: horizontal, vertical, diagonal /
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]
    for dr, dc in directions:
        count = 1
        # Count same checkers in positive direction
        count += check_direction(board, last_row + dr, last_col + dc, dr, dc, checker)
        # Count same checkers in negative direction
        count += check_direction(board, last_row - dr, last_col - dc, -dr, -dc, checker)
        if count >= WIN_LENGTH:
            return True
    return False

def is_draw(board):
    # Draw if no empty cell in top row
    return all(cell != " " for cell in board[0])

def get_valid_column_input(board, player_checker):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        if not is_valid_column(user_input):
            print("Invalid column. Please enter a valid column letter.")
            continue
        col_idx = get_column_index(user_input)
        if is_column_full(board, col_idx):
            print("Column full. You lose your turn.")
            return None  # Player loses turn
        return col_idx

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        col_idx = get_valid_column_input(board, player_checker)

        # Handle case if player loses turn (column full)
        if col_idx is None:
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        last_move = place_checker(board, col_idx, player_checker)
        print_board(board)

        # Check win
        if check_win(board, last_move[0], last_move[1], player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check draw
        if is_draw(board):
            print("Game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
