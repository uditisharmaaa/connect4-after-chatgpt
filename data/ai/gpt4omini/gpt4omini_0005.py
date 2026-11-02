import os
import random

# Constants for board dimensions and player characters
ROWS, COLS = 6, 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1)

def find_lowest_empty_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1

def check_win(board, player):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):
                    return True
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                    return True
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player for i in range(4)):
                    return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, min(len(PLAYERS) - 1, 1))  # For 2 players only
    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col = input(f"Player {current_player}, please enter a column (A-G): ").upper()

        while not is_valid_input(col):
            col = input("Invalid input! Please enter a column (A-G): ").upper()
        
        col_index = ord(col) - 65
        row_index = find_lowest_empty_row(board, col_index)

        if row_index == -1:
            print("Column is full! Try again.")
            continue

        board[row_index][col_index] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
