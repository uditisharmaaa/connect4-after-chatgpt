import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A','B','C','D','E','F','G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '--'*COLS + '+')

def get_player_count():
    while True:
        count = input("Enter number of players (2-5): ")
        if count.isdigit():
            count = int(count)
            if 2 <= count <= 5:
                return count
        print("Invalid input. Please enter a number from 2 to 5.")

def get_valid_move(board, player):
    while True:
        move = input(f"Player '{player}', choose a column (A-G): ").upper()
        if move in COLUMN_LABELS:
            col = COLUMN_LABELS.index(move)
            if board[0][col] == ' ':
                return col
            else:
                print("That column is full. Try again.")
        else:
            print("Invalid column. Please choose a letter from A to G.")

def drop_piece(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, player):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # Diagonal \ check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    # Diagonal / check
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    player_count = get_player_count()
    players = PLAYER_TOKENS[:player_count]

    board = create_board()
    current_player_index = random.randint(0, player_count -1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_index]

        col = get_valid_move(board, current_player)
        drop_piece(board, col, current_player)

        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player '{current_player}' wins! Congratulations!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        current_player_index = (current_player_index + 1) % player_count

if __name__ == "__main__":
    main()
