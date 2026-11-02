import random
import os

ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Use first N depending on number of players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COL_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '--'*COLS + '+')

def get_player_input(player_symbol, board):
    while True:
        col = input(f"Player {player_symbol}, choose a column (A-G): ").upper()
        if col not in COL_LABELS:
            print("Invalid column. Please choose a column from A to G.")
            continue
        col_index = COL_LABELS.index(col)
        if board[0][col_index] != ' ':
            print("That column is full. Choose another one.")
            continue
        return col_index

def drop_piece(board, col, player_symbol):
    # Drop piece to the lowest empty position in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_symbol
            return row, col

def check_winner(board, player_symbol):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == player_symbol for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == player_symbol for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == player_symbol for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == player_symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    # If top row has no empty spaces, board is full
    return all(cell != ' ' for cell in board[0])

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    while True:
        try:
            num_players = int(input("Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    players = PLAYERS[:num_players]
    turn = random.randint(0, num_players-1)  # Random first player index
    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        player = players[turn]
        col = get_player_input(player, board)
        row, col = drop_piece(board, col, player)

        if check_winner(board, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        # Next player's turn
        turn = (turn + 1) % num_players

if __name__ == "__main__":
    main()
