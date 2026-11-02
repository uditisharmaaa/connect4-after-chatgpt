import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(width, height):
    """Create an empty board with the given dimensions"""
    board = [[" " for _ in range(width)] for _ in range(height)]
    return board

def print_board(board, player_turn):
    """Print the current state of the board"""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")
    print("Player {}, please enter a column:".format(CHECKERS[player_turn]))

def validate_input(board, column):
    """Check if the user input is valid"""
    if not 'A' <= column <= 'G':
        return False
    column = ord(column) - ord('A')
    for row in reversed(board):
        if row[column] == " ":
            return True
    return False

def drop_checker(board, column, checker):
    """Drop a checker in the given column"""
    column = ord(column) - ord('A')
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_win(board, player):
    """Check if the given player has won"""
    # Check horizontal locations for win
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                return True

    # Check vertical locations for win
    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_WIDTH - 3):
        for r in range(3, BOARD_HEIGHT):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
                return True

def check_draw(board):
    """Check if the game is a draw"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    num_players = 2
    players = list(range(num_players))
    random.shuffle(players)
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    current_player = 0

    while True:
        print_board(board, players[current_player])
        column = input().upper()
        while not validate_input(board, column):
            print("Invalid input, please try again.")
            column = input().upper()
        drop_checker(board, column, CHECKERS[players[current_player]])
        if check_win(board, CHECKERS[players[current_player]]):
            print_board(board, players[current_player])
            print("Player {} won!".format(CHECKERS[players[current_player]]))
            break
        if check_draw(board):
            print_board(board, players[current_player])
            print("It's a draw!")
            break
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
