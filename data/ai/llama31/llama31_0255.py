import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
PLAYERS = 2

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a new board with the specified dimensions"""
    return [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("+---" * BOARD_WIDTH + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_WIDTH + "+")

def is_valid_input(input_str, board):
    """Check if the input is a valid column letter"""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    col = ord(input_str.upper()) - ord('A')
    if col < 0 or col >= BOARD_WIDTH:
        return False
    if board[0][col]!= " ":
        return False
    return True

def get_player_move(player, board):
    """Get the player's move and validate it"""
    while True:
        move = input(f"Player {player}, please enter a column: ")
        if is_valid_input(move, board):
            return ord(move.upper()) - ord('A')
        print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    """Place a checker in the specified column"""
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return

def check_win(board, checker):
    """Check if the current player has won"""
    # Check horizontal locations for win
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(3, BOARD_HEIGHT):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    while True:
        print_board(board)
        print(f"Current player: {current_player}")
        col = get_player_move(current_player, board)
        place_checker(board, col, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
