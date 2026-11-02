import os
import random

COLS = 7
ROWS = 6
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def init_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(c+65) for c in range(COLS)))
    print('+---' * COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLS + '+')

def drop_checker(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

def check_win(board, player):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if c <= COLS - 4 and all(board[r][c+i] == player for i in range(4)):
                    return True
                if r <= ROWS - 4 and all(board[r+i][c] == player for i in range(4)):
                    return True
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r+i][c+i] == player for i in range(4)):
                    return True
                if r >= 3 and c <= COLS - 4 and all(board[r-i][c+i] == player for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = init_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player_char = PLAYERS[current_player]
        print(f"Player {player_char}, please enter a column:")

        while True:
            try:
                col = input().strip().upper()
                col_idx = ord(col) - 65
                if col_idx < 0 or col_idx >= COLS:
                    raise ValueError("Invalid column")
                valid_move = drop_checker(board, col_idx, player_char)
                if not valid_move:
                    raise ValueError("Column full")
                break
            except ValueError as e:
                print(e)
        
        print_board(board)
        
        if check_win(board, player_char):
            print(f"Player {player_char} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
