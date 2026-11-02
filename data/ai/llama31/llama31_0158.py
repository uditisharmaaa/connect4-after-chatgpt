import os
import random

# Global constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = 2

# Create the game board
board = [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board():
    # Clear the game screen
    os.system('clear')
    
    # Print column labels
    print("  A   B   C   D   E   F   G")
    print("+---+---+---+---+---+---+---+")
    
    # Print the game board
    for row in board:
        print("|   |   |   |   |   |   |   |")
        print("+---+---+---+---+---+---+---+")
        print("|", end=" ")
        for cell in row:
            print(cell, end=" | ")
        print()
        print("+---+---+---+---+---+---+---+")

def get_player_checker(player_number):
    return CHECKERS[player_number - 1]

def is_valid_move(column):
    if column < 0 or column >= BOARD_WIDTH:
        return False
    return board[0][column] == " "

def get_lowest_empty_row(column):
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return -1

def place_checker(player_number, column):
    row = get_lowest_empty_row(column)
    if row == -1:
        return False
    board[row][column] = get_player_checker(player_number)
    return True

def check_for_win(player_number):
    checker = get_player_checker(player_number)
    
    # Check horizontal wins
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    
    # Check vertical wins
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    
    return False

def is_board_full():
    return all(cell!= " " for row in board for cell in row)

# Choose a random first player
current_player = random.randint(1, PLAYERS)

# Print the initial board
print_board()

while True:
    # Ask for the player's move
    print(f"Player {get_player_checker(current_player)}, please enter a column (A-{chr(65 + BOARD_WIDTH - 1)}):")
    column = input().upper()
    column = ord(column) - 65
    
    # Check if the move is valid
    if not is_valid_move(column):
        print("Invalid move, try again.")
        continue
    
    # Place the checker
    if not place_checker(current_player, column):
        print("Column is full, try again.")
        continue
    
    # Print the updated board
    print_board()
    
    # Check for a win
    if check_for_win(current_player):
        print(f"Player {get_player_checker(current_player)} won!")
        break
    
    # Check for a draw
    if is_board_full():
        print("It's a draw!")
        break
    
    # Switch to the next player
    current_player = (current_player % PLAYERS) + 1
