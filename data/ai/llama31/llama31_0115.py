import os
import random
import string

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces"""
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the board with column labels and clear the screen"""
    os.system('clear')
    print("  " + " ".join(string.ascii_uppercase[:BOARD_COLS]))
    print("  " + "+---" * BOARD_COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("  " + "+---" * BOARD_COLS)

def get_player_checker(player_num):
    """Get the checker for the given player number"""
    return CHECKERS[player_num - 1]

def get_next_player(current_player):
    """Get the next player"""
    return (current_player % PLAYERS) + 1

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    return input_str.isalpha() and len(input_str) == 1 and input_str.upper() in string.ascii_uppercase[:BOARD_COLS]

def get_column_from_input(input_str):
    """Get the column number from the input string"""
    return string.ascii_uppercase.index(input_str.upper())

def is_valid_move(board, column):
    """Check if the move is valid (column not full)"""
    return board[0][column] == " "

def make_move(board, player_checker, column):
    """Make a move on the board"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player_checker
            break

def check_win(board, player_checker):
    """Check for a win"""
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row][col + 1] == player_checker and board[row][col + 2] == player_checker and board[row][col + 3] == player_checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player_checker and board[row + 1][col] == player_checker and board[row + 2][col] == player_checker and board[row + 3][col] == player_checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row + 1][col + 1] == player_checker and board[row + 2][col + 2] == player_checker and board[row + 3][col + 3] == player_checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row - 1][col + 1] == player_checker and board[row - 2][col + 2] == player_checker and board[row - 3][col + 3] == player_checker:
                return True

    return False

def check_draw(board):
    """Check for a draw"""
    return all([cell!= " " for row in board for cell in row])

def main():
    board = create_board()
    current_player = random.randint(1, PLAYERS)
    while True:
        print_board(board)
        player_checker = get_player_checker(current_player)
        input_str = input(f"Player {player_checker}, please enter a column: ")
        if not is_valid_input(input_str):
            print("Invalid input. Please try again.")
            continue
        column = get_column_from_input(input_str)
        if not is_valid_move(board, column):
            print("Column is full. Please try again.")
            continue
        make_move(board, player_checker, column)
        if check_win(board, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = get_next_player(current_player)

if __name__ == "__main__":
    main()
