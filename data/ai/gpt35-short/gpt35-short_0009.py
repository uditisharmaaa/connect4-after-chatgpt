import os
import random

ROWS = 6
COLS = 7
COLUMNS_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Players allowed from 2 to 5
PLAYERS_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print(' ' + ' '.join(COLUMNS_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2 * COLS + 1))

def get_player_count():
    while True:
        try:
            count = int(input("Enter number of players (2-5): "))
            if 2 <= count <= 5:
                return count
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_player_move(player_symbol):
    while True:
        move = input(f"Player {player_symbol}, choose a column (A-G): ").upper()
        if move in COLUMNS_LABELS:
            col = COLUMNS_LABELS.index(move)
            return col
        else:
            print("Invalid column. Please choose a column between A and G.")

def make_move(board, col, player_symbol):
    # Place piece in lowest empty spot in column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player_symbol
            return row
    return -1  # Column full

def check_winner(board, player_symbol, row, col):
    # Check all directions: horizontal, vertical, diagonal \, diagonal /
    
    def count_in_direction(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        return count

    # Horizontal
    total = 1 + count_in_direction(0, -1) + count_in_direction(0, 1)
    if total >= 4:
        return True
    # Vertical
    total = 1 + count_in_direction(-1, 0) + count_in_direction(1, 0)
    if total >= 4:
        return True
    # Diagonal \ 
    total = 1 + count_in_direction(-1, -1) + count_in_direction(1, 1)
    if total >= 4:
        return True
    # Diagonal /
    total = 1 + count_in_direction(-1, 1) + count_in_direction(1, -1)
    if total >= 4:
        return True

    return False

def is_draw(board):
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    player_count = get_player_count()
    players = PLAYERS_SYMBOLS[:player_count]
    current_player_index = random.randint(0, player_count - 1)

    board = create_board()

    while True:
        print_board(board)
        player_symbol = players[current_player_index]
        col = get_player_move(player_symbol)

        row = make_move(board, col, player_symbol)
        if row == -1:
            print("That column is full. Try again.")
            continue

        if check_winner(board, player_symbol, row, col):
            print_board(board)
            print(f"Player {player_symbol} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % player_count

if __name__ == "__main__":
    main()
