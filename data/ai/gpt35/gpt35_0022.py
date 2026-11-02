import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # Use only first PLAYERS checkers

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers A-G
    headers = "  "
    for i in range(COLS):
        headers += "  " + chr(ord("A") + i) + " "
    print(headers)
    # Print the board with lines
    line = "+" + "---+" * COLS
    for row in range(ROWS):
        print(line)
        row_str = "|"
        for col in range(COLS):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print(line)

def valid_column_input(user_input):
    if len(user_input) != 1:
        return False
    if user_input < 'A' or user_input > chr(ord('A') + COLS - 1):
        return False
    return True

def get_column_index(user_input):
    return ord(user_input) - ord('A')

def place_checker(board, col, checker):
    # Place checker in lowest available space in the column
    # Return True if placed, False if column full
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal check (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Diagonal check (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    # If no spaces left in top row, it's a draw
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()

        # Validate input (length = 1, A-G)
        if not valid_column_input(user_input):
            # invalid input, ask again
            continue

        col = get_column_index(user_input)

        # Check if column full before placing
        if board[0][col] != " ":
            # column full, player loses turn
            # So just inform and continue with next player
            print_board(board)
            print(f"Column {user_input} is full! Player {current_checker} loses the turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        placed = place_checker(board, col, current_checker)
        print_board(board)

        if placed:
            # Check win
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            # Check draw
            if check_draw(board):
                print("The game is a draw!")
                break

            # Next turn
            current_player_index = (current_player_index + 1) % PLAYERS
        else:
            # Should never get here because we check fullness before placing,
            # but just in case:
            print(f"Cannot place checker in column {user_input}, turn lost.")
            current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
