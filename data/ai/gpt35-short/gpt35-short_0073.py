import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    # Create empty board (list of lists)
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(' '.join(COL_LABELS))
    for row in board:
        print(' '.join(row))

def get_player_count():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input, enter an integer.")

def get_move(player_marker):
    while True:
        move = input(f"Player {player_marker}, choose a column (A-G): ").upper()
        if move in COL_LABELS:
            return COL_LABELS.index(move)
        else:
            print("Invalid column. Please choose from A to G.")

def make_move(board, col, player_marker):
    # Place the marker in the lowest empty space in column
    for row in reversed(range(ROWS)):
        if board[row][col] == '.':
            board[row][col] = player_marker
            return True
    return False  # Column full

def check_winner(board, player_marker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player_marker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_marker for i in range(4)):
                return True
    
    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_marker for i in range(4)):
                return True
    
    # Check diagonal up-right
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player_marker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    # If no empty spaces ('.') in top row, it's a draw
    return all(board[0][col] != '.' for col in range(COLS))

def main():
    clear_screen()

    print("Welcome to Connect 4")
    player_count = get_player_count()
    players = PLAYER_MARKERS[:player_count]

    board = create_board()

    current_index = random.randint(0, player_count - 1)

    while True:
        clear_screen()
        print_board(board)
        player_marker = players[current_index]

        # Get valid move
        while True:
            col = get_move(player_marker)
            if make_move(board, col, player_marker):
                break
            else:
                print(f"Column {COL_LABELS[col]} is full. Choose another.")

        # Check win
        if check_winner(board, player_marker):
            clear_screen()
            print_board(board)
            print(f"Player {player_marker} wins!")
            break

        # Check draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player
        current_index = (current_index + 1) % player_count

if __name__ == "__main__":
    main()
