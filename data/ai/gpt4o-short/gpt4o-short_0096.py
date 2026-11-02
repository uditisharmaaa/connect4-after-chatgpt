import os
import random

# Constants
NUM_PLAYERS = 2      # Can be 2, 3, 4, or 5
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMNS = 7
ROWS = 6

def clear_screen():
    os.system('clear')  # Use 'cls' on Windows

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print("\n  A B C D E F G")
    for row in board:
        print("|" + "|".join(row) + "|")
    print("---------------")

def get_player_move(player):
    while True:
        move = input(f"Player {player}, choose a column (A-G): ").upper()
        if move in "ABCDEFG" and len(move) == 1:
            col = ord(move) - ord('A')
            if any(row[col] == ' ' for row in board):
                return col
            else:
                print("Column is full! Choose another column.")
        else:
            print("Invalid input! Please enter a column letter between A and G.")

def make_move(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

def is_winner(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    while True:
        clear_screen()
        print_board(board)
        print(f"It's {current_player}'s turn.")
        col = get_player_move(current_player)
        make_move(board, col, current_player)

        if is_winner(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_player_index + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
