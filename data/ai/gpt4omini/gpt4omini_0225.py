import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Players can be extended to include more characters

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def valid_input(col, board):
    if col < 0 or col >= COLS or board[0][col] != ' ':
        return False
    return True

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal matches for a win
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                if r + 3 < ROWS:
                    if all(board[r + i][c] == checker for i in range(4)):
                        return True
                    if c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                        return True
                    if c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                        return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if col_input not in [chr(65 + i) for i in range(COLS)]:
            print("Invalid input! Please choose a column between A and G.")
            continue
        
        col = ord(col_input) - 65
        
        if valid_input(col, board):
            place_checker(board, col, current_player)
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Invalid move! Try again.")
    
if __name__ == "__main__":
    main()
