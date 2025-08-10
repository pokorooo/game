import random
import copy


class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
    def is_valid(self, board, row, col, num):
        """指定した位置に数字を置けるかチェック"""
        # 行をチェック
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # 列をチェック  
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # 3x3ボックスをチェック
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def solve_board(self, board):
        """バックトラッキングでナンプレを解く"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.solve_board(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    def generate_complete_board(self):
        """完全なナンプレ盤を生成"""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # 対角線上の3x3ボックスから埋める
        self.fill_diagonal()
        
        # 残りを埋める
        self.solve_board(self.board)
        
        return self.board
    
    def fill_diagonal(self):
        """対角線上の3x3ボックスを埋める"""
        for box in range(0, 9, 3):
            self.fill_box(box, box)
    
    def fill_box(self, row, col):
        """3x3ボックスをランダムな数字で埋める"""
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = numbers.pop()


class SudokuPuzzle:
    def __init__(self):
        self.generator = SudokuGenerator()
        self.complete_board = None
        self.puzzle_board = None
        self.user_board = None
        
    def create_puzzle(self, difficulty="medium"):
        """問題を作成"""
        # 完全な盤面を生成
        self.complete_board = self.generator.generate_complete_board()
        
        # コピーを作成して問題用にする
        self.puzzle_board = copy.deepcopy(self.complete_board)
        
        # 難易度に応じてセルを消去
        cells_to_remove = self.get_cells_to_remove(difficulty)
        self.remove_cells(cells_to_remove)
        
        # ユーザー解答用の盤面を初期化
        self.user_board = copy.deepcopy(self.puzzle_board)
        
        return self.puzzle_board
    
    def get_cells_to_remove(self, difficulty):
        """難易度に応じて消すセル数を決定"""
        difficulty_levels = {
            "easy": 30,     # 30個のセルを消去
            "medium": 45,   # 45個のセルを消去
            "hard": 55      # 55個のセルを消去
        }
        return difficulty_levels.get(difficulty, 45)
    
    def remove_cells(self, cells_to_remove):
        """指定した数のセルをランダムに消去"""
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        for i in range(cells_to_remove):
            row, col = positions[i]
            self.puzzle_board[row][col] = 0
    
    def display_board(self, board=None):
        """盤面を表示"""
        if board is None:
            board = self.user_board
            
        print("\n  " + " ".join([str(i) for i in range(1, 10)]))
        print("  " + "-" * 17)
        
        for i in range(9):
            row_str = str(i + 1) + "|"
            for j in range(9):
                if board[i][j] == 0:
                    row_str += "."
                else:
                    row_str += str(board[i][j])
                
                if j < 8:
                    if (j + 1) % 3 == 0:
                        row_str += "|"
                    else:
                        row_str += " "
            
            print(row_str)
            
            if i < 8 and (i + 1) % 3 == 0:
                print("  " + "-" * 17)
    
    def make_move(self, row, col, num):
        """ユーザーの手を盤面に反映"""
        if 1 <= row <= 9 and 1 <= col <= 9 and 1 <= num <= 9:
            # 元の問題で埋められているセルは変更できない
            if self.puzzle_board[row-1][col-1] != 0:
                return False, "このセルは変更できません"
            
            self.user_board[row-1][col-1] = num
            return True, "手が記録されました"
        else:
            return False, "無効な入力です"
    
    def clear_cell(self, row, col):
        """セルをクリア"""
        if 1 <= row <= 9 and 1 <= col <= 9:
            # 元の問題で埋められているセルは変更できない
            if self.puzzle_board[row-1][col-1] != 0:
                return False, "このセルは変更できません"
            
            self.user_board[row-1][col-1] = 0
            return True, "セルがクリアされました"
        else:
            return False, "無効な入力です"
    
    def check_solution(self):
        """解答をチェック"""
        # 空欄があるかチェック
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] == 0:
                    return False, "まだ空欄があります"
        
        # 完全解答と比較
        if self.user_board == self.complete_board:
            return True, "正解です！おめでとうございます！"
        else:
            return False, "間違いがあります。再度確認してください。"
    
    def get_hint(self):
        """ヒントを提供"""
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            correct_num = self.complete_board[row][col]
            return f"ヒント: 行{row+1}, 列{col+1}に{correct_num}が入ります"
        else:
            return "ヒントは不要です - 盤面が埋まっています"