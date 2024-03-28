import random

# Tabela de restrições
restricoes = {
    "Analise 1": ["EspectrofotômetroUV-VIS", "CromatógrafoGasoso"],
    "Analise 2": ["CromatógrafoLíquido", "EspectrômetroInfravermelho"],
    "Analise 3": ["Microscópio", "BalançaAnalítica"],
    "Analise 4": ["EspectrômetrodeMassa"],
    "Analise 5": ["AgitadorMagnético", "EspectrômetroInfravermelho"],
    "Analise 6": ["CromatógrafoLíquido", "EspectrofotômetroUV-VIS"],
    "Analise 7": ["EspectrofotômetroUV-VIS", "Microscópio"],
    "Analise 8": ["CromatógrafoGasoso"],
    "Analise 9": ["EspectrômetroInfravermelho", "BalançaAnalítica"],
    "Analise 10": ["EspectrômetrodeMassa", "CromatógrafoGasoso"]
}

restricoes_max_horas = {
    "BalançaAnalítica": 6,
    "AgitadorMagnético": 4,
    "CromatógrafoLíquido": 8,
    "CromatógrafoGasoso": 6,
    "EspectrofotômetroUV-VIS": 4,
    "EspectrômetroInfravermelho": 6,
    "EspectrômetrodeMassa": 4,
    "Microscópio": 6
}


EQUIP_DIA = {}
num_instancias = 8  # Número de instâncias desejadas para cada equipamento

equipamentos = [
    "BalançaAnalítica",
    "AgitadorMagnético",
    "CromatógrafoLíquido",
    "CromatógrafoGasoso",
    "EspectrofotômetroUV-VIS",
    "EspectrômetroInfravermelho",
    "EspectrômetrodeMassa",
    "Microscópio"
]

for equipamento in equipamentos:
    for i in range(1, num_instancias + 1):
        chave = f"{equipamento} {i}"
        EQUIP_DIA[chave] = ""

def verificar_analises_iguais(individuo):
    analises_por_indice = {}

    for chave, analises in individuo.items():
        equipamento, indice = chave.split()
        
        if indice not in analises_por_indice:
            analises_por_indice[indice] = set()
        
        # Verifica se alguma análise deste equipamento e índice já ocorreu
        for analise in analises:
            if analise in analises_por_indice[indice]:
                return True
            else:
                analises_por_indice[indice].add(analise)

def gerar_individuo_aleatorio():
    individuo = EQUIP_DIA
    analises = list(restricoes.keys())
    for equipamento, info in individuo.items():
        analise_aleatoria = random.choice(analises)
        for _ in restricoes.items():
            individuo[equipamento] = {analise_aleatoria}



    # for equipamento, info in individuo.items():
    #     if equipamento.split()[0] == "BalançaAnalítica" and int(equipamento.split()[1]) > 6:
    #         individuo[equipamento] = {"0"}
            
    # For para respeitar as condicoes de horas        
    for equipamento in equipamentos:
        for i in range(1, num_instancias + 1):
            chave = f"{equipamento} {i}"
            if equipamento == "BalançaAnalítica" and i > 6:
                individuo[chave] = {"0"}
            elif equipamento == "AgitadorMagnético" and i > 4:
                individuo[chave] = {"0"}
            elif equipamento == "CromatógrafoLíquido" and i > 8:
                individuo[chave] = {"0"}
            elif equipamento == "CromatógrafoGasoso" and i > 6:
                individuo[chave] = {"0"}
            elif equipamento == "EspectrofotômetroUV-VIS" and i > 4:
                individuo[chave] = {"0"}
            elif equipamento == "EspectrômetroInfravermelho" and i > 6:
                individuo[chave] = {"0"}
            elif equipamento == "EspectrômetrodeMassa" and i > 4:
                individuo[chave] = {"0"}
            elif equipamento == "Microscópio" and i > 6:
                individuo[chave] = {"0"}


    return individuo

def fitness(individuo):
    fitness_restricao_analises = 0

    # for analise, equipamentos_necessarios in restricoes.items():
    #     for equipamento_necessario in equipamentos_necessarios:
    #         equipamento_encontrado = False
    #         for equipamento, info in individuo.items():

    #             if equipamento_necessario in equipamento:
    #                 equipamento_encontrado = True
    #                 break
    #         if not equipamento_encontrado:
    #             penalidade += 1  # Incrementa a penalidade se o equipamento necessário não estiver presente

    for equipamento, analise in individuo.items():
        for analise_res, equipamentos_necessarios in restricoes.items():
            if analise == {analise_res}:
                if equipamento.split(" ")[0] in equipamentos_necessarios:
                    fitness_restricao_analises +=1

    return fitness_restricao_analises


def mutacao(individuo):
    
    analises = list(restricoes.keys())
    analise_aleatoria = random.choice(analises)
    equipamentos = list(EQUIP_DIA.keys())
    equipamento_aleatorio = random.choice(equipamentos)
    if individuo[equipamento_aleatorio] != {"0"}:
        individuo[equipamento_aleatorio] = {analise_aleatoria}
    return individuo

def crossover(individuo1, individuo2):
    filho = {}
    for equipamento, analise1 in individuo1.items():
        analise2 = individuo2.get(equipamento)
        if analise2 is not None and random.random() < 0.5 and individuo1[equipamento] != {"0"} and individuo2[equipamento] != {"0"}:
            filho[equipamento] = analise2
        else:
            filho[equipamento] = analise1
    return filho

def selecao_torneio(populacao, num_a_manter, tamanho_torneio):
    selecionados = []
    for _ in range(num_a_manter):
        torneio = random.sample(populacao, tamanho_torneio)
        vencedor = max(torneio, key=lambda ind: fitness(ind))
        selecionados.append(vencedor)
    return selecionados

def algoritmo_genetico(tamanho_populacao, geracoes, tamanho_torneio):
    populacao = [gerar_individuo_aleatorio() for _ in range(tamanho_populacao)]
    for _ in range(geracoes):
        populacao = selecao_torneio(populacao, tamanho_populacao // 2, tamanho_torneio)
        while len(populacao) < tamanho_populacao:
            pai1 = random.choice(populacao)
            pai2 = random.choice(populacao)
            filho = crossover(pai1, pai2)
            if random.random() < 0.1:  # Chance de mutaçãoS
                filho = mutacao(filho)
               
            populacao.append(filho)

    melhor_individuo = max(populacao, key=lambda ind: fitness(ind))
    return melhor_individuo

individuo = gerar_individuo_aleatorio()
print(individuo)
print(fitness(individuo))
melhor_individuo = algoritmo_genetico(100, 1000, 2)
print(melhor_individuo)
print(fitness(melhor_individuo))
print("EQUIPAMENTO\t\t ANALISE")
for equipamento, dados in melhor_individuo.items():
    print(f"{equipamento}\t{dados}")
