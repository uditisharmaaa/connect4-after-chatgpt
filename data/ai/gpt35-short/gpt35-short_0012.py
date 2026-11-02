import os
import random

ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '--'*COLS + '+')

def get_valid_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_move(current_player, board):
    while True:
        move = input(f"Player {current_player}, choose column (A-G): ").upper()
        if move not in COLUMN_LABELS:
            print("Invalid column. Please select between A-G.")
            continue
        col = COLUMN_LABELS.index(move)
        if board[0][col] != ' ':
            print("Column full. Choose another column.")
            continue
        return col

def drop_piece(board, col, symbol):
    for row in reversed(range(ROWS)):
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
        count = 1  # count current piece
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_valid_num_players()
    players = PLAYER_SYMBOLS[:num_players]

    board = create_board()

    current_index = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_index]

        col = get_move(current_player, board)
        row, col = drop_piece(board, col, current_player)

        if check_win(board, current_player, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("Game ends in a draw!")
            break

        current_index = (current_index + 1) % num_players

if __name__ == "__main__":
    main()
