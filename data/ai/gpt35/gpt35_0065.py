import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" " for _ in range(COLS)]
        board.append(row)
    return board

def print_board(board):
    # Print column headers
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    # Print board rows
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        line = "|"
        for col in range(COLS):
            line += " " + board[row][col] + " |"
        print(line)
    print("+" + "---+" * COLS)

def is_valid_column(letter):
    if len(letter) != 1:
        return False
    if letter < 'A' or letter >= chr(ord('A') + COLS):
        return False
    return True

def column_to_index(letter):
    return ord(letter) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # From bottom row upwards find the first empty space
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # Column full, no placement
    return -1

def check_win(board, row, col, checker):
    # Directions to check: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the placed checker itself

        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False

def is_board_full(board):
    for col in range(COLS):
        if not is_column_full(board, col):
            return False
    return True

def main():
    board = create_board()

    players = CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS -1)

    clear_screen()
    print_board(board)

    while True:
        checker = players[current_player_index]
        print(f"Player {checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not is_valid_column(user_input):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = column_to_index(user_input)
            if is_column_full(board, col):
                print("This column is full. You lose your turn.")
                break  # lose turn
            else:
                row = place_checker(board, col, checker)
                break

        clear_screen()
        print_board(board)

        if is_column_full(board, col) and row == -1:
            # lost turn already handled, skip win check and next player
            current_player_index = (current_player_index +1) % PLAYERS
            continue

        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Next player
        current_player_index = (current_player_index +1) % PLAYERS

if __name__ == "__main__":
    main()
