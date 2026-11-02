import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("Connect 4")
    print("Players:", ' '.join(PLAYERS[:num_players]))
    print("  " + ' '.join(COLUMN_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+-' * COLS + '+')

def get_valid_column(board, player):
    while True:
        move = input(f"Player {player}, choose a column (A-G): ").strip().upper()
        if move in COLUMN_LABELS:
            col = COLUMN_LABELS.index(move)
            if board[0][col] == ' ':
                return col
            else:
                print("Column is full! Try again.")
        else:
            print("Invalid input. Enter a column letter A-G.")

def drop_piece(board, col, player):
    # Drop from bottom up
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_win(board, player):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def get_number_of_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number from 2 to 5.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def main():
    global num_players
    num_players = get_number_of_players()
    players = PLAYERS[:num_players]
    board = create_board()
    current_player_index = random.randint(0, num_players -1)

    while True:
        print_board(board)
        player = players[current_player_index]
        col = get_valid_column(board, player)
        drop_piece(board, col, player)

        if check_win(board, player):
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
