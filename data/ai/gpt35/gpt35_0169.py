import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    print("+---" * COLS + "+")
    for row in board:
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
        print("+---" * COLS + "+")

def is_valid_column(col_input):
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    col = ord(col_input.upper()) - ord('A')
    if 0 <= col < COLS:
        return True
    return False

def get_column_index(col_input):
    return ord(col_input.upper()) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest available space in column col
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    # Column full
    return False

def check_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        count = 0
        for col in range(COLS):
            if board[row][col] == checker:
                count +=1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0
    # Vertical check
    for col in range(COLS):
        count = 0
        for row in range(ROWS):
            if board[row][col] == checker:
                count +=1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0
    # Diagonal (down-right) check
    for row in range(ROWS - WIN_CONDITION +1):
        for col in range(COLS - WIN_CONDITION +1):
            win = True
            for i in range(WIN_CONDITION):
                if board[row + i][col + i] != checker:
                    win = False
                    break
            if win:
                return True
    # Diagonal (up-right) check
    for row in range(WIN_CONDITION -1, ROWS):
        for col in range(COLS - WIN_CONDITION +1):
            win = True
            for i in range(WIN_CONDITION):
                if board[row - i][col + i] != checker:
                    win = False
                    break
            if win:
                return True
    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        checker = players_checkers[current_player]
        print(f"Player {checker}, please enter a column:")
        col_input = input().strip()

        if not is_valid_column(col_input):
            # Invalid input (not a letter or out of range)
            continue

        col = get_column_index(col_input)
        placed = place_checker(board, col, checker)
        if not placed:
            # Column full => lose turn
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
