import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4
PLAYERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    board = []
    for _ in range(rows):
        board.append([" "] * columns)
    return board

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    # Print the board
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def is_valid_column(input_str, columns):
    if len(input_str) != 1:
        return False
    if not input_str.isalpha():
        return False
    col = ord(input_str.upper()) - ord('A')
    if col < 0 or col >= columns:
        return False
    return True

def get_column_index(input_str):
    return ord(input_str.upper()) - ord('A')

def place_checker(board, col, checker):
    # Start from bottom row and go up
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column is full
    return None, None

def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def main():
    rows = ROWS
    columns = COLUMNS
    num_players = 2
    players = PLAYERS[:num_players]

    board = create_board(rows, columns)
    current_player_index = random.randint(0, num_players -1)

    print_board(board)
    while True:
        checker = players[current_player_index]
        print("Player {}, please enter a column:".format(checker))
        player_input = input().strip()
        if not is_valid_column(player_input, columns):
            print("Invalid input! Please enter a valid column letter.")
            continue

        col = get_column_index(player_input)
        row, column = place_checker(board, col, checker)
        if row is None:
            # Column full -> lose turn
            print("Column is full! Player {} loses this turn.".format(checker))
            current_player_index = (current_player_index + 1) % num_players
            continue

        print_board(board)

        if check_win(board, row, column, checker):
            print("Player {} won!".format(checker))
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
