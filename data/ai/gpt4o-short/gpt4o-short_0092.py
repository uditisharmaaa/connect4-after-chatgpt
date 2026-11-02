import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
PLAYER_COUNT = 2  # Change this to the desired number of players (2 to 5)

def clear_screen():
    os.system('clear')  # For Windows, use 'cls'

def create_board():
    return [['-' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  A B C D E F G")
    for row in board:
        print(' ' + ' '.join(row))
    print()

def drop_piece(board, column, player_symbol):
    for row in reversed(board):
        if row[column] == '-':
            row[column] = player_symbol
            return True
    return False

def get_input(player_symbol):
    while True:
        try:
            column = input(f"Player {player_symbol}, choose a column (A-G): ").strip().upper()
            if column in 'ABCDEFG' and len(column) == 1:
                return ord(column) - ord('A')
            else:
                raise ValueError("Invalid Input")
        except ValueError as e:
            print("Invalid input. Please choose a column labeled A-G.")

def check_winner(board, player_symbol):
    # Check horizontal, vertical, and diagonal combinations
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col + 3 < COLUMNS and all(board[row][col + i] == player_symbol for i in range(4)):
                return True
            if row + 3 < ROWS and all(board[row + i][col] == player_symbol for i in range(4)):
                return True
            if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True
            if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == player_symbol for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != '-' for row in board for cell in row)

def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS[:PLAYER_COUNT])
    print_board(board)

    while True:
        col = get_input(current_player)
        if not drop_piece(board, col, current_player):
            print("Column full. Choose another column.")
            continue

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % PLAYER_COUNT]

if __name__ == "__main__":
    play_game()
