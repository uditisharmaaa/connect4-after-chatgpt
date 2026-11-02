import os
import random

# Constant global variables
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create an empty board with the given dimensions"""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the board"""
    print('  ' + ' '.join(chr(65 + i) for i in range(BOARD_WIDTH)))
    for row in board:
        print('+---' * BOARD_WIDTH + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_WIDTH + '+')

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    return len(input_str) == 1 and 'A' <= input_str <= 'Z' and ord(input_str) - 65 < BOARD_WIDTH

def get_player_move(player_checker):
    """Get the player's move (column letter) and validate it"""
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").upper()
        if is_valid_input(move):
            return ord(move) - 65
        print("Invalid input. Please try again.")

def place_checker(board, player_checker, column):
    """Place the player's checker in the given column"""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_checker
            return

def check_win(board, player_checker):
    """Check if the player has won (4 checkers in a row)"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == player_checker for cell in row[i:i+4]]):
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == player_checker for row in range(i, i+4)]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == player_checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == player_checker for i in range(4)]):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)"""
    return all([cell!= ' ' for row in board for cell in row])

def game():
    """Main game loop"""
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    os.system('clear')
    print_board(board)
    while True:
        column = get_player_move(current_player)
        place_checker(board, current_player, column)
        os.system('clear')
        print_board(board)
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    game()
