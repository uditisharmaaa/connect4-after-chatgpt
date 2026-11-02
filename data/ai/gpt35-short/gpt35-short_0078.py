import os
import random

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    # Create a ROWS x COLS board filled with spaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + ' '.join(COLUMN_LABELS))
    # Print board rows
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '--' * COLS + '+')

def get_move(player, num_players):
    while True:
        move = input(f"Player {player}'s turn. Choose column (A-G): ").strip().upper()
        if len(move) != 1 or move not in COLUMN_LABELS:
            print("Invalid input. Please enter a letter from A to G.")
            continue
        col = COLUMN_LABELS.index(move)
        return col

def is_valid_move(board, col):
    # A move is valid if the top row in that column is empty
    return board[0][col] == ' '

def make_move(board, col, player):
    # Start from bottom row and find first empty spot in column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col  # Return position where piece went
    return None  # Should not happen if move is valid

def check_winner(board, row, col, player):
    # Directions: horizontal, vertical, diagonal /, diagonal \
    directions = [
        [(0, 1), (0, -1)],   # horizontal
        [(1, 0), (-1, 0)],   # vertical
        [(1, 1), (-1, -1)],  # diagonal \
        [(1, -1), (-1, 1)]   # diagonal /
    ]

    for direction in directions:
        count = 1  # count the last played piece
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def check_draw(board):
    # If top row is full then board is full
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    # Select number of players (2-5)
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    players = PLAYER_SYMBOLS[:num_players]
    
    # Pick random player to start
    current_player_index = random.randint(0, num_players -1)
    
    board = create_board()

    while True:
        print_board(board)
        player = players[current_player_index]
        col = get_move(player, num_players)
        
        if not is_valid_move(board, col):
            print("That column is full. Try again.")
            continue

        row, col = make_move(board, col, player)
        
        if check_winner(board, row, col, player):
            print_board(board)
            print(f"Player {player} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == '__main__':
    main()
