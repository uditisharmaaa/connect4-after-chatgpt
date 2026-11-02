import os
import random

# Constant variables
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to create the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for i, row in enumerate(board):
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*[cell if cell!= " " else "" for cell in row]))
    print("+---+---+---+---+---+---+---+")

# Function to get the column index from the user input
def get_column_index(column):
    return ord(column.upper()) - ord('A')

# Function to check if the column is valid
def is_valid_column(board, column):
    return board[0][column] == " "

# Function to get the next available row index in a column
def get_next_available_row(board, column):
    for i in range(ROWS - 1, -1, -1):
        if board[i][column] == " ":
            return i
    return -1

# Function to check for a win
def check_win(board, checker):
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(cell!= " " for row in board for cell in row)

# Main function
def main():
    # Create the board
    board = create_board(ROWS, COLUMNS)

    # Choose a random player to start
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        # Print the board
        print_board(board)

        # Get the current player's checker
        checker = CHECKERS[current_player]

        # Get the user input
        while True:
            column = input("Player {}, please enter a column: ".format(checker))
            if len(column) == 1 and column.isalpha():
                column_index = get_column_index(column)
                if is_valid_column(board, column_index):
                    break
            print("Invalid input. Please enter a valid column.")

        # Get the next available row index in the column
        row_index = get_next_available_row(board, column_index)
        if row_index == -1:
            print("Column is full. Please choose another column.")
            continue

        # Place the checker
        board[row_index][column_index] = checker

        # Check for a win
        if check_win(board, checker):
            print_board(board)
            print("Player {} won!".format(checker))
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
