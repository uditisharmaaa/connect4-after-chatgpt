import os
import random

# CONSTANTS
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for c in range(len(board[0])):
        header += "  " + chr(ord('A') + c) + " "
    print(header)
    # Print each row with separators
    for r in range(len(board)):
        print("+" + "---+" * len(board[0]))
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * len(board[0]))

def valid_column_input(user_input, cols):
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col_index = ord(user_input.upper()) - ord('A')
    if 0 <= col_index < cols:
        return True
    return False

def find_row_to_place(board, col):
    # Start from bottom row and find first empty space
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r + i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r - i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    return False

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    player_order = list(range(PLAYERS))
    random.shuffle(player_order)  # Randomize starting player order
    current_index = 0  # index in player_order

    print_board(board)
    print(f"Player {CHECKERS[player_order[current_index]]} starts first.")

    while True:
        current_player = player_order[current_index]
        checker = CHECKERS[current_player]

        # Ask for input until valid (column A-G and not full, except turn loss case)
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            if not valid_column_input(user_input, COLS):
                continue  # Invalid input, ask again
            col = ord(user_input) - ord('A')
            row = find_row_to_place(board, col)
            if row == -1:
                # Column full - player loses turn, move to next player
                print(f"Column {user_input} is full. Player {checker} loses turn.")
                valid_input = True  # end this turn with loss
                row = -1
            else:
                valid_input = True  # valid input and column not full

        if row != -1:
            board[row][col] = checker
            print_board(board)

            # Check for a win
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break

            # Check for draw
            if board_full(board):
                print("The game is a draw!")
                break
        else:
            # Column full and player lost their turn, print board anyway
            print_board(board)

        # Next player's turn
        current_index = (current_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
