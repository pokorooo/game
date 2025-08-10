class SudokuWebApp {
    constructor() {
        this.selectedCell = null;
        this.gameBoard = null;
        this.puzzleBoard = null;
        this.userBoard = null;
        
        this.initializeEventListeners();
        this.createBoard();
    }

    initializeEventListeners() {
        // 新しいゲームボタン
        document.getElementById('new-game-btn').addEventListener('click', () => {
            this.startNewGame();
        });

        // 数字パッドボタン
        document.querySelectorAll('.number-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const num = parseInt(e.target.getAttribute('data-num'));
                this.inputNumber(num);
            });
        });

        // クリアボタン
        document.getElementById('clear-btn').addEventListener('click', () => {
            this.clearCell();
        });

        // 解答チェックボタン
        document.getElementById('check-btn').addEventListener('click', () => {
            this.checkSolution();
        });

        // ヒントボタン
        document.getElementById('hint-btn').addEventListener('click', () => {
            this.getHint();
        });

        // キーボード入力
        document.addEventListener('keydown', (e) => {
            if (e.key >= '1' && e.key <= '9') {
                this.inputNumber(parseInt(e.key));
            } else if (e.key === 'Delete' || e.key === 'Backspace') {
                this.clearCell();
            }
        });
    }

    createBoard() {
        const boardElement = document.getElementById('sudoku-board');
        boardElement.innerHTML = '';

        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                const cell = document.createElement('div');
                cell.className = 'sudoku-cell';
                cell.setAttribute('data-row', row);
                cell.setAttribute('data-col', col);
                
                cell.addEventListener('click', (e) => {
                    this.selectCell(e.target);
                });

                boardElement.appendChild(cell);
            }
        }
    }

    selectCell(cell) {
        // 前の選択をクリア
        document.querySelectorAll('.sudoku-cell').forEach(c => {
            c.classList.remove('selected');
        });

        // 新しいセルを選択
        cell.classList.add('selected');
        this.selectedCell = cell;
    }

    async startNewGame() {
        const difficulty = document.getElementById('difficulty').value;
        this.showMessage('新しいゲームを生成中...', 'info');

        try {
            const response = await fetch('/game/new_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    difficulty: difficulty
                })
            });

            const data = await response.json();

            if (data.success) {
                this.puzzleBoard = data.puzzle;
                this.userBoard = data.user_board;
                this.updateBoard();
                this.showMessage(`${difficulty.toUpperCase()}難易度の新しいゲームを開始しました！`, 'success');
            } else {
                this.showMessage('ゲーム生成エラー: ' + data.error, 'error');
            }
        } catch (error) {
            this.showMessage('サーバーエラー: ' + error.message, 'error');
        }
    }

    updateBoard() {
        const cells = document.querySelectorAll('.sudoku-cell');
        
        cells.forEach((cell, index) => {
            const row = Math.floor(index / 9);
            const col = index % 9;
            
            // スタイルをリセット
            cell.classList.remove('given', 'user-input');
            
            const puzzleValue = this.puzzleBoard[row][col];
            const userValue = this.userBoard[row][col];
            
            if (puzzleValue !== 0) {
                // 元から与えられている数字
                cell.textContent = puzzleValue;
                cell.classList.add('given');
            } else if (userValue !== 0) {
                // ユーザーが入力した数字
                cell.textContent = userValue;
                cell.classList.add('user-input');
            } else {
                // 空欄
                cell.textContent = '';
            }
        });
    }

    async inputNumber(num) {
        if (!this.selectedCell || !this.userBoard) {
            this.showMessage('セルを選択するか、新しいゲームを開始してください', 'error');
            return;
        }

        const row = parseInt(this.selectedCell.getAttribute('data-row'));
        const col = parseInt(this.selectedCell.getAttribute('data-col'));

        try {
            const response = await fetch('/game/make_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    row: row,
                    col: col,
                    num: num
                })
            });

            const data = await response.json();

            if (data.success) {
                this.userBoard = data.user_board;
                this.updateBoard();
                this.showMessage(data.message, 'success');
            } else {
                this.showMessage(data.error || data.message, 'error');
            }
        } catch (error) {
            this.showMessage('サーバーエラー: ' + error.message, 'error');
        }
    }

    async clearCell() {
        if (!this.selectedCell || !this.userBoard) {
            this.showMessage('セルを選択するか、新しいゲームを開始してください', 'error');
            return;
        }

        const row = parseInt(this.selectedCell.getAttribute('data-row'));
        const col = parseInt(this.selectedCell.getAttribute('data-col'));

        try {
            const response = await fetch('/game/clear_cell', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    row: row,
                    col: col
                })
            });

            const data = await response.json();

            if (data.success) {
                this.userBoard = data.user_board;
                this.updateBoard();
                this.showMessage(data.message, 'success');
            } else {
                this.showMessage(data.error || data.message, 'error');
            }
        } catch (error) {
            this.showMessage('サーバーエラー: ' + error.message, 'error');
        }
    }

    async checkSolution() {
        if (!this.userBoard) {
            this.showMessage('新しいゲームを開始してください', 'error');
            return;
        }

        try {
            const response = await fetch('/game/check_solution', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (data.success) {
                if (data.is_correct) {
                    this.showMessage(data.message + ' 🎉', 'success');
                    this.celebrateWin();
                } else {
                    this.showMessage(data.message, 'error');
                }
            } else {
                this.showMessage(data.error, 'error');
            }
        } catch (error) {
            this.showMessage('サーバーエラー: ' + error.message, 'error');
        }
    }

    async getHint() {
        if (!this.userBoard) {
            this.showMessage('新しいゲームを開始してください', 'error');
            return;
        }

        try {
            const response = await fetch('/game/get_hint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showMessage('💡 ' + data.hint, 'hint');
            } else {
                this.showMessage(data.error, 'error');
            }
        } catch (error) {
            this.showMessage('サーバーエラー: ' + error.message, 'error');
        }
    }

    showMessage(text, type) {
        const messageElement = document.getElementById('message');
        messageElement.textContent = text;
        messageElement.className = `message ${type}`;
        
        // 3秒後にメッセージを薄くする
        setTimeout(() => {
            messageElement.style.opacity = '0.6';
        }, 3000);
        
        // リセット用
        setTimeout(() => {
            messageElement.style.opacity = '1';
        }, 100);
    }

    celebrateWin() {
        // 勝利時のアニメーション効果
        const cells = document.querySelectorAll('.sudoku-cell');
        cells.forEach((cell, index) => {
            setTimeout(() => {
                cell.style.background = 'linear-gradient(45deg, #68d391, #38a169)';
                cell.style.color = 'white';
                cell.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    cell.style.transform = 'scale(1)';
                }, 200);
            }, index * 20);
        });

        // 元の色に戻す - インラインスタイルを完全にクリア
        setTimeout(() => {
            cells.forEach(cell => {
                cell.style.background = '';
                cell.style.color = '';
                cell.style.transform = '';
            });
            this.updateBoard();
        }, 2000);
    }
}

// ページ読み込み後にアプリを初期化
document.addEventListener('DOMContentLoaded', () => {
    new SudokuWebApp();
});