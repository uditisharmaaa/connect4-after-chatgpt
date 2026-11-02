import os
import random

# Constant global variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces"""
    board = []
    for _ in range(BOARD_ROWS):
        row = [" "] * BOARD_COLS
        board.append(row)
    return board

def print_board(board):
    """Print the board with column labels and clear screen"""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")

def get_player_checker(player):
    """Return the checker for the given player"""
    return CHECKERS[player]

def get_next_player(current_player):
    """Return the next player"""
    return (current_player + 1) % NUM_PLAYERS

def is_valid_input(column):
    """Check if the input is a valid column label"""
    return column.upper() >= "A" and column.upper() <= chr(65 + BOARD_COLS - 1)

def get_column_from_input(input_str):
    """Convert the input string to a column index"""
    return ord(input_str.upper()) - 65

def is_valid_turn(board, column):
    """Check if the turn is valid (column is not full)"""
    return board[0][column] == " "

def place_checker(board, player, column):
    """Place the checker at the correct location"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = get_player_checker(player)
            return

def check_win(board, player):
    """Check if the player has won"""
    checker = get_player_checker(player)

    # Check horizontal
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all(all(cell!= " " for cell in row) for row in board)

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {get_player_checker(current_player)}, please enter a column:")

        while True:
            column = input().strip()
            if is_valid_input(column):
                column = get_column_from_input(column)
                if is_valid_turn(board, column):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a column label.")

        place_checker(board, current_player, column)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {get_player_checker(current_player)} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = get_next_player(current_player)

if __name__ == "__main__":
    main()
