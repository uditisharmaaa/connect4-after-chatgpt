import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    # Print each row with separators
    for row in range(ROWS):
        print("+" + "---+"*COLS)
        row_str = "|"
        for col in range(COLS):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print("+" + "---+"*COLS)

def input_column(player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single uppercase letter.")
            continue
        if not ('A' <= col_input <= chr(ord('A') + COLS - 1)):
            print("Invalid column letter. Please try again.")
            continue
        col = ord(col_input) - ord('A')
        return col

def place_checker(board, col, checker):
    # From bottom row to top, find empty spot in col
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    # Column full
    return -1

def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0,1),  # horizontal right
        (1,0),  # vertical down
        (1,1),  # diagonal down-right
        (1,-1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS -1)
    print_board(board)
    
    while True:
        checker = players[current_player_index]
        col = input_column(checker)
        row_placed = place_checker(board, col, checker)
        if row_placed == -1:
            print("Column full. You lose your turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, row_placed, col, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
