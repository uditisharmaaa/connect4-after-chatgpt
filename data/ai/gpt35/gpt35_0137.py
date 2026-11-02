import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_CONDITION = 4
COLUMN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for c in range(len(board[0])):
        header += "  " + COLUMN_LETTERS[c] + " "
    print(header)
    # Print the separator line below header
    print(" +" + "---+" * len(board[0]))
    # Print each row
    for row in board:
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
        print(" +" + "---+" * len(board[0]))

def get_random_start_player(num):
    return random.randint(0, num -1)

def is_valid_column(input_str, board):
    if len(input_str) != 1:
        return False
    if input_str not in COLUMN_LETTERS[:len(board[0])]:
        return False
    col_index = COLUMN_LETTERS.index(input_str)
    # Check if column is full
    if board[0][col_index] != " ":
        return False
    return True

def place_checker(board, col_index, checker):
    # Place checker from bottom to top in the column
    for row_index in range(len(board)-1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index, col_index
    # Should not reach here if column is valid but just in case
    return None, None

def check_win(board, checker, row, col):
    # Directions represented as (delta_row, delta_col)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1

        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players_checkers = CHECKERS[:NUM_PLAYERS]

    current_player = get_random_start_player(NUM_PLAYERS)

    print_board(board)
    print(f"Game start! Player {players_checkers[current_player]} begins.")

    while True:
        player_checker = players_checkers[current_player]
        # Input loop for valid move
        while True:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            if is_valid_column(user_input, board):
                col = COLUMN_LETTERS.index(user_input)
                break
            else:
                # If column is full, player loses turn
                if len(user_input) ==1 and user_input in COLUMN_LETTERS[:len(board[0])]:
                    col_check = COLUMN_LETTERS.index(user_input)
                    if board[0][col_check] != " ":
                        # Turn lost
                        print(f"Column {user_input} is full! You lose your turn.")
                        col = None
                        break
                print("Invalid input! Please enter a valid column letter (A-G) that is not full.")

        if col is not None:
            row_placed, col_placed = place_checker(board, col, player_checker)
            print_board(board)
            # Check win
            if check_win(board, player_checker, row_placed, col_placed):
                print(f"Player {player_checker} won!")
                break
            # Check draw
            if board_full(board):
                print("The game is a draw!")
                break
        else:
            # No checker placed, just print board after lost turn
            print_board(board)

        # Next player
        current_player = (current_player +1 ) % NUM_PLAYERS

if __name__ == "__main__":
    main()
