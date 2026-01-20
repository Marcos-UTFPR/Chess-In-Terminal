import os
import sys
import time

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Constantes e Variáveis Globais ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Só vão ser alteradas dentro do desenvolvimento

# Símbolos
W = "_w" # Peças brancas
king_w = '♔'
queen_w = '♕'
rook_w = '♖'
bishop_w = '♗'
knight_w = '♘'
pawn_w = '♙'
empty_w = '■'
WHITE = (king_w, queen_w, rook_w, bishop_w, knight_w, pawn_w)

B = "_b" # Peças pretas
king_b = '♚'
queen_b = '♛'
rook_b = '♜'
bishop_b = '♝'
knight_b = '♞'
pawn_b = '♟'
empty_b = '□'
BLACK = (king_b, queen_b, rook_b, bishop_b, knight_b, pawn_b)

SYMBOLS = (king_w, queen_w, rook_w, bishop_w, knight_w, pawn_w, empty_w, king_b, queen_b, rook_b, bishop_b, knight_b, pawn_b, empty_b)

FREE_PLAYER = False # Flag que indica que o símbolo da rodada é automático e troca a vez do jogador (False = automática, True = manual, Padrão = False) - Não usada

# Variáveis usadas para guardar as células (e a peça) durante as alterações
oldCell = None
newCell = None
movingPiece = None

# Variável usada para definir as cores das casas do tabuleiro
collective_Cell_color = B

# Cores
PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Exceções -------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------

class EmptyCellException(Exception): # Exceção usada para indicar que selecionou uma casa vazia
    def __init__(self, message=("Erro de Casa")):
        # Call the base class constructor with the parameters it needs
        super(EmptyCellException, self).__init__(message) 

class EnemyCellException(Exception): # Exceção usada para indicar que selecionou uma peça inimiga
    def __init__(self, message=("Erro de Casa")):
        # Call the base class constructor with the parameters it needs
        super(EnemyCellException, self).__init__(message)

class BlockedPathException(Exception): # Exceção usada para indicar que achou uma casa ocupada no caminho
    def __init__(self, message=("Erro de Casa")):
        # Call the base class constructor with the parameters it needs
        super(BlockedPathException, self).__init__(message)

class InvalidMoveException(Exception): # Exceção usada para indicar um movimento inválido
    def __init__(self, message=("Erro de Casa")):
        # Call the base class constructor with the parameters it needs
        super(InvalidMoveException, self).__init__(message)

class WhiteVictoryException(Exception): # Exceção usada para detectar se houve vitória
    def __init__(self, message=("Branco Venceu!")):
        # Call the base class constructor with the parameters it needs
        super(WhiteVictoryException, self).__init__(message)

class BlackVictoryException(Exception): # Exceção usada para detectar se houve vitória
    def __init__(self, message=("Preto Venceu!")):
        # Call the base class constructor with the parameters it needs
        super(BlackVictoryException, self).__init__(message)

class OccupiedCellException(Exception): # Exceção usada para indicar que selecionou uma casa vazia
    def __init__(self, message=("Erro de Casa")):
        # Call the base class constructor with the parameters it needs
        super(OccupiedCellException, self).__init__(message) 

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Funções auxiliares ---------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------

def typewriterPrint(message): # Um print lento com efeito de "máquina de escrever"
    for x in message:
        print(x, end='')
        sys.stdout.flush()
        time.sleep(0.1)
    print('\n', end='') # Pulando linha

def travelHorizontalPath(): # Verifica o caminho em linha reta
    pass

def travelDiagonalPath(): # Verifica o caminho em diagonal
    pass

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Outros ---------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------

def doNothing():
    pass

def doNothingForApproximately(seconds): # Um time.sleep() bem piorado
    # 1 ciclo quase é 1 segundo exato
    for i in range(seconds):
        i = 0
        while i < 16706910:
            pass
            i += 1

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Classes principais ---------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class piece():
    # Atributos: symbol, current_cell, color e movimentos (quantidades de movimentos já feito)
    def __init__(self, color, name, cell=None):
        self.name = name # Nome do tipo de peça dela
        self.symbol = globals()[f"{name}{color}"]
        self.color = color # Cor da peça (constante W ou B)
        self.current_cell = cell # Casa onde ela está atualmente
        self.movimentos = 0 # Quantidade de movimentos que a peça já fez

    # ---------------------------------------
    
    def check(): # Checa se a peça existe
        return True
    
    # ---------------------------------------

    def start(self, cell):
        self.current_cell = cell
    
    # ---------------------------------------

    def print(self):
        return self.symbol
    
    # ---------------------------------------
    
    def checkPath(self): # Padrão das peças é retornar a exceção, mas a vazia sobreescreve esse método para retornar True
        raise BlockedPathException()

    # ---------------------------------------

    def capture(self, nextCell):
        if nextCell.current_piece.color != self.color:
            try:
                symbol = nextCell.current_piece.symbol
                gameMain.mainCemitery.capture(nextCell.current_piece) # Mandando a célula da casa destino para o cemitério
                self.current_cell.current_piece = empty(oldCell.color,"empty") # Esvaziando a casa atual
                self.current_cell = nextCell
                self.current_cell.current_piece = self
                self.movimentos += 1 # Aumenta o contador de movimentos
                print(BLUE,f"Peça {symbol}  capturada!",END)
            except (WhiteVictoryException, BlackVictoryException) as e: # Modifica uma última vez
                self.current_cell.current_piece = empty(oldCell.color,"empty") # Esvaziando a casa atual
                self.current_cell = nextCell
                self.current_cell.current_piece = self
                self.movimentos += 1 # Aumenta o contador de movimentos
                raise e
        else:
            raise OccupiedCellException()

    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class empty(piece):
    def __init__(self, color, name, cell=None):
        super().__init__(color, name, cell)

    # ---------------------------------------

    def alter(self, currentLine=None, newLine=None, nextCell=None):
        raise EmptyCellException()
    
    # ---------------------------------------

    def checkPath(self): # Padrão das peças é retornar a exceção, mas a vazia sobreescreve esse método para retornar True
        return True
    
    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class pawn(piece):
    # Atributos: symbol, current_cell, color e movimentos (quantidades de movimentos já feito)
    def __init__(self, color, name, cell=None):
        super().__init__(color, name, cell)

    # ---------------------------------------

    def alter(self, currentLine, newLine, nextCell): # Experimental (OBS: Primeiro movimento -> pode ter 2 pulos)
        currentLine = int(currentLine)
        newLine = int(newLine)
        if nextCell.cellNumber == oldCell.cellNumber: # Mesma coluna, mas linha 1 de diferença
            # Movimento padrão
            if ((currentLine+1 == newLine and self.color == W) or ((currentLine-1) == newLine and self.color == B)):
                if nextCell.current_piece.name == "empty": # A próxima casa precisa estar vazia
                    self.current_cell.current_piece = empty(oldCell.color,"empty") # Esvaziando a casa atual
                    self.current_cell = nextCell
                    self.current_cell.current_piece = self
                    self.movimentos += 1 # Aumenta o contador de movimentos
                    self.promotion(newLine) # Confere se o peão pode ser promovido ou não
                else:
                    raise InvalidMoveException()
            # Primeiro movimento
            elif (((currentLine+2 == newLine and self.color == W) or ((currentLine-2) == newLine and self.color == B)) and self.movimentos == 0): 
                if nextCell.current_piece.name == "empty": # A próxima casa precisa estar vazia
                    self.current_cell.current_piece = empty(oldCell.color,"empty") # Esvaziando a casa atual
                    self.current_cell = nextCell
                    self.current_cell.current_piece = self
                    self.movimentos += 1 # Aumenta o contador de movimentos
                    self.promotion(newLine) # Confere se o peão pode ser promovido ou não
                else:
                    raise InvalidMoveException()
            else:
                raise InvalidMoveException()
        else:
            # Movimento de captura na diagonal (1 ou 2 linhas pra frente)
            if (((((currentLine+2 == newLine and self.color == W) or ((currentLine-2) == newLine and self.color == B)) and self.movimentos == 0) or
                (((currentLine+1 == newLine and self.color == W) or ((currentLine-1) == newLine and self.color == B)))) and
                (abs(nextCell.cellNumber - oldCell.cellNumber)== 1)):
                if nextCell.current_piece.name != "empty":
                    self.capture(nextCell)
                    self.promotion(newLine)
                else:
                    raise InvalidMoveException()
            else:
                raise InvalidMoveException()

    # ---------------------------------------

    def promotion(self, newLine):
        if (newLine == 8 and self.color == W) or (newLine == 1 and self.color == B):
            pieceNames = ["rook","bishop","knight","queen"]
            message = ("Deseja promover o seu peão para qual peça? (OBS: Informe apenas o número)\n1-Torre\n2-Bispo\n3-Cavalo\n4-Rainha\nR: ")
            while True:
                try:
                    pieceNumber = int(input(message))-1 # Pega a peça que o peão vai se transformar
                    assert pieceNames[pieceNumber] != None
                except IndexError:
                    message = "Por favor, informe uma peça válida: "
                else:
                    break
            pieceName = pieceNames[pieceNumber]
            self.current_cell.current_piece = globals()[pieceName](self.color,pieceName,self.current_cell) # Troca o peão original por uma nova peça
            self.current_cell = None # Peão original perde a referência da célula
            del self # Peão original é deletado

    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class rook(piece):
    # Atributos: symbol, current_cell, color e movimentos (quantidades de movimentos já feito)
    def __init__(self, color, name, cell=None):
        super().__init__(color, name, cell)

    # ---------------------------------------

    def alter(self, currentLine, newLine, nextCell): # Experimental
        currentLine = int(currentLine)
        newLine = int(newLine)
        if (nextCell.cellNumber == oldCell.cellNumber and currentLine != newLine) or (nextCell.cellNumber != oldCell.cellNumber and currentLine == newLine):
            if nextCell.current_piece.name == "empty": # A próxima casa precisa estar vazia
                self.current_cell.current_piece = empty(oldCell.color,"empty") # Esvaziando a casa atual
                self.current_cell = nextCell
                self.current_cell.current_piece = self
                self.movimentos += 1 # Aumenta o contador de movimentos
            else:
                self.capture(nextCell)
        else:
            raise InvalidMoveException()

    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class bishop(piece):
    # Atributos: symbol, current_cell, color e movimentos (quantidades de movimentos já feito)
    def __init__(self, color, name, cell=None):
        super().__init__(color, name, cell)

    # ---------------------------------------

    def alter(self, currentLine, newLine, nextCell): # Experimental
        currentLine = int(currentLine)
        newLine = int(newLine)
        if (nextCell.cellNumber != oldCell.cellNumber and currentLine != newLine) and (abs(nextCell.cellNumber - oldCell.cellNumber) == abs(currentLine - newLine)):
            if nextCell.current_piece.name == "empty": # A próxima casa precisa estar vazia
                self.current_cell.current_piece = empty(oldCell.color,"empty") # Esvaziando a casa atual
                self.current_cell = nextCell
                self.current_cell.current_piece = self
                self.movimentos += 1 # Aumenta o contador de movimentos
            else:
                self.capture(nextCell)
        else:
            raise InvalidMoveException()

    # ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------

class knight(piece):
    # Atributos: symbol, current_cell, color e movimentos (quantidades de movimentos já feito)
    def __init__(self, color, name, cell=None):
        super().__init__(color, name, cell)

    # ---------------------------------------

    def alter(self, currentLine, newLine, nextCell): # Experimental
        currentLine = int(currentLine)
        newLine = int(newLine)
        if ((currentLine+1 == newLine and nextCell.cellNumber+2 == oldCell.cellNumber) or 
            (currentLine+1 == newLine and nextCell.cellNumber-2 == oldCell.cellNumber) or 
            (currentLine-1 == newLine and nextCell.cellNumber+2 == oldCell.cellNumber) or 
            (currentLine-1 == newLine and nextCell.cellNumber-2 == oldCell.cellNumber) or 
            (currentLine+2 == newLine and nextCell.cellNumber+1 == oldCell.cellNumber) or
            (currentLine+2 == newLine and nextCell.cellNumber-1 == oldCell.cellNumber) or 
            (currentLine-2 == newLine and nextCell.cellNumber+1 == oldCell.cellNumber) or
            (currentLine-2 == newLine and nextCell.cellNumber-1 == oldCell.cellNumber)):
            if nextCell.current_piece.name == "empty": # A próxima casa precisa estar vazia
                self.current_cell.current_piece = empty(oldCell.color,"empty") # Esvaziando a casa atual
                self.current_cell = nextCell
                self.current_cell.current_piece = self
                self.movimentos += 1 # Aumenta o contador de movimentos
            else:
                self.capture(nextCell)
        else:
            raise InvalidMoveException()

    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class queen(piece):
    # Atributos: symbol, current_cell, color e movimentos (quantidades de movimentos já feito)
    def __init__(self, color, name, cell=None):
        super().__init__(color, name, cell)

    # ---------------------------------------

    def alter(self, currentLine, newLine, nextCell): # Experimental
        currentLine = int(currentLine)
        newLine = int(newLine)
        # Movimento de torre + Movimento de bispo
        if ((nextCell.cellNumber == oldCell.cellNumber and currentLine != newLine) or (nextCell.cellNumber != oldCell.cellNumber and currentLine == newLine) or
            (nextCell.cellNumber != oldCell.cellNumber and currentLine != newLine) and (abs(nextCell.cellNumber - oldCell.cellNumber) == abs(currentLine - newLine))):
            if nextCell.current_piece.name == "empty": # A próxima casa precisa estar vazia
                self.current_cell.current_piece = empty(oldCell.color,"empty") # Esvaziando a casa atual
                self.current_cell = nextCell
                self.current_cell.current_piece = self
                self.movimentos += 1 # Aumenta o contador de movimentos
            else:
                self.capture(nextCell)
        else:
            raise InvalidMoveException()

    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class king(piece):
    # Atributos: symbol, current_cell, color e movimentos (quantidades de movimentos já feito)
    def __init__(self, color, name, cell=None):
        super().__init__(color, name, cell)

    # ---------------------------------------

    def alter(self, currentLine, newLine, nextCell): # Experimental
        currentLine = int(currentLine)
        newLine = int(newLine)
        # Movimento de torre + Movimento de bispo
        contJump = abs(nextCell.cellNumber - oldCell.cellNumber) == 1 or abs(currentLine - newLine) == 1 # Uma casa por vez só
        if contJump:
            if ((nextCell.cellNumber == oldCell.cellNumber and currentLine != newLine) or (nextCell.cellNumber != oldCell.cellNumber and currentLine == newLine) or
                (nextCell.cellNumber != oldCell.cellNumber and currentLine != newLine) and (abs(nextCell.cellNumber - oldCell.cellNumber) == abs(currentLine - newLine))):
                if nextCell.current_piece.name == "empty": # A próxima casa precisa estar vazia
                    self.current_cell.current_piece = empty(oldCell.color,"empty") # Esvaziando a casa atual
                    self.current_cell = nextCell
                    self.current_cell.current_piece = self
                    self.movimentos += 1 # Aumenta o contador de movimentos
                else:
                    self.capture(nextCell)
            else:
                raise InvalidMoveException()
        else:
            raise InvalidMoveException()

    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class cell():
    # Atributos: color, cellNumber e current_piece
    def __init__(self, number, color): # def __init__(self,symbol = None):, usada quando podia informar de início qual símbolo iniciava, com symbol sendo opcional
        self.cellNumber = number
        self.current_piece = empty(color,"empty")
        #self.symbol = self.current_piece.symbol
        self.color = color # Cor da célula (constante W ou B)

    # ---------------------------------------

    def print(self):
        return(" "+str(self.current_piece.print())+" ")
        
    # ---------------------------------------
        
    def alter_getCells(self):
        return self
    
    # ---------------------------------------
    
    # OBS: Ainda não utilizada
    def alter(self, currentLine, newLine, newCell, player_color):
        if self.current_piece.color == player_color:
            self.current_piece.alter(currentLine, newLine, newCell)
        else:
            raise EnemyCellException()
    
    # ---------------------------------------

    def checkPath(self):
        self.current_piece.checkPath()

    # ---------------------------------------
        
    def startingPieces(self, piece):
        self.current_piece = piece
        assert self.current_piece.check
        self.current_piece.start(self) # Adicionando a casa no objeto da peça
        
    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class line():
    # Atributos: cells e lineNumber (número da linha)
    def __init__(self, number):
        number = int(number)
        if number > 0 and number < 9: # De 1 a 8
            global collective_Cell_color # Chama a variável global
            if collective_Cell_color == W:
                collective_Cell_color = B
            elif collective_Cell_color == B:
                collective_Cell_color = W
            self.lineNumber = number
            self.cells = {}
            for i in range(1,9): # Oito células, 1 a 8
                #print(i)
                self.cells[str(i)] = cell(i, collective_Cell_color)
                if collective_Cell_color == W:
                    collective_Cell_color = B
                elif collective_Cell_color == B:
                    collective_Cell_color = W

    # ---------------------------------------

    def print(self):
        #OBS: Os prints das células retornam strings
        stringPrint = ""
        for cell in self.cells.values():
            stringPrint += (f"{cell.print()}")
        return stringPrint
    
    # ---------------------------------------
    
    def alter_getCells(self,cell,global_name): # Nome da variável global a ser informada
        #print(self.cells[str(cell)].color)
        globals()[global_name] = self.cells[str(cell)].alter_getCells()

    # ---------------------------------------

    def checkPath(self,currentCell):
        self.cells[str(currentCell)].checkPath()

    # ---------------------------------------
    
    def startingPieces(self,color,pieces):
        for i in range(1,9): # Oito células, 1 a 8
            self.cells[str(i)].startingPieces(globals()[pieces[i-1]](color,pieces[i-1]))

    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------
    
class table():
    # Atributos: lines
    def __init__(self):
        self.lines = {}
        for i in range(1,9): # Oito linhas, 1 a 8
            #print(str(i))
            self.lines[str(i)] = line(i)

    # ---------------------------------------

    def print(self):
        #OBS: Os prints das linhas retornam strings
        print('---------------------------------------\n\t   ',end="")
        for i in range(1,9):
            print((" "+str(i)+" "),end="")
        print("")
        for line in self.lines.values():
            print(f"\t{line.lineNumber}. {line.print()}\n",end="") # Se preferir um tabuleiro maior
            #print(f"\t{line.lineNumber}. {line.print()}\n") # Se preferir um tabuleiro maior
        print('---------------------------------------\n')

    # ---------------------------------------

    def endGamePrint(self):
        #OBS: Os prints das linhas retornam strings
        finalPrint = ('---------------------------------------\n\t   ')
        for i in range(1,9):
            finalPrint += ((f" {i} "))
        finalPrint += ("\n")
        for line in self.lines.values():
            finalPrint += (f"\t{line.lineNumber}. {line.print()}\n")
        finalPrint+=('---------------------------------------\n\n')
        return finalPrint
    
    # ---------------------------------------

    def alter_getCells(self,currentLine,currentCell, newLine, newCell):
        self.lines[str(currentLine)].alter_getCells(currentCell,"oldCell")
        self.lines[str(newLine)].alter_getCells(newCell,"newCell")

    # ---------------------------------------

    def checkPath(self,currentLine,currentCell, newLine, newCell): # Confere se o caminho está todo vazio
        try:
            while currentLine != newLine or currentCell != newCell:
                # Muda a linha
                if currentLine > newLine:
                    currentLine -= 1
                elif currentLine < newLine:
                    currentLine += 1
                # Muda a coluna (número da célula)
                if currentCell > newCell:
                    currentCell -= 1
                elif currentCell < newCell:
                    currentCell += 1
                if currentLine != newLine or currentCell != newCell:
                    self.lines[str(currentLine)].checkPath(currentCell) # Checa todas do caminho (menos a destino e a origem)
        except BlockedPathException as e:
            raise e

    # ---------------------------------------

    def startingPieces(self):
        self.lines['1'].startingPieces(W, ["rook","knight","bishop","queen","king","bishop","knight","rook"])
        self.lines['2'].startingPieces(W, ["pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn"])
        self.lines['7'].startingPieces(B, ["pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn"])
        self.lines['8'].startingPieces(B, ["rook","knight","bishop","queen","king","bishop","knight","rook"])

    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class cemitery():
    # Atributos: pieces
    def __init__(self):
        self.captured_pieces = []

    # ---------------------------------------

    def print(self):
        #print('---------------------------------------\n')
        length = len(self.captured_pieces)
        #print("-",end="")
        print("Peças capturadas: ",end="")
        for i in range(length):
            print(self.captured_pieces[i].print()+" -",end="")
        print("")
        #print('---------------------------------------\n')

    # ---------------------------------------

    def endGamePrint(self):
        length = len(self.captured_pieces)
        finalPrint = ("Peças capturadas: ")
        for i in range(length):
            finalPrint += (self.captured_pieces[i].print()+" -")
        finalPrint += ("\n")
        return finalPrint
    
    # ---------------------------------------

    def capture(self,piece):
        self.captured_pieces.append(piece)
        if piece.name == "king":
            if piece.color == W: # Verifica a cor do rei que acabou de ser capturado
                raise BlackVictoryException()
            elif piece.color == B:
                raise WhiteVictoryException()
    
    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------

class game():
    # Atributos: mainTable, mainCemitery e current_player
    def __init__(self, current_player = None):
        self.current_player = current_player # OBS: current_player deve ser W (Branco) ou B (Preto)
        assert self.current_player == W or self.current_player == B
        self.mainTable = table()
        self.mainCemitery = cemitery()

    # ---------------------------------------

    def print(self): # Print usada para chamar o método que gera a tabela
        print('---------------------------------------')
        current_color = self.current_player
        print(f'Jogador atual: {(current_color.replace("_","")).upper()}')
        self.mainTable.print()
        self.mainCemitery.print()
    
    # ---------------------------------------

    def coloredPrint(self):
        coloredPrint = self.mainTable.endGamePrint()
        coloredPrint += self.mainCemitery.endGamePrint()
        # ----
        for i in coloredPrint: # Pega e printa cada caracter da string final separadamente
            if i in BLACK: # Preto vira Ciano
                print(CYAN+i+END, end='') # Printa os símbolos vencedores em verde
            elif i in WHITE: # Branco vira Amarelo
                print(YELLOW+i+END, end='') # Printa os símbolos perdedores em vermelho
            else:
                print(i, end='') # Printa os demais normalmente

    # ---------------------------------------

    def endGamePrint(self, winner): # Print usada para printar o jogo uma última vez
        finalPrint = self.mainTable.endGamePrint()
        finalPrint += self.mainCemitery.endGamePrint()
        # ----
        if winner == "Branco":
            loser = BLACK
            winner = WHITE
        elif winner == "Preto":
            loser = WHITE
            winner = BLACK
        for i in finalPrint: # Pega e printa cada caracter da string final separadamente
            if i in winner:
                print(GREEN+i+END, end='') # Printa os símbolos vencedores em verde
            elif i in loser:
                print(RED+i+END, end='') # Printa os símbolos perdedores em vermelho
            else:
                print(i, end='') # Printa os demais normalmente

    # ---------------------------------------

    def start(self):
        self.mainTable.startingPieces()

    # ---------------------------------------

    def switch(self):
        if self.current_player == W:
            self.current_player = B
        elif self.current_player == B:
            self.current_player = W
        assert self.current_player == W or self.current_player == B

    # ---------------------------------------

    def round(self):
        try:
            self.alter()
        except BlackVictoryException:
            self.victory("Preto")
        except WhiteVictoryException:
            self.victory("Branco")

    # ---------------------------------------

    def victory(self,winner):
        typewriterPrint(GREEN+f"{winner} venceu!!!"+END) # Printando em verde
        self.endGamePrint(winner)
        exit()

    # ---------------------------------------

    def alter(self): # Função que faz todas as alterações no round, separei para não acumular com os tratamentos das exceções de vitória
        while True:
            try:
                currentLine = int(input("Informe uma linha: "))
                currentCell = int(input("Informe uma coluna: ")) # Número da célula na programação
                newLine = int(input("Informe uma nova linha: "))
                nextCell = int(input("Informe uma nova coluna: ")) # Número da célula na programação
                self.mainTable.alter_getCells(currentLine,currentCell, newLine, nextCell) # Coloca as duas casas (origem e destino) nas variáveis globais
                global oldCell # Contém a célula de origem
                global newCell # Contém a célula de destino
                # !!!! - Alterar essa parte
                # OBS: Tem que alterar esse teste das casas vazias ou peças inimigas
                if oldCell.current_piece.color == self.current_player: 
                    oldCell.current_piece.alter(currentLine, newLine, newCell) # Pegando a peça via a casa original
                    self.switch() # Alterando o jogador
                else:
                    raise EnemyCellException()
                if oldCell.current_piece.name != "knight": # Cavalo ignora essa regra do caminho bloqueado
                    self.mainTable.checkPath(currentLine,currentCell, newLine, nextCell) # Confere se o caminho está vazio
            except EmptyCellException:
                print(YELLOW,"Casa vazia, selecione outra...",END)
            except EnemyCellException:
                print(YELLOW,"Peça inimiga selecionada, selecione outra casa...",END)
            except InvalidMoveException:
                print(YELLOW,"Movimento inválido! Selecione outra casa...",END)
            except (KeyError,ValueError):
                print(YELLOW,"Casa inválida, selecione outra casa...",END)
            except BlockedPathException:
                print(YELLOW,"Caminho bloqueado, selecione outra casa...",END)
            except OccupiedCellException:
                print(YELLOW,"Casa ocupada, selecione outra casa...",END)
            else:
                #exit()
                break

    # ---------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Seção principal do código --------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------

def main(): # Função principal
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa o terminal

    # ---------------------------------------
    global gameMain
    gameMain = game(W) # Iniciando com as peças brancas
    gameMain.start()
    # ---------------------------------------
    
    # ---------------------------------------
    # Loop do game
    # OBS: W = Branco e B = Preto
    gameMain.print()
    #gameMain.coloredPrint() # OBS: Preto vira Ciano e Branco vira Amarelo
    while True:
        gameMain.round()
        gameMain.print()
        #gameMain.coloredPrint()
        #break
    # ---------------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(YELLOW+"\nPrograma encerrado via terminal..."+END)

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Fim do código --------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------          