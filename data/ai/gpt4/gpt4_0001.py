import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players supported

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "  # Check if the column is not full

def drop_checker(board, column, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return

def check_winner(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def board_full(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)  # Randomly select first player
    
    while True:
        print_board(board)
        print(f"Player {players[current_player]}'s turn")
        
        # Input validation
        while True:
            column_input = input("Please enter a column (A-G): ").strip().upper()
            if len(column_input) != 1 or not column_input.isalpha():
                print("Invalid input. Please enter a valid column letter.")
                continue
            column = ord(column_input) - ord('A')
            if not is_valid_column(column, board):
                print("Invalid column or column is full. Try again.")
                continue
            break
        
        # Drop checker
        drop_checker(board, column, players[current_player])
        
        # Check for a winner
        if check_winner(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        
        # Check for a draw
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
