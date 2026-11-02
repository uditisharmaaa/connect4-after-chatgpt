import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
MAX_COLUMNS = 26

# Initialize board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    col_labels = ' '.join(f"{chr(65 + i)}" for i in range(len(board[0])))
    print(f"  {col_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check for a win
def check_win(board, player_checker):
    def check_direction(row, col, d_row, d_col):
        count = 0
        while 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == player_checker:
            count += 1
            if count == 4:
                return True
            row += d_row
            col += d_col
        return False

    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player_checker:
                # Check all directions: right, down, diagonal down-right, diagonal down-left
                if (check_direction(row, col, 0, 1) or 
                    check_direction(row, col, 1, 0) or 
                    check_direction(row, col, 1, 1) or 
                    check_direction(row, col, 1, -1)):
                    return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Get valid column from player
def get_valid_column(board):
    while True:
        col = input("Please enter a column: ").upper()
        if len(col) == 1 and 'A' <= col <= chr(65 + COLUMNS - 1):
            column_index = ord(col) - 65
            if board[0][column_index] == " ":
                return column_index
            else:
                print("Column is full!")
        else:
            print("Invalid input!")

# Place the checker
def place_checker(board, column, player_checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player_checker
            break

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYER_COUNT - 1)
    player_checkers = PLAYER_CHECKERS[:PLAYER_COUNT]

    print_board(board)

    while True:
        print(f"Player {player_checkers[current_player]}'s turn")
        
        column_choice = get_valid_column(board)
        
        place_checker(board, column_choice, player_checkers[current_player])
        print_board(board)

        if check_win(board, player_checkers[current_player]):
            print(f"Player {player_checkers[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    play_game()
