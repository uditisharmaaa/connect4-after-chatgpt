import os
import random

ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']  # 2 to 5 players

def clear_screen():
    os.system('clear')  # Use 'cls' instead of 'clear' if on Windows

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLS * 2 + 1))

def get_player_input(player_mark):
    while True:
        col = input(f"Player {player_mark}, pick a column (A-G): ").upper()
        if col in COL_LABELS:
            col_idx = COL_LABELS.index(col)
            return col_idx
        else:
            print("Invalid input. Please pick a column from A to G.")

def drop_piece(board, col, player_mark):
    # Drop piece into the lowest empty row in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_mark
            return row
    return -1  # Column full

def check_win(board, row, col, player_mark):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        [(0,1),(0,-1)],  # horizontal
        [(1,0),(-1,0)],  # vertical
        [(1,1),(-1,-1)], # diagonal \
        [(1,-1),(-1,1)]  # diagonal /
    ]

    for direction in directions:
        count = 1  # count current piece
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_mark:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Please enter a valid number.")

    player_marks = PLAYER_MARKS[:num_players]

    board = create_board()
    current_player_index = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        player_mark = player_marks[current_player_index]

        # Get valid column input and drop piece
        while True:
            col = get_player_input(player_mark)
            row = drop_piece(board, col, player_mark)
            if row != -1:
                break
            else:
                print("That column is full. Try another one.")

        # Check for win
        if check_win(board, row, col, player_mark):
            clear_screen()
            print_board(board)
            print(f"Player {player_mark} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == '__main__':
    main()
