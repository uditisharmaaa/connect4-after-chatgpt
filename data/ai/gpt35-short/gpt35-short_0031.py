import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print('  ' + ' '.join(COLUMN_LABELS))
    # Print each row
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '--' * COLUMNS + '+')

def get_num_players():
    while True:
        try:
            n = int(input(f"Enter number of players (2-{len(PLAYER_SYMBOLS)}): "))
            if 2 <= n <= len(PLAYER_SYMBOLS):
                return n
            else:
                print(f"Please enter a number between 2 and {len(PLAYER_SYMBOLS)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_move(player):
    while True:
        move = input(f"Player {player}, choose a column (A-G): ").strip().upper()
        if move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print(f"Invalid column. Please choose from {', '.join(COLUMN_LABELS)}.")

def is_valid_move(board, col):
    return board[0][col] == ' '

def apply_move(board, col, symbol):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col

def check_win(board, symbol, row, col):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        [(0, 1), (0, -1)],  # horizontal
        [(1, 0), (-1, 0)],  # vertical
        [(1, 1), (-1, -1)], # diagonal \
        [(1, -1), (-1, 1)]  # diagonal /
    ]
    for direction in directions:
        count = 1
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    turn = random.randint(0, num_players -1)
    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        current_player = players[turn]
        col = get_move(current_player)
        if not is_valid_move(board, col):
            print("Column full. Try again.")
            input("Press Enter to continue...")
            continue
        row, col_played = apply_move(board, col, current_player)
        if check_win(board, current_player, row, col_played):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break
        turn = (turn + 1) % num_players

if __name__ == "__main__":
    main()
