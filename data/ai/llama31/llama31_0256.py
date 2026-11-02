import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def create_board():
    """Create a 2D list representing the game board"""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the game board"""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")

def get_player_order():
    """Randomly select the order of players"""
    players = CHECKERS[:NUM_PLAYERS]
    random.shuffle(players)
    return players

def is_valid_input(column):
    """Check if the user input is a valid column letter"""
    return column.upper() in "ABCDEFG"

def get_next_open_row(board, column):
    """Find the next open row in the specified column"""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return -1

def check_for_win(board, player):
    """Check for a win condition"""
    # Check horizontal locations for win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical locations for win
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def check_for_draw(board):
    """Check if the game is a draw"""
    return all(cell!= " " for row in board for cell in row)

def main():
    os.system('clear')
    board = create_board()
    players = get_player_order()
    current_player = 0

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column:")

        while True:
            column = input().strip().upper()
            if is_valid_input(column):
                column_index = ord(column) - ord("A")
                next_open_row = get_next_open_row(board, column_index)
                if next_open_row!= -1:
                    board[next_open_row][column_index] = players[current_player]
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid input. Please enter a column letter.")

        if check_for_win(board, players[current_player]):
            os.system('clear')
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        elif check_for_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
