import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Add more player symbols if needed

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    while True:
        column = input(f"Player {player}, please enter a column (A-G): ").upper()
        if column in [chr(65 + i) for i in range(COLS)]:
            return ord(column) - 65
        else:
            print("Invalid input. Please enter a letter from A to G.")

def place_checker(board, column, player):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                # Check horizontal
                if col + 3 < COLS and all(board[row][col + i] == player for i in range(4)):
                    return True
                # Check vertical
                if row + 3 < ROWS and all(board[row + i][col] == player for i in range(4)):
                    return True
                # Check diagonal (down-right)
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == player for i in range(4)):
                    return True
                # Check diagonal (up-right)
                if row - 3 >= 0 and col + 3 < COLS and all(board[row - i][col + i] == player for i in range(4)):
                    return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        
        column = get_valid_input(current_player)
        if not place_checker(board, column, current_player):
            print("Column full. Try another column.")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
