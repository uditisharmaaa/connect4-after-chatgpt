import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---+" + "---+" * (COLUMNS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLUMNS - 1))

def get_valid_input(player):
    while True:
        col = input(f"Player {player}, please enter a column (A-{chr(65+COLUMNS-1)}): ").upper()
        if len(col) == 1 and 'A' <= col <= chr(65 + COLUMNS - 1):
            col_index = ord(col) - 65
            if board[0][col_index] == " ":
                return col_index
            else:
                print("Column is full. Please try again.")
        else:
            print("Invalid input. Please choose a valid column.")

def place_checker(col_index, player):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = player
            return True
    return False

def check_win(player):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c <= COLUMNS - 4 and all(board[r][c + i] == player for i in range(4))) or \
               (r <= ROWS - 4 and all(board[r + i][c] == player for i in range(4))) or \
               (r <= ROWS - 4 and c <= COLUMNS - 4 and all(board[r + i][c + i] == player for i in range(4))) or \
               (r >= 3 and c <= COLUMNS - 4 and all(board[r - i][c + i] == player for i in range(4))):
                return True
    return False

def check_draw():
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    random_player = random.choice(PLAYERS[:2])
    current_player = random_player
    print_board()

    while True:
        col_index = get_valid_input(current_player)
        place_checker(col_index, current_player)

        if check_win(current_player):
            print_board()
            print(f"Player {current_player} won!")
            break
        
        if check_draw():
            print_board()
            print("The game is a draw!")
            break

        print_board()
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
