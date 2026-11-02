import os
import random

# Global constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board, players):
    """Print the current state of the board"""
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(NUM_COLS)))
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('| ' + ' | '.join(cell if cell!= ' ' else '   ' for cell in row) + ' |')
    print('+---' * NUM_COLS + '+')
    print(f"Player {players[0]}, please enter a column:")

def is_valid_input(col):
    """Check if the input is a valid column letter"""
    return col.isalpha() and 'A' <= col <= chr(65 + NUM_COLS - 1)

def get_next_player(current_player, players):
    """Get the next player in the sequence"""
    return players[(players.index(current_player) + 1) % len(players)]

def is_win(board, player):
    """Check if the current player has won"""
    # Check horizontal
    for row in board:
        for col in range(NUM_COLS - 3):
            if all(cell == player for cell in row[col:col+4]):
                return True

    # Check vertical
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw"""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    num_players = 2
    players = CHECKERS[:num_players]
    current_player = random.choice(players)

    while True:
        print_board(board, players)
        col = input().upper()
        if not is_valid_input(col):
            print("Invalid input. Please enter a column letter.")
            continue

        col_index = ord(col) - 65
        for row in reversed(board):
            if row[col_index] == ' ':
                row[col_index] = current_player
                break
        else:
            print("Column is full. Please choose another column.")
            continue

        if is_win(board, current_player):
            print_board(board, players)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print_board(board, players)
            print("It's a draw!")
            break

        current_player = get_next_player(current_player, players)

if __name__ == "__main__":
    main()
