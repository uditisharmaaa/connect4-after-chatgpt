import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    letters = [chr(ord('A')+i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def is_valid_col(col_letter):
    return col_letter.isalpha() and col_letter in [chr(ord('A')+i) for i in range(COLS)]

def col_to_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # full column

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # diagonal down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        checker = players[current]
        move = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not is_valid_col(move):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = col_to_index(move)
        if not place_checker(board, col, checker):
            # full column - lose turn
            print(f"Column {move} is full. Player {checker} loses this turn.")
        else:
            print_board(board)
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
