import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # You can modify this for more players as needed

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_column_choice(player):
    while True:
        choice = input(f"Player {player}, please enter a column (A-{chr(64 + COLUMNS)}): ").upper()
        if len(choice) != 1 or not ('A' <= choice <= chr(64 + COLUMNS)):
            print("Invalid input. Please try again.")
            continue
        col_index = ord(choice) - 65
        if board[0][col_index] != " ":
            print("Column is full! Please choose another column.")
            continue
        return col_index

def drop_checker(board, col_index, player):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = player
            return

def check_win(board, player):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == player for cell in row[col:col + 4]):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def play_connect_4():
    global board
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        col_index = get_column_choice(current_player)
        drop_checker(board, col_index, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    play_connect_4()
