import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def clear_screen():
    os.system('clear')


def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board


def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(COLUMNS)]
    print("  " + "   ".join(letters))
    # Print board rows with formatting
    for row in range(ROWS):
        print("+" + "---+" * COLUMNS)
        line = "|"
        for col in range(COLUMNS):
            line += " " + board[row][col] + " |"
        print(line)
    print("+" + "---+" * COLUMNS)


def valid_column_input(user_input):
    if len(user_input) != 1:
        return False
    c = user_input[0]
    return 'A' <= c <= chr(ord('A') + COLUMNS - 1)


def column_index(letter):
    return ord(letter) - ord('A')


def place_checker(board, col, checker):
    # Place checker at the lowest empty row in column col
    # Return True if placed successfully, False if column full
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def is_winning_move(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row][col+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row+i][col] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Check diagonal down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row+i][col+i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Check diagonal up-right
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row - i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    return False


def is_board_full(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True


def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = players_checkers[current_player_idx]
        player_prompt = f"Player {checker}, please enter a column: "

        # Input validation loop
        while True:
            user_input = input(player_prompt).strip().upper()
            if not valid_column_input(user_input):
                # Invalid column letter
                continue
            col = column_index(user_input)
            # Check if column full
            if board[0][col] != " ":  # top row is occupied full => column full
                # Player loses turn if column full (no retry)
                placed = False
                break
            # Otherwise, place checker
            placed = place_checker(board, col, checker)
            if placed:
                break

        print_board(board)

        if placed:
            # Check win
            if is_winning_move(board, checker):
                print(f"Player {checker} won!")
                break
            # Check draw
            if is_board_full(board):
                print("Game is a draw!")
                break
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
