import os
import random

# Constant global variables
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with the specified dimensions."""
    return [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for i, row in enumerate(board):
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    print("+---+---+---+---+---+---+---+")

def get_valid_input(player):
    """Get a valid column input from the user."""
    while True:
        column = input("Player {}, please enter a column: ".format(player))
        if column.upper() >= "A" and column.upper() <= chr(64 + BOARD_COLUMNS):
            return ord(column.upper()) - 65
        else:
            print("Invalid input. Please enter a column between A and {}.".format(chr(64 + BOARD_COLUMNS)))

def place_checker(board, player, column):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            break
    else:
        print("Column is full. Please try again.")
        return False
    return True

def check_win(board, player):
    """Check for a win condition."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True

    return False

def check_draw(board):
    """Check for a draw condition."""
    return all(cell!= " " for row in board for cell in row)

def main():
    # Create the board
    board = create_board()

    # Randomly select the first player
    players = PLAYERS_CHECKERS[:2]
    current_player = random.choice(players)

    while True:
        # Print the board
        print_board(board)

        # Get a valid input from the user
        column = get_valid_input(current_player)

        # Place the checker
        if not place_checker(board, current_player, column):
            continue

        # Check for a win
        if check_win(board, current_player):
            print_board(board)
            print("Player {} won!".format(current_player))
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
