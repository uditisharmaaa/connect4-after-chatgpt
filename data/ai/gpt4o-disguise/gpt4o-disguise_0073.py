import os
import random

ROWS = 6
COLS = 7
NO_OF_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
CHECKERS = CHECKERS[:NO_OF_PLAYERS]

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65+i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def is_valid_input(char):
    return char.isalpha() and 'A' <= char <= chr(65 + COLS - 1)

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, player, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = CHECKERS[player]
            return

def check_direction(board, row, col, dr, dc):
    start_checker = board[row][col]
    if start_checker == ' ':
        return False

    for i in range(1, 4):
        r, c = row + i*dr, col + i*dc
        if r < 0 or r >= ROWS or c < 0 or c >= COLS or board[r][c] != start_checker:
            return False 

    return True

def check_win(board):
    for row in range(ROWS):
        for col in range(COLS):
            if (check_direction(board, row, col, 0, 1) or
                check_direction(board, row, col, 1, 0) or
                check_direction(board, row, col, 1, 1) or
                check_direction(board, row, col, 1, -1)):
                return True
    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game(board):
    player = random.randint(0, NO_OF_PLAYERS-1)
    while True:
        print_board(board)
        if check_win(board):
            print(f"Player {CHECKERS[player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        
        col = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        while not is_valid_input(col) or is_column_full(board, ord(col) - 65):
            col = input(f"Invalid input. Player {CHECKERS[player]}, please enter a column: ").strip().upper()

        place_checker(board, player, ord(col) - 65)
        player = (player + 1) % NO_OF_PLAYERS

def main():
    board = create_board()
    play_game(board)

if __name__ == "__main__":
    main()
