import os
import random

# Constants
ROWS = 6
COLUMNS = 7
WINNING_LENGTH = 4
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players supported

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers A, B, C, ...
    headers = "  "
    for i in range(len(board[0])):
        headers += "  " + chr(ord('A') + i) + " "
    print(headers)

    # Print the board with horizontal separators
    sep_line = "+" + "---+" * len(board[0])
    for row in range(len(board)):
        print(sep_line)
        line = "|"
        for col in range(len(board[0])):
            line += " " + board[row][col] + " |"
        print(line)
    print(sep_line)

def is_valid_column(col_letter, cols):
    if len(col_letter) != 1:
        return False
    if not ('A' <= col_letter <= chr(ord('A') + cols -1)):
        return False
    return True

def column_to_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col_index, checker):
    # Place checker in lowest empty spot in the column
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    # Column full
    return False

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for row in range(rows):
        for col in range(cols - WINNING_LENGTH +1):
            count = 0
            for i in range(WINNING_LENGTH):
                if board[row][col+i] == checker:
                    count += 1
                else:
                    break
            if count == WINNING_LENGTH:
                return True

    # Vertical check
    for col in range(cols):
        for row in range(rows - WINNING_LENGTH +1):
            count = 0
            for i in range(WINNING_LENGTH):
                if board[row+i][col] == checker:
                    count += 1
                else:
                    break
            if count == WINNING_LENGTH:
                return True

    # Diagonal (left-top to right-bottom) check
    for row in range(rows - WINNING_LENGTH +1):
        for col in range(cols - WINNING_LENGTH +1):
            count = 0
            for i in range(WINNING_LENGTH):
                if board[row+i][col+i] == checker:
                    count += 1
                else:
                    break
            if count == WINNING_LENGTH:
                return True

    # Diagonal (left-bottom to right-top) check
    for row in range(WINNING_LENGTH -1, rows):
        for col in range(cols - WINNING_LENGTH +1):
            count = 0
            for i in range(WINNING_LENGTH):
                if board[row - i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WINNING_LENGTH:
                return True

    return False

def is_draw(board):
    # If no empty space in top row of any column -> draw
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS -1)

    while True:
        print_board(board)
        player_checker = players[current_player_index]
        print(f"Player {player_checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not is_valid_column(user_input, COLUMNS):
                print("Invalid input. Please enter a valid column letter (A-G):")
                continue
            col_idx = column_to_index(user_input)
            if board[0][col_idx] != " ":
                # Column full - lose turn
                print(f"Column {user_input} is full. You lose your turn.")
                break
            placed = place_checker(board, col_idx, player_checker)
            if not placed:
                # Should not happen since we checked above, but safe
                print(f"Column {user_input} is full. You lose your turn.")
            else:
                # Successfully placed
                break

        # Check win
        if check_winner(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        # Check draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index +1) % PLAYERS

if __name__ == "__main__":
    main()
