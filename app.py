from flask import Flask, render_template, jsonify, request, session, Blueprint
from sudoku import SudokuPuzzle
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# ゲームセッションを保存する辞書
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)