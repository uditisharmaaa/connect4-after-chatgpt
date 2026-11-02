import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can add more players like ['X', 'O', 'V', 'H', 'M'] for more than 2 players

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Printing column labels
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def get_valid_input(player):
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(move) == 1 and 'A' <= move <= chr(65 + COLS - 1):
            return ord(move) - 65  # convert 'A', 'B', etc. to index 0, 1, ...
        else:
            print("Invalid input. Please enter a valid column letter.")

def drop_piece(board, col, piece):
    for row in reversed(board):  # Start from the bottom row
        if row[col] == " ":
            row[col] = piece
            return True
    return False

def check_winner(board, piece):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == piece for cell in row[col:col + 4]):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == piece for i in range(4)):
                return True
    
    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True
    
    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        col = get_valid_input(current_player)
        if drop_piece(board, col, current_player):
            print_board(board)
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            # Switch player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full, please choose another column")

if __name__ == "__main__":
    main()
