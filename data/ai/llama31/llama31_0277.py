import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with the given dimensions"""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    print("  " + " ".join(string.ascii_uppercase[:NUM_COLS]))
    print("+---" * NUM_COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLS + "+")

def get_player_checker(player_num):
    """Get the checker for the given player"""
    return CHECKERS[player_num - 1]

def get_valid_move(board, player):
    """Get a valid move from the player"""
    while True:
        move = input(f"Player {get_player_checker(player)}, please enter a column: ")
        if move not in string.ascii_uppercase[:NUM_COLS]:
            print("Invalid column. Please enter a letter between A and", string.ascii_uppercase[NUM_COLS - 1])
        elif board[0][string.ascii_uppercase.index(move)]!= " ":
            print("Column is full. Please choose another column.")
        else:
            return move

def place_checker(board, move, player):
    """Place the checker in the correct location"""
    col = string.ascii_uppercase.index(move)
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = get_player_checker(player)
            return

def check_win(board, player):
    """Check if the given player has won"""
    checker = get_player_checker(player)
    # Check horizontal
    for row in board:
        for col in range(NUM_COLS - 3):
            if all([cell == checker for cell in row[col:col + 4]]):
                return True
    # Check vertical
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all([board[row + i][col] == checker for i in range(4)]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all([board[row + i][col + i] == checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all([board[row - i][col + i] == checker for i in range(4)]):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all([all([cell!= " " for cell in row]) for row in board])

def main():
    # Initialize the game
    board = create_board()
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)
    current_player = 0
    os.system('clear')
    print_board(board)

    # Game loop
    while True:
        player = players[current_player]
        move = get_valid_move(board, player)
        place_checker(board, move, player)
        os.system('clear')
        print_board(board)
        if check_win(board, player):
            print(f"Player {get_player_checker(player)} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
