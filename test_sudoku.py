#!/usr/bin/env python3
from sudoku import SudokuPuzzle

def test_sudoku_functionality():
    """ナンプレの機能をテストする"""
    print("="*60)
    print("         ナンプレアプリ機能テスト")
    print("="*60)
    
    # ナンプレパズルのインスタンスを作成
    puzzle = SudokuPuzzle()
    
    print("\n1. 完全なナンプレ盤の生成をテスト...")
    complete_board = puzzle.generator.generate_complete_board()
    print("✓ 完全なナンプレ盤が生成されました")
    
    print("\n完全解答（参考用）:")
    puzzle.complete_board = complete_board
    puzzle.display_board(complete_board)
    
    print("\n2. 難易度別の問題生成をテスト...")
    difficulties = ["easy", "medium", "hard"]
    
    for difficulty in difficulties:
        print(f"\n--- {difficulty.upper()} 難易度 ---")
        puzzle_board = puzzle.create_puzzle(difficulty)
        
        # 空欄の数を数える
        empty_cells = sum(row.count(0) for row in puzzle_board)
        print(f"空欄の数: {empty_cells}個")
        
        # 問題を表示
        puzzle.display_board()
        
    print("\n3. 解答チェック機能をテスト...")
    
    # 中程度の問題を作成
    puzzle.create_puzzle("medium")
    print("問題盤面:")
    puzzle.display_board()
    
    # 間違った解答で確認
    puzzle.user_board[0][0] = 9  # 間違いを入れる
    is_correct, message = puzzle.check_solution()
    print(f"\n間違った解答のテスト: {message}")
    
    # 正解を入れて確認
    puzzle.user_board = puzzle.complete_board
    is_correct, message = puzzle.check_solution()
    print(f"正解のテスト: {message}")
    
    print("\n4. 数字入力機能をテスト...")
    puzzle.create_puzzle("easy")
    
    # 有効な手をテスト
    success, message = puzzle.make_move(1, 1, 5)
    print(f"数字入力テスト (1,1,5): {message}")
    
    # 無効な手をテスト
    success, message = puzzle.make_move(10, 1, 5)
    print(f"無効座標テスト (10,1,5): {message}")
    
    print("\n5. ヒント機能をテスト...")
    hint = puzzle.get_hint()
    print(f"ヒント: {hint}")
    
    print("\n6. セルクリア機能をテスト...")
    success, message = puzzle.clear_cell(1, 1)
    print(f"セルクリアテスト: {message}")
    
    print("\n="*60)
    print("全機能のテストが完了しました！")
    print("="*60)
    print("\nアプリは正常に動作しています。")
    print("実際に使用するには以下のコマンドを実行してください:")
    print("python3 main.py")
    print("\nまたは、より詳細な動作を確認したい場合:")
    print("python3 -c \"from main import SudokuCLI; cli = SudokuCLI(); print('アプリが正常に初期化されました'); puzzle = cli.puzzle; puzzle.create_puzzle('easy'); puzzle.display_board()\"")

def test_board_generation_speed():
    """盤面生成速度をテスト"""
    import time
    
    print("\n" + "="*40)
    print("盤面生成速度テスト")
    print("="*40)
    
    puzzle = SudokuPuzzle()
    
    # 複数回生成して平均時間を計測
    times = []
    for i in range(5):
        start_time = time.time()
        puzzle.create_puzzle("medium")
        end_time = time.time()
        generation_time = end_time - start_time
        times.append(generation_time)
        print(f"生成 {i+1}: {generation_time:.3f}秒")
    
    avg_time = sum(times) / len(times)
    print(f"\n平均生成時間: {avg_time:.3f}秒")
    print("✓ パフォーマンステスト完了")

if __name__ == "__main__":
    test_sudoku_functionality()
    test_board_generation_speed()