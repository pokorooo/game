from flask import Flask, render_template, jsonify, request, session, Blueprint
import sys
import os
import uuid
import random
import copy

# Vercel用のシンプルなパス設定
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

app = Flask(__name__, 
           template_folder=os.path.join(parent_dir, 'templates'),
           static_folder=os.path.join(parent_dir, 'static'))

app.secret_key = os.environ.get('SECRET_KEY', 'vercel-sudoku-secret-key-2024')

# 数独クラスを直接定義（import問題を回避）
class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
    def is_valid(self, board, row, col, num):
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
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_diagonal()
        self.solve_board(self.board)
        return self.board
    
    def fill_diagonal(self):
        for box in range(0, 9, 3):
            self.fill_box(box, box)
    
    def fill_box(self, row, col):
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
        self.complete_board = self.generator.generate_complete_board()
        self.puzzle_board = copy.deepcopy(self.complete_board)
        
        cells_to_remove = self.get_cells_to_remove(difficulty)
        self.remove_cells(cells_to_remove)
        
        self.user_board = copy.deepcopy(self.puzzle_board)
        return self.puzzle_board
    
    def get_cells_to_remove(self, difficulty):
        difficulty_levels = {
            "easy": 30,
            "medium": 45,
            "hard": 55
        }
        return difficulty_levels.get(difficulty, 45)
    
    def remove_cells(self, cells_to_remove):
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        for i in range(cells_to_remove):
            row, col = positions[i]
            self.puzzle_board[row][col] = 0
    
    def make_move(self, row, col, num):
        if 1 <= row <= 9 and 1 <= col <= 9 and 1 <= num <= 9:
            if self.puzzle_board[row-1][col-1] != 0:
                return False, "このセルは変更できません"
            
            self.user_board[row-1][col-1] = num
            return True, "手が記録されました"
        else:
            return False, "無効な入力です"
    
    def clear_cell(self, row, col):
        if 1 <= row <= 9 and 1 <= col <= 9:
            if self.puzzle_board[row-1][col-1] != 0:
                return False, "このセルは変更できません"
            
            self.user_board[row-1][col-1] = 0
            return True, "セルがクリアされました"
        else:
            return False, "無効な入力です"
    
    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] == 0:
                    return False, "まだ空欄があります"
        
        if self.user_board == self.complete_board:
            return True, "正解です！おめでとうございます！"
        else:
            return False, "間違いがあります。再度確認してください。"
    
    def get_hint(self):
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

# ゲームセッションを保存する辞書（Vercelの制約により簡易実装）
games = {}

# Blueprint for /game prefix
game_bp = Blueprint('game', __name__, url_prefix='/game')

@game_bp.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')

@game_bp.route('/new_game', methods=['POST'])
def new_game():
    """新しいゲームを開始"""
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'medium')
        
        # 新しいパズルを作成
        puzzle = SudokuPuzzle()
        puzzle.create_puzzle(difficulty)
        
        # ゲームIDを生成
        game_id = str(uuid.uuid4())
        
        # セッションに保存
        games[game_id] = puzzle
        session['game_id'] = game_id
        
        return jsonify({
            'success': True,
            'game_id': game_id,
            'puzzle': puzzle.puzzle_board,
            'user_board': puzzle.user_board,
            'difficulty': difficulty
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@game_bp.route('/make_move', methods=['POST'])
def make_move():
    """数字を入力"""
    try:
        data = request.get_json()
        game_id = session.get('game_id')
        
        if not game_id or game_id not in games:
            return jsonify({'success': False, 'error': 'ゲームが見つかりません'})
        
        puzzle = games[game_id]
        row = int(data.get('row'))
        col = int(data.get('col'))
        num = int(data.get('num'))
        
        success, message = puzzle.make_move(row + 1, col + 1, num)
        
        return jsonify({
            'success': success,
            'message': message,
            'user_board': puzzle.user_board
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@game_bp.route('/clear_cell', methods=['POST'])
def clear_cell():
    """セルをクリア"""
    try:
        data = request.get_json()
        game_id = session.get('game_id')
        
        if not game_id or game_id not in games:
            return jsonify({'success': False, 'error': 'ゲームが見つかりません'})
        
        puzzle = games[game_id]
        row = int(data.get('row'))
        col = int(data.get('col'))
        
        success, message = puzzle.clear_cell(row + 1, col + 1)
        
        return jsonify({
            'success': success,
            'message': message,
            'user_board': puzzle.user_board
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@game_bp.route('/check_solution', methods=['POST'])
def check_solution():
    """解答をチェック"""
    try:
        game_id = session.get('game_id')
        
        if not game_id or game_id not in games:
            return jsonify({'success': False, 'error': 'ゲームが見つかりません'})
        
        puzzle = games[game_id]
        is_correct, message = puzzle.check_solution()
        
        return jsonify({
            'success': True,
            'is_correct': is_correct,
            'message': message
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@game_bp.route('/get_hint', methods=['POST'])
def get_hint():
    """ヒントを取得"""
    try:
        game_id = session.get('game_id')
        
        if not game_id or game_id not in games:
            return jsonify({'success': False, 'error': 'ゲームが見つかりません'})
        
        puzzle = games[game_id]
        hint = puzzle.get_hint()
        
        return jsonify({
            'success': True,
            'hint': hint
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@game_bp.route('/get_board', methods=['GET'])
def get_board():
    """現在の盤面を取得"""
    try:
        game_id = session.get('game_id')
        
        if not game_id or game_id not in games:
            return jsonify({'success': False, 'error': 'ゲームが見つかりません'})
        
        puzzle = games[game_id]
        
        return jsonify({
            'success': True,
            'puzzle_board': puzzle.puzzle_board,
            'user_board': puzzle.user_board
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Blueprintを登録
app.register_blueprint(game_bp)

# ルートパスから /game にリダイレクト
@app.route('/')
def root():
    from flask import redirect
    return redirect('/game/')

# Vercel用のハンドラー
def handler(request):
    return app(request.environ, lambda status, headers: None)