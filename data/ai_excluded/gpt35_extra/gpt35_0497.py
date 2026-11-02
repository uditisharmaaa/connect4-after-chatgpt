import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLUMNS)
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = ""
    for i in range(COLUMNS):
        labels += "  " + chr(ord("A") + i) + " "
    print(labels)
    # Print board rows with separators
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        line = ""
        for col in range(COLUMNS):
            line += "| " + board[row][col] + " "
        line += "|"
        print(line)
    print("+---" * COLUMNS + "+")

def input_valid_column(input_str):
    if len(input_str) != 1:
        return False
    c = input_str[0]
    if c < 'A' or c >= chr(ord('A') + COLUMNS):
        return False
    return True

def column_index(column_char):
    return ord(column_char) - ord("A")

def place_checker(board, col, checker):
    # Place checker in the lowest available row in col
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - (WIN_LENGTH -1)):
            count = 0
            for offset in range(WIN_LENGTH):
                if board[row][col+offset] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - (WIN_LENGTH -1)):
            count = 0
            for offset in range(WIN_LENGTH):
                if board[row+offset][col] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True
    # Diagonal down-right check
    for row in range(ROWS - (WIN_LENGTH -1)):
        for col in range(COLUMNS - (WIN_LENGTH -1)):
            count = 0
            for offset in range(WIN_LENGTH):
                if board[row+offset][col+offset] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True
    # Diagonal up-right check
    for row in range(WIN_LENGTH -1, ROWS):
        for col in range(COLUMNS - (WIN_LENGTH -1)):
            count = 0
            for offset in range(WIN_LENGTH):
                if board[row - offset][col + offset] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True
    return False

def board_full(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_index]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip().upper()
            if not input_valid_column(user_input):
                continue
            col = column_index(user_input)
            if col < 0 or col >= COLUMNS:
                continue
            if board[0][col] != " ":
                # Column full, player loses turn
                break
            if place_checker(board, col, checker):
                break
            else:
                # Column full, player loses turn
                break

        print_board(board)

        if board[0][col] == checker:  # If checker was placed successfully
            if check_win(board, checker):
                print(f"Player {checker} won!")
                return
        if board_full(board):
            print("The game is a draw.")
            return

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
