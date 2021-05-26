from ClearPDFParser_old import listarDiretorio, main


try:
    import pdfminer
    from subprocess import run
    from subprocess import DEVNULL
    from os import getcwd
    from os import listdir
    from datetime import datetime
    from time import strptime
except ImportError:
    print('Pacote pdfminer não foi encontrado, tente executar: pip3 install pdfminer')

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Nota:
# Refatoração do outro arquivo

    def __init__(self, vt, q, n, o, e, d, a):
        self.valor_total = vt
        self.negociacao = n
        self.quantidade = q
        self.operacao = o
        self.empresa = e
        self.data = d
        self.arq = a

    def setArq(self, arq):
        self.arq = arq
        return self.arq

    def getValorTotal(self, arq):
        index = 0
        try:
            index = arq.index('Valor Operação / Ajuste')+2
            try:
                # Valor da ação
                if(type(arq[index][0]) == int):
                    self.valor_total = self.quantidade * float(arq[index+2].replace(',', '.'))
                    return
            except:
                # Nome de empresa
                index += 2
                self.valor_total = self.quantidade * float(arq[index+2].replace(',', '.'))
                return
        except:
            index = -1
            print('Erro ao procurar valor total!')
            exit()
        return 
    
    def getNegociacoes(self, arq):
        self.negociacao = arq.count('1-BOVESPA')
        return self.negociacao
    
    def getEmpresa(self, arq):
        if self.negociacao > 0:

            self.empresa = []
            try:
                index = arq.index('Valor Operação / Ajuste')+2
            except:
                print('\nMais de uma empresa não identificada!')
                pass

            for f in range(index, index+self.negociacao):
                tratar_string = arq[f].replace('    ', '').replace('ON', '').replace('NM','').strip()
                self.empresa.append(tratar_string)
        else:
            print('\nErro: nenhuma negociação identificada!')

        return self.empresa

    def getPrazoFix(self, arq):
        try:
            index = arq.index('Prazo Especificação do título')
        except:
            index = arq.index('Especificação do título')
        return

    def getQuantidade(self, arq):
        self.quantidade = []
        if self.negociacao > 0:
            index = arq.index('Valor Operação / Ajuste')+2
            try:
                # Valor da ação
                for _ in range(0, self.negociacao):
                    # print('Ação', arq[index])
                    if(type(int(arq[index][0])) == int):
                        self.quantidade.append(int(arq[index]))
                        index += 1
                return self.quantidade
            except:
                # Nome de empresa
                index += 2 if self.negociacao == 1 else + self.negociacao + 1
                for _ in range(0, self.negociacao+1):
                    # print('Nome', arq[index])
                    if (arq[index] == ''):
                        continue
                    self.quantidade.append(int(arq[index]))
                    index += 1
                return self.quantidade

        else:
            print('\nErro: nenhuma negociação identificada!')
        
        return self.quantidade

    def getData(self, arq):
        index = arq.index('Data pregão')+2
        self.data = datetime(*(strptime(arq[index], '%d/%m/%Y')[:6]))
        return self.data

def listarDiretorio():
    itens = list(filter(lambda f: f.endswith('pdf'), listdir(getcwd())))
    
    for item in itens:
        if(item.endswith('pdf')):
            print(Colors.OKBLUE + str(itens.index(item)+1) + '. ' + item + Colors.ENDC)
    
    try:
        i = input(Colors.WARNING + 'Qual arquivo deseja extrair informações? \n(digite -1 caso queira extrair todos os arquivos)?\n' + Colors.ENDC)
        if type(i) != str:
            raise ValueError()

        if i=='-1':
            return itens
        else:
            r = []
            r.append(itens[int(i)-1])
            return r

    except ValueError:
        print('A resposta não é um número!\nInput lido: {}'.format(type(i)))
        exit()

def main(i_arq):

    for i in i_arq:
        
        input_arq = str(i)[:-3]+'txt'
        run(['pdf2txt.py', '-o', input_arq, i], stdout=None, stderr=DEVNULL)

        with open(input_arq, 'r') as tempTxt:
            arq = tempTxt.readlines()

        arq = [f.strip() for f in arq]

        n = Nota(None, None, None, None, None, None, arq)
    
        print(n.getNegociacoes(n.arq))
        print(n.getData(n.arq))
        print(n.getQuantidade(n.arq))
        print(n.getValorTotal(n.arq))

        # n.getNegociacoes(n.arq)
        # n.getData(n.arq)
        # n.getQuantidade(n.arq)
        # n.getValorTotal(n.arq)

if __name__ == '__main__':
    lD = listarDiretorio()
    main(lD)