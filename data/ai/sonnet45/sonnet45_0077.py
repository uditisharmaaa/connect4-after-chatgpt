import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+" + "---+" * COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    # Horizontal
    for c in range(max(0, col - 3), min(COLS - 3, col + 1)):
        if all(board[row][c + i] == checker for i in range(4)):
            return True
    
    # Vertical
    for r in range(max(0, row - 3), min(ROWS - 3, row + 1)):
        if all(board[r + i][col] == checker for i in range(4)):
            return True
    
    # Diagonal (down-right)
    for offset in range(-3, 1):
        r, c = row + offset, col + offset
        if 0 <= r <= ROWS - 4 and 0 <= c <= COLS - 4:
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Diagonal (up-right)
    for offset in range(-3, 1):
        r, c = row - offset, col + offset
        if 3 <= r < ROWS and 0 <= c <= COLS - 4:
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def get_valid_input(board):
    while True:
        user_input = input().strip()
        if len(user_input) == 1 and user_input.isalpha():
            col = ord(user_input.upper()) - 65
            if 0 <= col < COLS:
                if is_valid_move(board, col):
                    return col
                else:
                    print("Column is full. Please enter another column:")
            else:
                print(f"Please enter a column between A and {chr(64 + COLS)}:")
        else:
            print("Invalid input. Please enter a column letter:")

def main():
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        
        col = get_valid_input(board)
        row = place_checker(board, col, current_checker)
        
        print_board(board)
        
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
