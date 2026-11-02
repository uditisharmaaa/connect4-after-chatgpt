import os
import random

# Constant global variables
NUM_ROWS = 6
NUM_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with all elements initialized with whitespaces"""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    print("  " + " ".join(chr(65 + i) for i in range(NUM_COLS)))
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLS + "+")

def get_valid_input(player):
    """Get a valid column input from the user"""
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if column not in [chr(65 + i) for i in range(NUM_COLS)]:
            print("Invalid input. Please enter a letter between A and G.")
        else:
            return ord(column) - 65

def place_checker(board, player, column):
    """Place a checker in the specified column"""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won"""
    # Check horizontal locations for win
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
                return True

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= " " for row in board for cell in row)

def main():
    num_players = 2
    players = CHECKERS[:num_players]
    board = create_board()
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        column = get_valid_input(current_player)
        if place_checker(board, current_player, column):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player = players[(players.index(current_player) + 1) % num_players]
        else:
            print("Invalid move. Try again.")

if __name__ == "__main__":
    main()
