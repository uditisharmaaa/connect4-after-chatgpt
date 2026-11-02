import random
import os

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"] # Up to 5 players

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print('  ' + '   '.join(chr(i + ord('A')) for i in range(COLUMNS)))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

# Function to create the initial board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to switch players
def switch_player(current, players_count):
    return (current + 1) % players_count

# Function to check for win condition
def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

# Function to check for draw condition
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Function to place the checker on the board
def place_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

# Function to get valid column input from a player
def get_user_input():
    while True:
        column_input = input("Please enter a column: ").strip().upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + COLUMNS - 1):
            return ord(column_input) - ord('A')
        print("Invalid input. Please enter a valid column letter.")

# Main function to start the game
def start_game():
    board = create_board()
    current_player = random.choice(range(PLAYERS_COUNT))
    print_board(board)

    while True:
        current_checker = PLAYER_CHECKERS[current_player]
        print(f"Player {current_checker}, it's your turn.")
        column = get_user_input()

        if place_checker(board, column, current_checker):
            print_board(board)
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = switch_player(current_player, PLAYERS_COUNT)
        else:
            print(f"Column {chr(column + ord('A'))} is full. Turn lost.")

if __name__ == "__main__":
    start_game()
