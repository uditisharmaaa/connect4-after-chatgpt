import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    # Board initialized with spaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print('  ' + ' '.join(COL_LABELS))
    # Print each row
    for r in range(ROWS):
        print(str(ROWS - r) + ' ' + ' '.join(board[r]))
    print()

def get_num_players():
    while True:
        try:
            n = int(input(f"Enter number of players (2 to {len(PLAYER_TOKENS)}): "))
            if 2 <= n <= len(PLAYER_TOKENS):
                return n
            else:
                print(f"Please enter a number between 2 and {len(PLAYER_TOKENS)}.")
        except ValueError:
            print("Invalid input. Enter an integer.")

def get_move(player_token, board):
    while True:
        col = input(f"Player {player_token}, choose a column (A-G): ").upper()
        if col not in COL_LABELS:
            print("Invalid column. Choose a letter from A to G.")
            continue
        col_index = COL_LABELS.index(col)
        if board[0][col_index] != ' ':
            print("Column is full. Pick another one.")
            continue
        return col_index

def make_move(board, col, player_token):
    # Place token in lowest available row in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_token
            return row, col

def check_win(board, row, col, player_token):
    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal right down
        (1, -1),  # diagonal left down
    ]
    for dr, dc in directions:
        count = 1  # count player token itself
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    # If top row has no empty space, board is full
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYER_TOKENS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        player_token = players[current_player_index]
        col = get_move(player_token, board)
        row, col = make_move(board, col, player_token)

        if check_win(board, row, col, player_token):
            clear_screen()
            print_board(board)
            print(f"Player {player_token} wins! Congratulations!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
