import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+' + '+'.join(['---'] * COLS) + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '+'.join(['---'] * COLS) + '+')

def get_valid_move(board, player):
    while True:
        try:
            col = input(f"Player {player}, please enter a column: ").upper()
            if len(col) != 1 or col < 'A' or col >= chr(65 + COLS):
                raise ValueError("Invalid column.")
            col_idx = ord(col) - 65
            if board[0][col_idx] != ' ':
                print("Column is full. Try another.")
                continue
            return col_idx
        except ValueError:
            print("Invalid input. Enter a column letter (e.g., A, B, C).")

def place_checker(board, col_idx, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = player
            return row
    return -1

def check_win(board, row, col):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    player = board[row][col]
    for dr, dc in directions:
        count = 1
        for step in (1, -1):
            r, c = row + step * dr, col + step * dc
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                r += step * dr
                c += step * dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board()
    current_player = random.choice(CHECKERS)
    print_board(board)
    
    while True:
        col_idx = get_valid_move(board, current_player)
        row = place_checker(board, col_idx, current_player)
        print_board(board)
        if check_win(board, row, col_idx):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("Game ended in a draw!")
            break
        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
