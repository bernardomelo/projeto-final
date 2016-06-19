
import sys
import re

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''    
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result



def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))
                    
def StopWords(fname):
    arq = open(fname,'r')
    stopWords = arq.readlines()
    return stopWords

def readTrainingSet(fname):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''
    stopWords = StopWords(#caminho das stopwords aqui)
    score = 0
    words = dict()
    temp = []
    arq = open(fname,'r')
    for line in arq:
        linha = split_on_separators(line, ' ')
        for x in linha:
            if x == '0' or x =='1' or x == '2' or x == '3' or x == '4':
                score = int(x)
                continue
            palavra = clean_up(x)
            if palavra in temp:
                for i in words.keys():
                    if i[0] == palavra:
                        words[(palavra, int(i[1]+1),int(i[2]+score))] = words[i]
                        del words[i]
                        break
            else:
                if palavra not in stopWords:
                    temp.append(palavra)
                    words[(palavra, 1, score)] = 0
    arq.close()

    for x in words.keys():
        words[x] = x[2]/x[1]
        
    return words

def readTestSet(fname):
    reviews = []
    arq = open(fname,'r')
    for line in arq:
        reviews.append((int(line[0]),line[1:-1]))
    arq.close()
    return reviews

def computeSentiment(review,words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''
    score = 0.0
    count = 0
    s = split_on_separators(review,' ')
    for i in s:
        palavra = clean_up(i)
        for p in words.keys():
            if p[0] == palavra:
                score += p[2]
                count += 1
            else:
                score += 2
                count += 1
    return score/count

def computeSumSquaredErrors(reviews,words):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''    
    sse = 0
    final = 0
    for line in reviews:
        sentiment = computeSentiment(line[1],words)
        if line[0] != sentiment:
            diference = float(line[0]) - sentiment
            result = diference**2
            final += result
            sse = final / len(reviews)
    return sse

    
def main():
    
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (e' parte do
    # projeto).
    
    # A ordem dos parametros e' a seguinte: o primeiro e' o nome do arquivo
    # com o conjunto de treinamento, em seguida o arquivo do conjunto de teste.
    
    if len(sys.argv) < 3:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        sys.exit(0)

    # Lendo conjunto de treinamento e computando escore das palavras
    words = readTrainingSet(sys.argv[1])
    
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    
    # Inferindo sentimento e computando soma dos quadrados dos erros
    sse = computeSumSquaredErrors(reviews,words)
    
    print( 'A soma do quadrado dos erros e\': {0}'.format(sse))
            

if __name__ == '__main__':
   main()
    
    
