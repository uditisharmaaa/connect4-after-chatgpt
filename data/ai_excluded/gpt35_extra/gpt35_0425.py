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
    headers = "  "
    for i in range(COLUMNS):
        headers += chr(ord('A') + i) + "   "
    print(headers)
    # Print rows and separating lines
    for row in range(ROWS):
        line = "+"
        for _ in range(COLUMNS):
            line += "---+"
        print(line)

        row_str = "|"
        for col in range(COLUMNS):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    # Last line after last row
    line = "+"
    for _ in range(COLUMNS):
        line += "---+"
    print(line)

def valid_column_input(col_input, board):
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    col = ord(col_input.upper()) - ord('A')
    if col < 0 or col >= COLUMNS:
        return False
    # If column is full, invalid input here would mean player loses turn (handled separately)
    return True

def column_full(board, col):
    # If top row in column is occupied, column is full
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in lowest empty space in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column full

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == checker and
                board[row][col+1] == checker and
                board[row][col+2] == checker and
                board[row][col+3] == checker):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if (board[row][col] == checker and
                board[row+1][col] == checker and
                board[row+2][col] == checker and
                board[row+3][col] == checker):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if (board[row][col] == checker and
                board[row+1][col+1] == checker and
                board[row+2][col+2] == checker and
                board[row+3][col+3] == checker):
                return True
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if (board[row][col] == checker and
                board[row+1][col-1] == checker and
                board[row+2][col-2] == checker and
                board[row+3][col-3] == checker):
                return True
    return False

def board_full(board):
    for col in range(COLUMNS):
        if not column_full(board, col):
            return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]

    current_player_idx = random.randint(0, PLAYERS -1)
    while True:
        print_board(board)
        print(f"Player {players_checkers[current_player_idx]}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not valid_column_input(user_input, board):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = ord(user_input) - ord('A')
            if column_full(board, col):
                # Player loses turn if column full
                print("Column is full. You lose your turn.")
                break
            else:
                pos = place_checker(board, col, players_checkers[current_player_idx])
                break

        if not column_full(board, col):
            # Only check win/draw if a checker was placed
            if check_win(board, players_checkers[current_player_idx]):
                print_board(board)
                print(f"Player {players_checkers[current_player_idx]} won!")
                return
            if board_full(board):
                print_board(board)
                print("The game is a draw!")
                return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
