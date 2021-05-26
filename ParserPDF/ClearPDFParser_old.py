try:
    import pdfminer
    from subprocess import run
    from subprocess import DEVNULL
    from os import getcwd
    from os import listdir
except ImportError:
    print('Pacote pdfminer não foi encontrado, tente executar: pip3 install pdfminer')

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def listarDiretorio():
    itens = list(filter(lambda f: f.endswith('pdf'), listdir(getcwd())))
    for item in itens:
        if(item.endswith('pdf')):
            print(colors.OKBLUE + str(itens.index(item)+1) + '. ' + item + colors.ENDC)
    
    try:
        i = input(colors.WARNING + 'Qual arquivo deseja extrair informações? \n(digite -1 caso queira extrair todos os arquivos)?\n' + colors.ENDC)
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

def organizarPorEmpresa(todas):
    d_todas = dict({})
    print(colors.OKGREEN + 'Organizado:\n' + colors.ENDC)
    # Adiciona chaves
    for t in todas:
        if t[1] not in d_todas:
            d_todas.update({t[1]: []})

    # Adiciona negociações
    for t in todas:
        d_todas[t[1]].append('Ordem de {} de {} no dia {} pelo valor total R${}{}'.format(t[0], t[1], t[2], t[3], t[4]))
    
    for d in d_todas.keys():
        print(colors.WARNING + d + colors.ENDC)
        for i in d_todas[d]:
            print(colors.OKGREEN + '\t' + i + colors.ENDC)
        print('\n')
    
    return

def main():
    i_arq = listarDiretorio()
    
    todas_neg = []
    
    for i in i_arq:
        qnt_acoes = 0
        arr_acoes = []
        arq = []
        
        input_arq = str(i)[:-3]+'txt'
        run(['pdf2txt.py', '-o', input_arq, i], stdout=None, stderr=DEVNULL)
        with open(input_arq, 'r') as tempTxt:
            arq = tempTxt.readlines()

        # print(arq)
        arq = [f.strip() for f in arq]

        try:
            i = arq.index('Data pregão')+2
            data = arq[i]
        except ValueError:
            print(colors.FAIL + 'Campo \'Data pregão\' não encontrado!' + colors.ENDC)
            exit()

        qnt_acoes = arq.count('1-BOVESPA')
        
        try: 
            i = arq.index('D/C')+1
        except ValueError:
            print(colors.FAIL + 'Campo \'D/C\' não encontrado!' + colors.ENDC)
            exit()

        # Achar valor de compra
        for r in range(i, i+qnt_acoes):
            arr_acoes.append(arq[r].split(' '))

        posterior = ''

        # Achar ações (Empresa e Quantidade)
        i = arq.index('Valor Operação / Ajuste')+2
        for r in range(i, i+qnt_acoes):
            arr_acoes[i-r].append(data)
            # Empresa
            arr_acoes[i-r].append(arq[r].replace('    ', '').replace('ON', '').replace('NM','').strip())
            
            # Caso de ordem não confirmada no mesmo dia
            try:
                if type(int(arr_acoes[i-r][-1][0])==int):
                    arr_acoes[i-r].pop()
                    try:
                        especificacao = arq[arq.index('Prazo Especificação do título')+1] 
                    except:
                        especificacao = arq[arq.index('Especificação do título')+1]
                    arr_acoes[i-r].append(especificacao.replace('    ', '').replace('ON', '').replace('NM','').strip())
                    posterior = ', confirmada posteriormente'
            except:
                # print(arr_acoes[i-r])
                pass
                
            # Quantidade
            # print(float(arq[r+qnt_acoes+1].replace(',', '.')))

        # print(arr_acoes)

        d = dict({})
        for x in arr_acoes:
            op = 'venda' if x[1] == 'D' else 'compra'
            # print(x)
            d.update({x[3]: 'Ordem de {} de {} no dia {} pelo valor total R${}{}'.format(op, x[3], x[2], x[0], posterior)})
            todas_neg.append([op, x[3], x[2], x[0], posterior])

        # run(['rm', input_arq])
        
        # print(d)
    organizarPorEmpresa(todas_neg)
    return

if __name__ == '__main__':
    main()
