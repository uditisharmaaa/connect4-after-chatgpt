import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Use 'cls' on Windows
    letters = "ABCDEFG"
    print("  " + "   ".join(letters[:COLS]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")
    
def is_valid_input(col, board):
    if col >= COLS or col < 0:
        return False
    return board[0][col] == " "

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break

def check_winner(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    checkers = ["X", "O", "V", "H", "M"][:PLAYERS]
    
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    while True:
        print(f"Player {checkers[current_player]}, please enter a column:")
        col = input().strip().upper()
        if col in "ABCDEFG"[:COLS]:
            col = ord(col) - ord('A')
            if is_valid_input(col, board):
                place_checker(board, col, checkers[current_player])
                print_board(board)
                
                if check_winner(board, checkers[current_player]):
                    print(f"Player {checkers[current_player]} won!")
                    break
                if check_draw(board):
                    print("The game is a draw.")
                    break
                
                current_player = (current_player + 1) % PLAYERS
            else:
                print("Column full! You lose your turn.")
        else:
            print("Invalid input! Please enter a valid column.")
        
if __name__ == "__main__":
    main()
