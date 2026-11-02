import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    # Print board rows
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("| " + " | ".join(board[row]) + " |")
    print("+" + "---+" * COLS)

def get_player_input(player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ")
        if len(inp) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        col_letter = inp.upper()
        if not ('A' <= col_letter <= chr(ord('A') + COLS -1)):
            print("Invalid column. Please enter a valid column letter.")
            continue
        col = ord(col_letter) - ord('A')
        return col

def place_checker(board, col, checker):
    # place checker in the lowest available position in col
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    # column full
    return False

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # vertical check
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # diagonal check (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True
    # diagonal check (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True
    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    checkers = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    while True:
        print_board(board)
        player_checker = checkers[current_player_index]
        col = get_player_input(player_checker)
        valid_move = place_checker(board, col, player_checker)
        if not valid_move:
            print(f"Column {chr(ord('A')+col)} is full. You lose your turn.")
        else:
            if check_win(board, player_checker):
                print_board(board)
                print(f"Player {player_checker} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
