import os
import random
import string

# Constants (change if you want to test, but submission should be 6x7 and 2 players)
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players

def clear_screen():
    os.system('clear')   # for Linux/Unix terminal

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    # Print top border
    print("+" + "---+" * cols)
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    valid = []
    for c in range(len(board[0])):
        if board[0][c] == " ":
            valid.append(c)
    return valid

def get_player_input(board):
    cols = len(board[0])
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in valid_letters:
            print("Invalid input. Please enter a column letter from", valid_letters[0], "to", valid_letters[-1])
            continue
        col = ord(col_input) - ord('A')
        if board[0][col] != " ":
            print("Column is full. Please select another column.")
            continue
        return col

def place_checker(board, col, checker):
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None, None  # should not happen if handled correctly

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # check horizontal
            if c + 3 < cols and all(board[r][c + i] == checker for i in range(4)):
                return True
            # check vertical
            if r + 3 < rows and all(board[r + i][c] == checker for i in range(4)):
                return True
            # check diagonal /
            if r - 3 >= 0 and c + 3 < cols and all(board[r - i][c + i] == checker for i in range(4)):
                return True
            # check diagonal \
            if r + 3 < rows and c + 3 < cols and all(board[r + i][c + i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    player_names = ["Player " + checker for checker in player_checkers]
    turn = random.randint(0, NUM_PLAYERS - 1)
    
    # Initial print
    clear_screen()
    print_board(board)
    print(player_names[turn] + " (" + player_checkers[turn] + ") starts!")
    input("Press Enter to start...")
    
    while True:
        clear_screen()
        print_board(board)
        current_player = player_names[turn]
        current_checker = player_checkers[turn]
        print(f"{current_player} ({current_checker}), please enter a column:")

        col = get_player_input(board)
        row, _ = place_checker(board, col, current_checker)

        # Check win
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"{current_player} ({current_checker}) won!")
            break

        # Check draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Switch player
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
