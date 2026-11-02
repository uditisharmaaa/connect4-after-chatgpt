import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    # Print rows with separators
    for row in board:
        print("+" + "---+"*COLS)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+"*COLS)

def input_column(player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Enter a single letter.")
            continue
        if not ('A' <= col_input <= chr(ord('A') + COLS -1)):
            print("Invalid column letter. Please try again.")
            continue
        col = ord(col_input) - ord('A')
        return col

def place_checker(board, col, checker):
    # Place checker in lowest empty position in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # Column full
    return -1

def check_winner(board, row, col, checker):
    # Directions: horizontal, vertical, diag \, diag /
    directions = [
        (0,1),  # horizontal right
        (1,0),  # vertical down
        (1,1),  # diag down-right
        (1,-1)  # diag down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row+dr, col+dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS -1)
    print_board(board)
    
    while True:
        checker = players[current_player_idx]
        col = input_column(checker)
        row = place_checker(board, col, checker)
        if row == -1:
            # Column full: player loses turn
            continue
        print_board(board)
        if check_winner(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw.")
            break
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
