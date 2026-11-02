import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # 2 players

# Initialize the game board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, etc.
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

# Check for a valid move
def is_valid_move(board, col):
    return board[0][col] == ' '

# Place a checker in the board
def place_checker(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

# Check for a win
def check_win(board, player):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check diagonal locations for win
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
        for c in range(3, COLS):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True
                
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main function to run the game
def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)

    while True:
        player = PLAYERS[current_player_index]
        column = input(f"Player {player}, please enter a column (A-G): ").upper()

        if column not in "ABCDEFG":  # Validate input
            print("Invalid input. Please enter a letter from A to G.")
            continue

        col_index = ord(column) - 65  # Convert column letter to index

        if not is_valid_move(board, col_index):
            print("Column is full! Try a different column.")
            continue
        
        place_checker(board, col_index, player)
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)  # Alternate turns

if __name__ == "__main__":
    main()
