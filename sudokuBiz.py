import numpy as np

#メイン盤面。初期値0で9x9の盤面を生成。
board = np.zeros((9, 9), dtype=int)
#候補盤面。3次元。全てのマスに1~9の値が候補として入っている。
opt = np.full((9, 9, 9), np.arange(1, 10, dtype=int))
#過去分の盤面データ。iで何番目のデータを取り出すか指定。
hBoard = [] #1+2次元。
hOpt = []   #1+3次元。

# モジュール実行用。盤面情報を入力したら答えを返す。
def execute(paramBoard: np.ndarray):
    global board
    board = np.copy(paramBoard)
    for i in range(0,9):
        for j in range(0,9):
            if board[i,j] != 0:
                answer(j,i,board[i,j])
    dataSave()
    contradiction()
    return board

# xyマスの数字をnumで確定させる。
def answer(x, y, num):
    global board
    if x < 0: x += 9 
    if y < 0: y += 9
    board[y,x] = num
    # 候補を消去する。
    omitopt(x, y, num)

# xyマスの候補からnumを外す。縦横、3x3エリアの候補からもnumを外す。
def omitopt(x,y,num):
    global opt
    # xyマスの候補を消去。
    opt[y,x,:] = np.zeros(9, dtype=int)
    # y軸の候補を消去
    opt[:,x,num-1] = np.zeros(9, dtype=int)
    # x軸の候補を消去
    opt[y,:,num-1] = np.zeros(9, dtype=int)
    
    # 9つに分解した3x3エリアのどこに位置するか特定
    #x軸
    if x < 3:
        plusx = 0 
    elif x < 6:
        plusx = 3
    else:
        plusx = 6
    # y軸
    if y < 3:
        plusy = 0 
    elif y < 6:
        plusy = 3
    else:
        plusy = 6
    # 特定した3x3エリアの候補からnumを消去
    for i in range(plusy, plusy+3):
        for j in range(plusx, plusx+3):
            opt[i,j,num-1] = 0
    
    # 候補が1つだけのマスがあったらanswerを再帰的に呼び出す。
    for i in range(0, 9):
        for j in range(0, 9):
            if np.count_nonzero(opt[i,j,:]) == 1:
                answer(j, i, searchFirstNonzero(j,i))

# xyマスから0を除いた最初の候補を取り出す。
def searchFirstNonzero(x,y):
    global opt
    # xyマスの候補から0を除いた配列を出力
    arr = np.nonzero(opt[y,x,:])
    # 出力した配列から最初の候補のみ取り出す。
    return opt[y,x,arr[0][0]]

# 背理法を用いて計算する。
def contradiction():
    global board, opt
    i = 0
    j = 0
    while i < 9:
        while j < 9:
            if board[i,j] == 0:
                if np.count_nonzero(opt[i,j,:]) == 0:
                    # optの候補が無くなってもboardが埋まらなかったら直近の解答は偽であるため、候補から外す。
                    dataLoad() #直近の状態に戻す。
                    dataDelete() #直近の状態を履歴から削除
                    deleteFirstSel()
                    # カウントをリセットして最初からやり直し。
                    i = 0
                    j = 0
                    continue
                else:
                    dataSave()
                    answer(j, i, searchFirstNonzero(j,i))
            j += 1
        j = 0
        i += 1

# dataから直近の候補を削除する。
def deleteFirstSel():
    global opt
    for i in range(0,9):
        for j in range(0,9):
            if np.count_nonzero(opt[i,j,:]) > 0:
                opt[i,j,searchFirstNonzero(j,i)-1] = 0
                return

def dataSave():
    global hBoard, hOpt
    hBoard.append(np.copy(board))
    hOpt.append(np.copy(opt))

def dataDelete():
    global hBoard, hOpt
    hBoard = hBoard[:-1]
    hOpt = hOpt[:-1]

def dataLoad():
    global board, opt, hBoard, hOpt
    board = np.copy(hBoard[-1])
    opt = np.copy(hOpt[-1])