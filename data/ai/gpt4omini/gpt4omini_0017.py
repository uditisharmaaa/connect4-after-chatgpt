import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # You can change this for more players; e.g., ["X", "O", "V", "H", "M"]

# Function to create the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the console (Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Function to check for a win
def check_win(board, player):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical win
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal win (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal win (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        valid_input = False

        while not valid_input:
            user_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()

            if len(user_input) == 1 and 'A' <= user_input <= chr(65 + COLS - 1):
                column = ord(user_input) - 65  # Convert column letter to index
                if board[0][column] == " ":
                    for row in range(ROWS - 1, -1, -1):  # Start from the bottom of the column
                        if board[row][column] == " ":
                            board[row][column] = current_player
                            valid_input = True
                            break
                else:
                    print("Column is full, try again.")
            else:
                print("Invalid input, try again.")

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch to the next player

if __name__ == "__main__":
    main()
