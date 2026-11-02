import random
import os

# Global constants
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = ["X", "O"]  # You can extend the list to ["X", "O", "V", "H", "M"] for 5 players

# Initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the game board
def print_board(board):
    os.system('clear')
    header = "  " + "   ".join([chr(65 + i) for i in range(len(board[0]))])
    print(header)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# Check if the move is valid
def is_valid_move(board, col):
    return 0 <= col < len(board[0]) and board[0][col] == " "

# Place the checker
def place_checker(board, col, checker):
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            break

# Check for a win
def check_win(board, checker):
    # Check horizontal locations
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical locations
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            if board[row][col] == checker and all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonals (\)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonals (/)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Connect 4 game logic
def play_game():
    board = create_board(ROWS, COLS)
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        move_valid = False
        while not move_valid:
            col_input = input().strip()
            if len(col_input) == 1 and col_input.isalpha():
                col = ord(col_input.upper()) - ord('A')
                if is_valid_move(board, col):
                    place_checker(board, col, current_player)
                    move_valid = True
                else:
                    print("Invalid move. Try again:")
            else:
                print("Invalid input. Try again:")

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        else:
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_game()
