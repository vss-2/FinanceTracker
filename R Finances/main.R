library('quantmod')
library('jsonlite')

options(warn=-1)
#a = c()
#while(TRUE){
#    a = append(a, readline(prompt='Insira outra ação ou pressione ENTER para prosseguir:'))
#    print(a)
#    if(a == ""){
#      break
#    }
#}

ler_json = fromJSON(readLines(file(open="r", "acoes.json")))

preco_medio <- function(acoes, nome){
    acoes[[paste(nome, 'Preço médio', sep='')]] <- acoes[,3]/acoes[,4]
    # print(acoes)
}

dataset = preco_medio(ler_json, '')

for (acao in ler_json[,1]){ 
    if (!endsWith(acao, '.SA') ){
        acao = paste(acao, '.SA', sep='')
    }
    cat('---------------', acao, '---------------\n')
    env = new.env()
    bvsp = getSymbols(acao, src = "yahoo", env = env, from=as.Date('2021-05-01'), warnings=FALSE)
    k = names(env)[[1]]
    if(k == '.getSymbols'){
      k = names(env)[[2]]
    }
    acao = env[[k]]
    # print(acao)
    cat(c('Abertura mínima:', min(acao[,1])), '\n')
    cat(c('Abertura recente (em relação ao min):', acao[length(acao[,1])][,1][[1]]-min(acao[,1]), '\n'))
    cat(c('Média de abertura:', mean(acao[,1])), '\n')
    cat(c('Abertura máxima:', max(acao[,1])), '\n')
    cat('-----------------------------------', '\n')
    cat(c('Fechamento mínima:', min(acao[,2])), '\n')
    cat(c('Fechamento recente (em relação ao min.):', acao[length(acao[,2])][,2][[1]]-min(acao[,2]), '\n'))
    cat(c('Média de fechamento:', mean(acao[,2])), '\n')
    cat(c('Fechamento máxima:', max(acao[,2])), '\n')
    cat('\n')
}