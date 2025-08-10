#!/usr/bin/env python3
from sudoku import SudokuPuzzle


class SudokuCLI:
    def __init__(self):
        self.puzzle = SudokuPuzzle()
        self.running = True
        
    def display_menu(self):
        """メインメニューを表示"""
        print("\n" + "="*50)
        print("           ナンプレ（数独）ゲーム")
        print("="*50)
        print("1. 新しいゲームを始める")
        print("2. 数字を入力する")
        print("3. セルをクリアする")
        print("4. 盤面を表示する")
        print("5. 解答をチェックする")
        print("6. ヒントを見る")
        print("7. ゲームを終了する")
        print("-"*50)
        
    def get_difficulty(self):
        """難易度を選択"""
        print("\n難易度を選択してください:")
        print("1. 簡単 (Easy)")
        print("2. 普通 (Medium)")  
        print("3. 難しい (Hard)")
        
        while True:
            try:
                choice = input("選択 (1-3): ").strip()
                if choice == "1":
                    return "easy"
                elif choice == "2":
                    return "medium"
                elif choice == "3":
                    return "hard"
                else:
                    print("1、2、3のいずれかを入力してください")
            except KeyboardInterrupt:
                print("\nゲームを終了します")
                return None
                
    def get_input_coordinates(self, action="入力"):
        """座標と数字の入力を取得"""
        try:
            if action == "入力":
                input_str = input(f"\n{action}する位置と数字を入力 (例: 1 1 5 = 1行1列に5): ").strip()
                parts = input_str.split()
                if len(parts) != 3:
                    return None, None, None, "行、列、数字を空白で区切って入力してください"
                row, col, num = map(int, parts)
                return row, col, num, None
            else:  # クリア
                input_str = input(f"\n{action}する位置を入力 (例: 1 1 = 1行1列): ").strip()
                parts = input_str.split()
                if len(parts) != 2:
                    return None, None, None, "行、列を空白で区切って入力してください"
                row, col = map(int, parts)
                return row, col, 0, None
                
        except ValueError:
            return None, None, None, "数字を正しく入力してください"
        except KeyboardInterrupt:
            return None, None, None, "キャンセルされました"
            
    def show_instructions(self):
        """操作説明を表示"""
        print("\n" + "="*50)
        print("              操作説明")
        print("="*50)
        print("• 数字入力: 行番号 列番号 数字 (例: 1 1 5)")
        print("• セルクリア: 行番号 列番号 (例: 1 1)")
        print("• 行・列番号は1-9の範囲です")
        print("• . は空欄を表します")
        print("• |と-は3x3ブロックの区切りです")
        print("="*50)
        
    def run(self):
        """メインループ"""
        print("ナンプレ（数独）ゲームへようこそ！")
        self.show_instructions()
        
        while self.running:
            try:
                self.display_menu()
                choice = input("選択してください (1-7): ").strip()
                
                if choice == "1":
                    self.start_new_game()
                elif choice == "2":
                    self.input_number()
                elif choice == "3":
                    self.clear_cell()
                elif choice == "4":
                    self.display_board()
                elif choice == "5":
                    self.check_solution()
                elif choice == "6":
                    self.show_hint()
                elif choice == "7":
                    self.exit_game()
                else:
                    print("無効な選択です。1-7の数字を入力してください。")
                    
            except KeyboardInterrupt:
                print("\nゲームを終了します...")
                self.running = False
            except Exception as e:
                print(f"エラーが発生しました: {e}")
                
    def start_new_game(self):
        """新しいゲームを開始"""
        print("\n新しいゲームを開始します...")
        
        difficulty = self.get_difficulty()
        if difficulty is None:
            return
            
        print(f"難易度: {difficulty}")
        print("問題を生成中...")
        
        try:
            self.puzzle.create_puzzle(difficulty)
            print("問題が生成されました！")
            self.puzzle.display_board()
        except Exception as e:
            print(f"問題生成エラー: {e}")
            
    def input_number(self):
        """数字を入力"""
        if self.puzzle.user_board is None:
            print("まず新しいゲームを始めてください")
            return
            
        row, col, num, error = self.get_input_coordinates("入力")
        if error:
            print(f"エラー: {error}")
            return
            
        success, message = self.puzzle.make_move(row, col, num)
        print(message)
        
        if success:
            self.puzzle.display_board()
            
    def clear_cell(self):
        """セルをクリア"""
        if self.puzzle.user_board is None:
            print("まず新しいゲームを始めてください")
            return
            
        row, col, _, error = self.get_input_coordinates("クリア")
        if error:
            print(f"エラー: {error}")
            return
            
        success, message = self.puzzle.clear_cell(row, col)
        print(message)
        
        if success:
            self.puzzle.display_board()
            
    def display_board(self):
        """盤面を表示"""
        if self.puzzle.user_board is None:
            print("まず新しいゲームを始めてください")
            return
            
        self.puzzle.display_board()
        
    def check_solution(self):
        """解答をチェック"""
        if self.puzzle.user_board is None:
            print("まず新しいゲームを始めてください")
            return
            
        is_correct, message = self.puzzle.check_solution()
        print(f"\n{message}")
        
        if is_correct:
            print("🎉 ゲームクリア！新しいゲームを始めますか？")
            
    def show_hint(self):
        """ヒントを表示"""
        if self.puzzle.user_board is None:
            print("まず新しいゲームを始めてください")
            return
            
        hint = self.puzzle.get_hint()
        print(f"\n💡 {hint}")
        
    def exit_game(self):
        """ゲームを終了"""
        print("ゲームを終了します。ありがとうございました！")
        self.running = False


def main():
    """メイン実行関数"""
    cli = SudokuCLI()
    cli.run()


if __name__ == "__main__":
    main()