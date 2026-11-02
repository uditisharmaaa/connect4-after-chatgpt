import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty board with the given dimensions"""
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")

def get_player_input(player):
    """Get the player's input and validate it"""
    while True:
        col = input(f"Player {player}, please enter a column: ")
        if len(col)!= 1 or not col.isalpha() or col.upper() < 'A' or col.upper() > chr(65 + NUM_COLS - 1):
            print("Invalid input. Please enter a letter between A and", chr(65 + NUM_COLS - 1))
        else:
            return ord(col.upper()) - 65

def place_checker(board, col, player):
    """Place the player's checker in the given column"""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return

def check_win(board, player):
    """Check if the player has won"""
    # Check horizontal wins
    for row in board:
        for col in range(NUM_COLS - 3):
            if row[col] == player and row[col + 1] == player and row[col + 2] == player and row[col + 3] == player:
                return True

    # Check vertical wins
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= " " for row in board for cell in row)

def main():
    # Create the board
    board = create_board()

    # Choose a random player to start
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    # Game loop
    while True:
        print_board(board)
        col = get_player_input(current_player)
        place_checker(board, col, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
