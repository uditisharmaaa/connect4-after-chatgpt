import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    cols = len(board[0])
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Print board rows
    for r in range(len(board)):
        print("+---" * cols + "+")
        row_str = ""
        for c in range(cols):
            row_str += "| " + board[r][c] + " "
        row_str += "|"
        print(row_str)
    print("+---" * cols + "+")

def is_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    c = input_str.upper()
    if c < 'A' or c >= chr(ord('A') + cols):
        return False
    return True

def column_index(column_letter):
    return ord(column_letter.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    # Place checker in the lowest empty spot in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # Column full

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(r_step, c_step):
        count = 0
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        return count

    # Check horizontal
    total = 1 + count_direction(0, 1) + count_direction(0, -1)
    if total >= 4:
        return True
    # Check vertical
    total = 1 + count_direction(1, 0) + count_direction(-1, 0)
    if total >= 4:
        return True
    # Check diagonal /
    total = 1 + count_direction(-1, 1) + count_direction(1, -1)
    if total >= 4:
        return True
    # Check diagonal \
    total = 1 + count_direction(1, 1) + count_direction(-1, -1)
    if total >= 4:
        return True

    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Set constants for this assignment
    rows = ROWS
    cols = COLS
    players = PLAYERS
    checkers = CHECKERS[:players]

    board = create_board(rows, cols)

    current_player = random.randint(0, players -1)

    while True:
        clear_screen()
        print_board(board)
        player_checker = checkers[current_player]
        print("Player {}, please enter a column:".format(player_checker))
        while True:
            user_input = input().strip()
            # Validate input
            if not is_valid_column(user_input, cols):
                print("Invalid input. Please enter a valid column letter (A-{}):".format(chr(ord('A')+cols-1)))
                continue
            col = column_index(user_input)
            # Try to place checker
            row_col = place_checker(board, col, player_checker)
            if row_col is None:
                # Column full, lose turn
                print("Column {} is full. You lose your turn.".format(user_input.upper()))
                break
            else:
                # Successful placement
                row, col_placed = row_col
                # Check for win
                if check_win(board, row, col_placed, player_checker):
                    clear_screen()
                    print_board(board)
                    print("Player {} won!".format(player_checker))
                    return
                break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            return

        # Next player
        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
