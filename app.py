from flask import Flask, render_template, jsonify, request, session, Blueprint, redirect
import uuid
import random
import copy
import os

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'vercel-sudoku-secret-key-2024')

# Game sessions storage
games = {}

# Sudoku classes (embedded to avoid import issues)
class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
    def is_valid(self, board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column  
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
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

# Blueprint for /game prefix
game_bp = Blueprint('game', __name__, url_prefix='/game')

@game_bp.route('/')
def index():
    return render_template('index.html')

@game_bp.route('/new_game', methods=['POST'])
def new_game():
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'medium')
        
        puzzle = SudokuPuzzle()
        puzzle.create_puzzle(difficulty)
        
        game_id = str(uuid.uuid4())
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

# Register Blueprint
app.register_blueprint(game_bp)

# Root route redirect
@app.route('/')
def root():
    return redirect('/game/')

if __name__ == '__main__':
    app.run(debug=False)