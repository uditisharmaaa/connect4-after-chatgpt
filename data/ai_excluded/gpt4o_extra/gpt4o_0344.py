import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Adjust checker symbols according to number of players

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(c) for c in range(ord('A'), ord('A') + COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def get_valid_input():
    while True:
        player_input = input("Please enter a column: ").strip().upper()
        if len(player_input) == 1 and 'A' <= player_input < chr(ord('A') + COLUMNS):
            return ord(player_input) - ord('A')
        else:
            print("Invalid input. Try again.")

def place_checker(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    
    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    
    return False

def board_full(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]
    print_board(board)
    
    while True:
        print(f"Player {current_checker}, it's your turn.")
        column = get_valid_input()

        if place_checker(board, column, current_checker):
            print_board(board)
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            
            if board_full(board):
                print("The game is a draw!")
                break
            
            current_player_index = (current_player_index + 1) % PLAYERS
            current_checker = CHECKERS[current_player_index]
        else:
            print(f"Column {chr(column + ord('A'))} is full. Try a different column.")

if __name__ == "__main__":
    main()
