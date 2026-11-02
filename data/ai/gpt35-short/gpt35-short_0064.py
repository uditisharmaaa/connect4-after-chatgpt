import os
import random

ROWS = 6
COLS = 7
COL_LABELS = 'ABCDEFG'
TOKENS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(' ' + ' '.join(COL_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (COLS * 2 + 1))

def get_valid_num_players():
    while True:
        n = input("Enter number of players (2-5): ")
        if n.isdigit():
            n = int(n)
            if 2 <= n <= 5:
                return n
        print("Invalid input, please enter an integer between 2 and 5.")

def get_move(player_token, board):
    while True:
        move = input(f"Player {player_token}, choose a column (A-G): ").upper()
        if move in COL_LABELS:
            col = COL_LABELS.index(move)
            if board[0][col] == ' ':
                return col
            else:
                print("That column is full, try again.")
        else:
            print("Invalid column, please enter A through G.")

def make_move(board, col, token):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = token
            return row

def check_win(board, row, col, token):
    # Check directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check forward
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        # Check backward
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def play_game():
    clear_screen()
    num_players = get_valid_num_players()
    players = TOKENS[:num_players]
    board = create_board()
    current_player_index = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player order: {' '.join(players)}")
        current_token = players[current_player_index]

        col = get_move(current_token, board)
        row = make_move(board, col, current_token)

        if check_win(board, row, col, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins! Congratulations!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == '__main__':
    play_game()
