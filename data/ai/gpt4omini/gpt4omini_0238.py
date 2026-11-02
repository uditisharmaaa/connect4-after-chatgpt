import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # Can expand to ["X", "O", "V", "H", "M"] for more players

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for a win
def check_win(board, player):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                # Check horizontally
                if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check vertically
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check diagonally (down-right)
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check diagonally (down-left)
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == player for i in range(4)):
                    return True
    return False

# Check for a draw
def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Place checker in the specified column
def place_checker(board, column, player):
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = player
            return True
    return False

# Main game loop
def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    player = PLAYERS[current_player_index]
    
    print_board(board)

    while True:
        valid_input = False
        while not valid_input:
            column_input = input(f"Player {player}, please enter a column (A-G): ").upper()
            if len(column_input) != 1 or column_input < 'A' or column_input > chr(65 + COLS - 1):
                print("Invalid input. Please enter a letter from A to " + chr(65 + COLS - 1) + ".")
                continue
            
            column = ord(column_input) - 65  # Convert A-G to 0-6
            if not place_checker(board, column, player):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True

        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)
        player = PLAYERS[current_player_index]

if __name__ == "__main__":
    main()
