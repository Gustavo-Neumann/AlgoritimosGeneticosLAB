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



def gerar_individuo_aleatorio():
    individuo = {}
    for i in range(1, num_instancias + 1):
        analises_disponiveis = list(restricoes.keys())
        analises_disponiveis.append("0")
        for equipamento in equipamentos:
            chave = f"{equipamento} {i}"
            analise_aleatoria = random.choice(analises_disponiveis)
            analises_disponiveis.remove(analise_aleatoria)  # Remove para evitar repetição
            individuo[chave] = analise_aleatoria

    return individuo

def fitness(individuo):
    fitness_score = 0
    punicao = 0
    
    # Dicionário para contar o uso de cada equipamento
    uso_equipamento = {equipamento: 0 for equipamento in equipamentos}
    
    # Conjunto para rastrear as análises alocadas em cada hora
    analises_por_hora = set()

    for chave, analise in individuo.items():
        equipamento, indice = chave.split(" ")
        indice = int(indice)
        
        # Incrementa o uso do equipamento
        uso_equipamento[equipamento] += 1
        
        # Verifica se a capacidade máxima do equipamento foi excedida
        if uso_equipamento[equipamento] > restricoes_max_horas[equipamento] and individuo[chave] != "0":
            punicao += 200  
        
        # Verifica se a análise está sendo repetida na mesma hora
        if analise != '0':  
            if (analise, indice) in analises_por_hora:
                punicao += 100  
            else:
                analises_por_hora.add((analise, indice))
            
            # Verifica se o equipamento é apropriado para a análise
            if analise in restricoes and equipamento not in restricoes[analise]:
                punicao += 100  # Equipamento não apropriado para a análise
                
    # Calcula o fitness base no cumprimento das restrições, subtraindo as punições
    fitness_score = 10000 - punicao  # Inicia com uma pontuação alta e subtrai as punições
    
    return fitness_score


def mutacao(individuo):
    
    analises = list(restricoes.keys())
    analises.append("0")
    analise_aleatoria = random.choice(analises)
    equipamentos = list(individuo.keys())
    equipamento_aleatorio = random.choice(equipamentos)
    
    individuo[equipamento_aleatorio] = analise_aleatoria
    return individuo

def crossover(individuo1, individuo2):
    filho = {}
    for equipamento, analise1 in individuo1.items():
        analise2 = individuo2.get(equipamento)
        if analise2 is not None and random.random() < 0.5:
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
            if random.random() < 0.4:  # Chance de mutaçãoS
                filho = mutacao(filho)
               
            populacao.append(filho)

    melhor_individuo = max(populacao, key=lambda ind: fitness(ind))
    return melhor_individuo

for i in range(1, 8):
    melhor_individuo = algoritmo_genetico(100, 1000, 2)
    print(f"EQUIPAMENTO\t\t ANALISE\t\t DIA {i} ")
    for equipamento, dados in melhor_individuo.items():
        print(f"{equipamento}\t{dados}")
    print(f"\nFitness dia {i}: {fitness(melhor_individuo)}\n")