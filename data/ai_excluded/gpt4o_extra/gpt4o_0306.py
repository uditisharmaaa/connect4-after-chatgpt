import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Check if the input is valid
def valid_input(input_str, board):
    if len(input_str) != 1 or not input_str.isalpha():
        return False

    col = ord(input_str.upper()) - 65
    if col < 0 or col >= COLUMNS or board[0][col] != " ":
        return False

    return True

# Place the checker in the chosen column
def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

# Check for a win
def check_winner(board, player):
    def check_line(start_row, start_col, delta_row, delta_col):
        row, col = start_row, start_col
        count = 0
        while 0 <= row < ROWS and 0 <= col < COLUMNS:
            if board[row][col] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            row += delta_row
            col += delta_col
        return False

    # Check horizontal, vertical, and both diagonals
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (check_line(r, c, 0, 1) or  # Horizontal 
                check_line(r, c, 1, 0) or  # Vertical
                check_line(r, c, 1, 1) or  # Diagonal down-right
                check_line(r, c, 1, -1)):  # Diagonal down-left
                return True
    return False

# Check for a draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main game function
def connect_4_game():
    players = 2
    current_player_idx = random.randint(0, players - 1)
    board = create_board(ROWS, COLUMNS)

    print_board(board)
    
    while True:
        player_letter = PLAYER_SYMBOLS[current_player_idx]
        print(f"Player {player_letter}, please enter a column:")

        user_input = input().strip().upper()
        
        if not valid_input(user_input, board):
            print("Invalid input. Please try again.")
            continue

        column_index = ord(user_input) - 65
        
        if not place_checker(board, column_index, player_letter):
            print("Column full. Try a different column.")
            continue

        print_board(board)

        if check_winner(board, player_letter):
            print(f"Player {player_letter} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch players
        current_player_idx = (current_player_idx + 1) % players

# Run the game
if __name__ == "__main__":
    connect_4_game()
