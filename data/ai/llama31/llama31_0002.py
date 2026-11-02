import os
import random

# Constants for the game
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a new Connect 4 board with the given dimensions"""
    board = []
    for _ in range(BOARD_ROWS):
        row = [" "] * BOARD_COLS
        board.append(row)
    return board

def print_board(board, player):
    """Print the current state of the board"""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")
    print(f"Player {player}, please enter a column:")

def validate_input(input_str):
    """Validate the user's input"""
    if len(input_str)!= 1:
        return False
    if not input_str.isalpha():
        return False
    if not 'A' <= input_str.upper() <= chr(65 + BOARD_COLS - 1):
        return False
    return True

def get_column_index(input_str):
    """Get the column index from the user's input"""
    return ord(input_str.upper()) - 65

def place_checker(board, player, column_index):
    """Place a checker on the board at the specified column"""
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = player
            break

def check_win(board, player):
    """Check for a win in the given board"""
    # Check horizontal locations for win
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == player and row[col + 1] == player and row[col + 2] == player and row[col + 3] == player:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

def check_draw(board):
    """Check for a draw in the given board"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def game():
    """Run the Connect 4 game"""
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    while True:
        print_board(board, current_player)
        input_str = input().upper()
        while not validate_input(input_str):
            print("Invalid input. Please enter a column letter.")
            input_str = input().upper()
        column_index = get_column_index(input_str)
        for row in reversed(board):
            if row[column_index] == " ":
                place_checker(board, current_player, column_index)
                break
        else:
            print("Column is full. Please choose another column.")
            continue
        if check_win(board, current_player):
            print_board(board, current_player)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board, current_player)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    game()
