import os
import random

# Constant global variables
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces"""
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the board with column labels"""
    print("  A B C D E F G")
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")

def validate_input(input_str):
    """Validate user input"""
    if len(input_str)!= 1:
        return False
    if input_str.upper() not in [chr(65 + i) for i in range(BOARD_COLS)]:
        return False
    return True

def get_player_checker(player_num):
    """Get the checker for a given player number"""
    return CHECKERS[player_num - 1]

def place_checker(board, player_num, col):
    """Place a checker on the board"""
    checker = get_player_checker(player_num)
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return

def check_win(board, player_num):
    """Check for a win"""
    checker = get_player_checker(player_num)
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Check for a draw"""
    for row in board:
        if " " in row:
            return False
    return True

def game():
    """Main game loop"""
    board = create_board()
    num_players = 2
    players = list(range(1, num_players + 1))
    current_player = random.choice(players)
    while True:
        os.system('clear')
        print_board(board)
        print("Player", get_player_checker(current_player), "turn")
        while True:
            col_str = input("Enter column (A-G): ")
            if validate_input(col_str):
                col = ord(col_str.upper()) - 65
                if board[0][col]!= " ":
                    print("Column is full, try again.")
                else:
                    place_checker(board, current_player, col)
                    break
            else:
                print("Invalid input, try again.")
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print("Player", get_player_checker(current_player), "won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player % num_players) + 1

if __name__ == "__main__":
    game()
