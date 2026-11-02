import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the given dimensions"""
    return [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player):
    """Get the checker for the given player"""
    return CHECKERS[player - 1]

def get_column_index(column):
    """Get the column index from the column letter"""
    return ord(column) - ord('A')

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    return len(input_str) == 1 and 'A' <= input_str <= 'G'

def is_valid_move(board, column):
    """Check if the move is valid (column is not full)"""
    return board[0][column] == " "

def place_checker(board, column, checker):
    """Place the checker in the lowest available space in the column"""
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            break

def check_win(board, checker):
    """Check if the given player has won"""
    # Check horizontal locations for win
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_WIDTH):
        for row in range(BOARD_HEIGHT - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw"""
    return all([cell!= " " for row in board for cell in row])

def main():
    board = create_board()
    print_board(board)
    player = random.randint(1, NUM_PLAYERS)
    while True:
        print("Player " + get_player_checker(player) + "'s turn")
        column = input("Enter a column (A-G): ").upper()
        while not is_valid_input(column) or not is_valid_move(board, get_column_index(column)):
            if not is_valid_input(column):
                print("Invalid input. Please enter a column letter (A-G).")
            else:
                print("Column is full. Please choose another column.")
            column = input("Enter a column (A-G): ").upper()
        place_checker(board, get_column_index(column), get_player_checker(player))
        print_board(board)
        if check_win(board, get_player_checker(player)):
            print("Player " + get_player_checker(player) + " won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        player = (player % NUM_PLAYERS) + 1

if __name__ == "__main__":
    main()
