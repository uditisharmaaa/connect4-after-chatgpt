import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("\n  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_move(column_letter, board):
    # Check if the input is valid
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    column = ord(column_letter) - ord('A')
    if column < 0 or column >= COLUMNS:
        return False
    if board[0][column] != ' ':
        return False
    return True

def make_move(player_symbol, column_letter, board):
    column = ord(column_letter) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player_symbol
            break

def check_winner(board):
    # Check horizontal, vertical, and diagonal (both directions) for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == ' ':
                continue
            if col + 3 < COLUMNS and all(board[row][col + i] == board[row][col] for i in range(4)):
                return True
            if row + 3 < ROWS and all(board[row + i][col] == board[row][col] for i in range(4)):
                return True
            if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == board[row][col] for i in range(4)):
                return True
            if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == board[row][col] for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    player_count = 2  # Change as needed, but max 5
    players = PLAYERS_SYMBOLS[:player_count]
    current_player_index = random.randint(0, player_count - 1)
    print_board(board)

    while True:
        current_player = players[current_player_index]
        move = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        if is_valid_move(move, board):
            make_move(current_player, move, board)
            print_board(board)
            if check_winner(board):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % player_count
        else:
            print("Invalid move. Please try again.")

if __name__ == "__main__":
    main()
