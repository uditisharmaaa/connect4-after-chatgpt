import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LETTERS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    print(" ", end="")
    for letter in COLUMN_LETTERS:
        print(f"  {letter} ", end="")
    print()
    # Print separator line
    print("+" + "---+" * COLS)
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * COLS)

def get_valid_input(current_player):
    while True:
        player_checker = CHECKERS[current_player]
        choice = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(choice) != 1:
            continue
        choice = choice.upper()
        if choice in COLUMN_LETTERS:
            col_index = COLUMN_LETTERS.index(choice)
            return col_index
        # invalid input, ask again
        

def place_checker(board, col, checker):
    # Place checker in lowest available row in that column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    # Column full
    return False

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r][c + i] == checker:
                    count +=1
                else:
                    break
            if count == WIN_COUNT:
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c] == checker:
                    count +=1
                else:
                    break
            if count == WIN_COUNT:
                return True
    # Check diagonal down-right
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c + i] == checker:
                    count +=1
                else:
                    break
            if count == WIN_COUNT:
                return True
    # Check diagonal up-right
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r - i][c + i] == checker:
                    count +=1
                else:
                    break
            if count == WIN_COUNT:
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
    current_player = random.randint(0, PLAYERS -1)
    print_board(board)
    
    while True:
        col = get_valid_input(current_player)
        placed = place_checker(board, col, CHECKERS[current_player])
        if not placed:
            # Turn lost if column is full
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
