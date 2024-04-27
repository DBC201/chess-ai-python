from ChessGui import ChessGui
from ChessAi import ChessAi

if __name__ == '__main__':
    ChessGui.init()
    chess_gui = ChessGui()
    chess_gui.run(None, ChessAi(3))
    ChessGui.quit()
