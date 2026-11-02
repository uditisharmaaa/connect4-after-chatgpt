import os
import random
import sys

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Change this to 2-5 to support more players (max 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players supported
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]

    # Header: column labels
    print("  " + "   ".join(letters))
    # Print the board rows with separators
    for r in range(len(board)):
        print("+" + "---+"*len(board[0]))
        print("|", end='')
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end='')
        print()
    print("+" + "---+"*len(board[0]))

def is_valid_column(input_str, columns):
    if len(input_str) != 1:
        return False
    if not ('A' <= input_str <= chr(ord('A') + columns - 1)):
        return False
    return True

def column_index_from_letter(letter):
    return ord(letter) - ord('A')

def get_lowest_empty_row(board, col):
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row == -1:
        return False
    board[row][col] = checker
    return True

def board_full(board):
    # If any cell in top row is empty, board not full
    return all(cell != ' ' for cell in board[0])

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal down-right check
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal up-right check
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def next_player_index(current_index, total_players):
    return (current_index + 1) % total_players

def main():
    if PLAYERS < 2 or PLAYERS > 5:
        print("Error: Number of players must be between 2 and 5.")
        sys.exit(1)
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS -1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "

        # Input loop for valid input
        while True:
            choice = input(prompt).strip().upper()
            if not is_valid_column(choice, COLUMNS):
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
                continue
            col = column_index_from_letter(choice)
            # Check if column full
            if get_lowest_empty_row(board, col) == -1:
                print(f"Column {choice} is full. You lose your turn!")
                break
            # Place checker
            placed = place_checker(board, col, current_checker)
            if placed:
                break
            else:
                # This should not happen because of the check above
                print(f"Cannot place checker in column {choice}. Try again.")

        # Only check win/draw if checker was actually placed
        if get_lowest_empty_row(board, col) != -1:
            if check_win(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                return
            if board_full(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                return

        # If player lost turn because column was full
        if get_lowest_empty_row(board, col) == -1:
            # turn lost, but still move to next player
            current_player_idx = next_player_index(current_player_idx, PLAYERS)
        else:
            # successful move, next turn
            current_player_idx = next_player_index(current_player_idx, PLAYERS)

if __name__ == "__main__":
    main()
