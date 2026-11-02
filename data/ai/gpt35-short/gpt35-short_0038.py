import os
import random

ROWS = 6
COLS = 7
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Use first n of these players

def clear_screen():
    os.system('clear')  # For Linux/macOS, Windows would be 'cls'

def create_board():
    # Create empty board filled with spaces
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print('  ' + ' '.join(COLUMNS))
    # Print each row
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+-----------------+')

def get_player_count():
    while True:
        count = input("Enter number of players (2-5): ")
        if count.isdigit():
            count = int(count)
            if 2 <= count <= 5:
                return count
        print("Invalid input. Please enter a number from 2 to 5.")

def get_move(player):
    while True:
        move = input("Player {}'s turn. Enter column (A-G): ".format(player)).upper()
        if move in COLUMNS:
            return COLUMNS.index(move)
        print("Invalid column. Please enter a letter from A to G.")

def drop_piece(board, col, player):
    # Drop piece in the lowest empty row in the chosen column
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1  # Column is full

def check_win(board, row, col, player):
    def count_direction(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count

    # Check all directions: horizontal, vertical, two diagonals
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for dr, dc in directions:
        count = 1  # Count current piece
        count += count_direction(dr, dc)
        count += count_direction(-dr, -dc)
        if count >= 4:
            return True
    return False

def board_full(board):
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    clear_screen()
    player_count = get_player_count()
    players = PLAYERS[:player_count]
    board = create_board()
    current_player_idx = random.randint(0, player_count -1)

    while True:
        clear_screen()
        print_board(board)
        player = players[current_player_idx]

        col = get_move(player)
        row = drop_piece(board, col, player)

        if row == -1:
            print("Column full! Try a different column.")
            input("Press Enter to continue...")
            continue

        if check_win(board, row, col, player):
            clear_screen()
            print_board(board)
            print("Player {} wins! Congrats!".format(player))
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        current_player_idx = (current_player_idx + 1) % player_count

if __name__ == "__main__":
    main()
