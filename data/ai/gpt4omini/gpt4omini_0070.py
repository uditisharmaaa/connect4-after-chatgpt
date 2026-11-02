import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
WINNING_LENGTH = 4

# Function to create an empty board
def create_board():
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    return board

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column headers
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

# Function to check if the input is valid
def is_valid_input(column, board):
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < COLS and board[0][col_index] == ' '

# Function to place a checker in the board
def place_checker(board, column, player):
    col_index = ord(column.upper()) - 65
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return True
    return False

# Function to check for a win
def check_win(board, player):
    # Check horizontal, vertical and diagonal directions
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                if check_direction(board, row, col, player, 1, 0) or \
                   check_direction(board, row, col, player, 0, 1) or \
                   check_direction(board, row, col, player, 1, 1) or \
                   check_direction(board, row, col, player, 1, -1):
                    return True
    return False

# Helper function to check specific direction
def check_direction(board, row, col, player, d_row, d_col):
    count = 0
    for _ in range(WINNING_LENGTH):
        if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == player:
            count += 1
        else:
            break
        row += d_row
        col += d_col
    return count == WINNING_LENGTH

# Function to check for a draw
def check_draw(board):
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

# Main function to play the game
def play_game():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    while not game_over:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        column = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        while not is_valid_input(column, board):
            print("Invalid input. Please enter a valid column.")
            column = input(f"Player {current_player}, please enter a column: ").strip().upper()

        placed = place_checker(board, column, current_player)
        if not placed:
            print("Column is full. You lose your turn.")
        else:
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    play_game()
