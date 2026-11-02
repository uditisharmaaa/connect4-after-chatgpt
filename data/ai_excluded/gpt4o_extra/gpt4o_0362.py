import os
import random

# Constants for configuration
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board with column labels
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(i + ord('A')) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Get valid input from the current player
def get_player_input(player):
    while True:
        move = input(f"Player {CHECKERS[player]}, please enter a column: ").upper()
        if move in [chr(i + ord('A')) for i in range(COLUMNS)]:
            col = ord(move) - ord('A')
            if board[0][col] == ' ':
                return col
            else:
                print("Column is full. Try another column.")
        else:
            print("Invalid input. Please enter a letter between A and", chr(ord('A') + COLUMNS - 1) + ".")

# Place the checker in the correct location
def place_checker(board, player, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = CHECKERS[player]
            return row

# Check for a win (4 in row)
def check_win(board, player, row, col):
    checker = CHECKERS[player]
    # Check horizontal
    for start in range(max(0, col-3), min(COLUMNS-3, col+1)):
        if all(board[row][c] == checker for c in range(start, start+4)):
            return True
    # Check vertical
    for start in range(max(0, row-3), min(ROWS-3, row+1)):
        if all(board[r][col] == checker for r in range(start, start+4)):
            return True
    # Check diagonal (/)
    for start in range(-3, 1):
        if row + start >= 0 and col + start >= 0 and row + start + 3 < ROWS and col + start + 3 < COLUMNS:
            if all(board[row + start + i][col + start + i] == checker for i in range(4)):
                return True
    # Check diagonal (\)
    for start in range(-3, 1):
        if row - start < ROWS and col + start >= 0 and row - start - 3 >= 0 and col + start + 3 < COLUMNS:
            if all(board[row - start - i][col + start + i] == checker for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main function that drives the game
def play_game():
    global board
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    
    print_board(board)
    
    while True:
        col = get_player_input(current_player)
        row = place_checker(board, current_player, col)
        print_board(board)
        
        if check_win(board, current_player, row, col):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS  # Switch players

# Start the game
if __name__ == "__main__":
    play_game()
