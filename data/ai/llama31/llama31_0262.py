import os
import random

# Global variables
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with specified dimensions."""
    board = [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("|", end=" ")
        for cell in row:
            print(cell, end=" | ")
        print()
    print("+---+---+---+---+---+---+---+")

def validate_input(column):
    """Validate user input."""
    if len(column)!= 1 or not column.isalpha() or not "A" <= column <= "G":
        return False
    return True

def place_checker(board, column, checker):
    """Place a checker in the specified column."""
    column_index = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return

def check_win(board, checker):
    """Check for a win in all directions."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True

    # Check vertical
    for col in range(BOARD_COLUMNS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == checker and board[i+1][col] == checker and board[i+2][col] == checker and board[i+3][col] == checker:
                return True

    # Check positive diagonal
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Check negative diagonal
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    os.system('clear')
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        print("Player", players[current_player_index], "please enter a column:")
        column = input().strip().upper()
        if not validate_input(column):
            print("Invalid input. Please try again.")
            continue
        place_checker(board, column, players[current_player_index])
        if check_win(board, players[current_player_index]):
            print_board(board)
            print("Player", players[current_player_index], "won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
