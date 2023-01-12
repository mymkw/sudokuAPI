from flask import Flask, request
import numpy as np
import sudokuBiz as sd


app = Flask(__name__)

@app.route("/calc", methods=["POST"])
def calcProbrem():
    data = request.get_json()
    board_param = data["board"]
    print(f'param  -> {board_param}')
    board_result = sd.execute(convert_str2arr(board_param))
    board = convert_arr2str(board_result)
    print(f'result -> {board}')
    return {
        "board": board
    }
    
def convert_str2arr(str: str):
    arr = np.array(list(str), dtype="int").reshape(9,9)
    return arr

def convert_arr2str(arr: np.ndarray):
    str = np.array2string(arr.flatten(), max_line_width=83 , separator="")[1:-1]
    return str