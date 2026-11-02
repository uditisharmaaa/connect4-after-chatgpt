import os
import random

ROWS = 6
COLS = 7
COL_LABELS = "A B C D E F G".split()
PLAYER_PIECES = ['X', 'O', 'V', 'H', 'M']  # up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(COL_LABELS))
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("-" * (COLS * 4 + 1))

def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 2 and 5.")

def get_player_move(player_piece):
    while True:
        move = input(f"Player {player_piece}, choose a column (A-G): ").strip().upper()
        if move in COL_LABELS:
            col = COL_LABELS.index(move)
            return col
        else:
            print("Invalid column. Please choose between A-G.")

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, piece):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row, col
    return None  # just a fallback; should never be called when checked first

def check_direction(board, start_row, start_col, delta_row, delta_col, piece):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == piece:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, piece):
    # Check all directions for 4 in a row:
    # horizontal (0,1), vertical (1,0), diagonal down-right (1,1), diagonal down-left (1,-1)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # count pieces in both directions
        count = 1  # count the piece just placed
        count += check_direction(board, row - dr, col - dc, -dr, -dc, piece)
        count += check_direction(board, row + dr, col + dc, dr, dc, piece)
        if count >=4:
            return True
    return False

def is_draw(board):
    # No spaces in top row means board full (since pieces stack from bottom)
    return all(cell != ' ' for cell in board[0])

def main():
    num_players = get_num_players()
    players = PLAYER_PIECES[:num_players]
    current_player_idx = random.randint(0, num_players - 1)

    board = create_board()
    print_board(board)
    print(f"Player {players[current_player_idx]} starts first!")
    
    while True:
        piece = players[current_player_idx]
        col = get_player_move(piece)
        if not is_valid_move(board, col):
            print("That column is full. Try another one.")
            continue

        row, col = make_move(board, col, piece)
        print_board(board)

        if check_win(board, row, col, piece):
            print(f"Player {piece} wins! 🎉")
            break
        if is_draw(board):
            print("The game is a draw! No more moves possible.")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
