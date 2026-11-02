import os
import random

ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Constants for players
PLAYERS_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for __ in range(ROWS)]

def print_board(board):
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2*COLS + 1))

def get_player_count():
    while True:
        try:
            n = int(input(f'Enter number of players (2-5): '))
            if 2 <= n <= 5:
                return n
            else:
                print('Number of players must be between 2 and 5.')
        except ValueError:
            print('Invalid input. Please enter a number between 2 and 5.')

def get_move(player_symbol):
    while True:
        move = input(f"Player {player_symbol}, choose a column (A-G): ").upper()
        if move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print("Invalid column. Please enter a letter from A to G.")

def make_move(board, col, player_symbol):
    # Place the player's symbol in the lowest empty spot in the column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player_symbol
            return row, col
    return None  # Column full

def is_winning_move(board, row, col, symbol):
    # Check all directions: horizontal, vertical, diagonal (/ and \)
    def count_direction(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        return count

    # Check horizontally
    total = 1 + count_direction(0, 1) + count_direction(0, -1)
    if total >= 4:
        return True

    # Check vertically
    total = 1 + count_direction(1, 0) + count_direction(-1, 0)
    if total >= 4:
        return True

    # Check diagonal /
    total = 1 + count_direction(-1, 1) + count_direction(1, -1)
    if total >= 4:
        return True

    # Check diagonal \
    total = 1 + count_direction(1, 1) + count_direction(-1, -1)
    if total >= 4:
        return True

    return False

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    num_players = get_player_count()
    players = PLAYERS_SYMBOLS[:num_players]

    current_player_index = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn.")
        col = get_move(players[current_player_index])
        move_pos = make_move(board, col, players[current_player_index])
        if move_pos is None:
            print("That column is full. Try again.")
            input("Press Enter to continue...")
            continue

        row, col = move_pos
        if is_winning_move(board, row, col, players[current_player_index]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player_index]} wins! Congratulations!")
            break

        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
