import os
import random

ROWS, COLS = 6, 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  '.join(COLUMN_LABELS))
    for row in board:
        print(' | '.join(row))
        print("-" * 29)

def is_valid_move(board, col):
    return board[0][col] == ' '

def drop_piece(board, col, piece):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = piece
            break

def check_win(board, piece):
    # Check horizontal, vertical and diagonal (both directions) for a connect 4
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS[:NUM_PLAYERS])
    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_player}'s turn")
        move = input(f"Choose column (A-G): ").strip().upper()
        if move in COLUMN_LABELS:
            col = COLUMN_LABELS.index(move)
            if is_valid_move(board, col):
                drop_piece(board, col, current_player)
                if check_win(board, current_player):
                    print_board(board)
                    print(f"Player {current_player} wins!")
                    game_over = True
                elif is_draw(board):
                    print_board(board)
                    print("It's a draw!")
                    game_over = True
                else:
                    # Switch to the next player
                    player_index = (PLAYERS.index(current_player) + 1) % NUM_PLAYERS
                    current_player = PLAYERS[player_index]
            else:
                print("Column is full! Try again.")
        else:
            print("Invalid input. Choose a column between A-G.")

if __name__ == "__main__":
    main()
