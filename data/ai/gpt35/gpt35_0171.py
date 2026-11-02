import os
import random
import string

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
CONNECT_N = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    rows = len(board)
    # Print column labels
    labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(labels))
    print("+---" * cols + "+")
    for r in range(rows):
        print("| " + " | ".join(board[r]) + " |")
        print("+---" * cols + "+")

def is_valid_column(choice, columns):
    if len(choice) != 1:
        return False
    if choice not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_column_index(choice):
    return string.ascii_uppercase.index(choice)

def column_not_full(board, col_idx):
    # Top row empty means column not full
    return board[0][col_idx] == " "

def place_checker(board, col_idx, checker):
    rows = len(board)
    # Place from bottom up
    for r in reversed(range(rows)):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    return None

def check_winner(board, last_r, last_c, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 1  # count the last placed checker itself
        # forward direction
        r, c = last_r + dr, last_c + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # backward direction
        r, c = last_r - dr, last_c - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        return count

    # Check horizontal, vertical, diagonal /
    if count_direction(0,1) >= CONNECT_N:
        return True
    if count_direction(1,0) >= CONNECT_N:
        return True
    if count_direction(1,1) >= CONNECT_N:
        return True
    if count_direction(1,-1) >= CONNECT_N:
        return True

    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS-1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            choice = input().strip().upper()
            if not is_valid_column(choice, COLUMNS):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col_idx = get_column_index(choice)
            if not column_not_full(board, col_idx):
                # Column full: player loses turn
                break
            else:
                placed = place_checker(board, col_idx, current_checker)
                break  # Valid move done

        if col_idx is not None and placed is not None:
            r, c = placed
            if check_winner(board, r, c, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                return
        else:
            # full column chosen - player loses turn (per instructions)
            pass

        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
