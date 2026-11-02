import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
TOTAL_TO_WIN = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    column_labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_valid_input(board):
    columns = len(board[0])
    while True:
        player_input = input("Please enter a column (A-G): ").strip().upper()
        if len(player_input) == 1 and 'A' <= player_input < chr(65 + columns):
            col_index = ord(player_input) - 65
            if board[0][col_index] == " ":
                return col_index
            else:
                print("Column is full, try a different one.")
        else:
            print("Invalid input. Please try again.")

def place_checker(board, col, symbol):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col

def check_winner(board, row, col, symbol):
    directions = [(-1, 0), (0, 1), (-1, 1), (-1, -1)]  # vertical, horizontal, diagonals
    for dr, dc in directions:
        count = 1
        for sign in (-1, 1):  # Check both directions in this line
            r, c = row, col
            while True:
                r += sign * dr
                c += sign * dc
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
                    count += 1
                else:
                    break
        if count >= TOTAL_TO_WIN:
            return True
    return False

def check_draw(board):
    return all(cell != " " for cell in board[0])

def main():
    # Initialization
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Constant defined in the assignment
    players = PLAYER_SYMBOLS[:num_players]
    current_player = random.choice(players)
    
    clear_screen()
    print_board(board)
    print(f"Randomly selected first player: Player {current_player}")

    # Game loop
    while True:
        print(f"Player {current_player}'s turn.")
        col = get_valid_input(board)
        row, col = place_checker(board, col, current_player)
        
        clear_screen()
        print_board(board)
        
        if check_winner(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == '__main__':
    main()
