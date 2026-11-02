import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for i in range(COLUMNS):
        header += " " + chr(ord('A') + i) + "  "
    print(header)
    # Print the board with separators
    for row in range(ROWS):
        line = "+"
        for _ in range(COLUMNS):
            line += "---+"
        print(line)
        row_line = "|"
        for col in range(COLUMNS):
            row_line += " " + board[row][col] + " |"
        print(row_line)
    print("+" + "---+" * COLUMNS)

def get_player_input(player_checker, board):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        col = ord(user_input) - ord('A')
        if col < 0 or col >= COLUMNS:
            print("Invalid column. Please enter a valid column letter.")
            continue
        # Check if column is full
        if board[0][col] != " ":
            # Turn is lost if column full, so notify and return None
            print("Column is full. You lose your turn.")
            return None
        return col

def place_checker(board, col, checker):
    # Place from bottom up
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None, None  # shouldn't happen if checked before

def check_win(board, last_row, last_col, checker):
    # Directions vectors: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # count the last checker itself
        # check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check in negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    # If top row has any empty cell, not draw
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS-1)

    print_board(board)

    while True:
        checker = players_checkers[current_player]
        col = get_player_input(checker, board)
        if col is None:
            # player lost turn due to full column
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue
        row, col = place_checker(board, col, checker)
        print_board(board)

        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
