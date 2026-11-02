import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
CONNECT_NUM = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLUMNS)
    return board

def print_board(board):
    clear_screen()
    # print column headers
    header = "  "
    for i in range(COLUMNS):
        header += chr(ord('A') + i) + "   "
    print(header)

    # print each row with separators
    for r in range(ROWS):
        print("+---" * COLUMNS + "+")
        row_str = "|"
        for c in range(COLUMNS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+---" * COLUMNS + "+")

def get_valid_column(board, player):
    valid_columns = [chr(ord('A') + i) for i in range(COLUMNS)]
    while True:
        inp = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Invalid input. Enter a single letter.")
            continue
        if inp not in valid_columns:
            print("Invalid column letter. Choose from:", ", ".join(valid_columns))
            continue
        col = ord(inp) - ord('A')
        # check if column is full
        if board[0][col] != " ":
            print(f"Column {inp} is full. You lose your turn.")
            return -1
        return col

def place_checker(board, col, checker):
    # Place checker in lowest empty row of column col
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - CONNECT_NUM + 1):
            count = 0
            for i in range(CONNECT_NUM):
                if board[r][c+i] == checker:
                    count += 1
                else:
                    break
            if count == CONNECT_NUM:
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - CONNECT_NUM + 1):
            count = 0
            for i in range(CONNECT_NUM):
                if board[r+i][c] == checker:
                    count += 1
                else:
                    break
            if count == CONNECT_NUM:
                return True

    # Check diagonal down-right
    for r in range(ROWS - CONNECT_NUM + 1):
        for c in range(COLUMNS - CONNECT_NUM + 1):
            count = 0
            for i in range(CONNECT_NUM):
                if board[r+i][c+i] == checker:
                    count += 1
                else:
                    break
            if count == CONNECT_NUM:
                return True

    # Check diagonal down-left
    for r in range(ROWS - CONNECT_NUM + 1):
        for c in range(CONNECT_NUM - 1, COLUMNS):
            count = 0
            for i in range(CONNECT_NUM):
                if board[r+i][c-i] == checker:
                    count += 1
                else:
                    break
            if count == CONNECT_NUM:
                return True

    return False

def check_draw(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    current_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        player = players[current_index]
        col = get_valid_column(board, player)
        if col == -1:
            # full column - lose turn
            current_index = (current_index + 1) % PLAYERS
            print_board(board)
            continue

        place_checker(board, col, player)
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_index = (current_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
