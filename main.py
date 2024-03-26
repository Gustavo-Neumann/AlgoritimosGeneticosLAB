import random

# Tabela de restrições
restricoes = {
    "Analise 1": ["Espectrofotômetro UV-VIS", "Cromatógrafo Gasoso"],
    "Analise 2": ["Cromatógrafo Líquido", "Espectrômetro Infravermelho"],
    "Analise 3": ["Microscópio", "Balança Analítica"],
    "Analise 4": ["Espectrômetro de Massa"],
    "Analise 5": ["Agitador Magnético", "Espectrômetro Infravermelho"],
    "Analise 6": ["Cromatógrafo Líquido", "Espectrofotômetro UV-VIS"],
    "Analise 7": ["Espectrofotômetro UV-VIS", "Microscópio"],
    "Analise 8": ["Cromatógrafo Gasoso"],
    "Analise 9": ["Espectrômetro Infravermelho", "Balança Analítica"],
    "Analise 10": ["Espectrômetro de Massa", "Cromatógrafo Gasoso"]
}

restricoes_max_horas = {
    "Balança Analítica": 6,
    "Agitador Magnético": 4,
    "Cromatógrafo Líquido": 8,
    "Cromatógrafo Gasoso": 6,
    "Espectrofotômetro UV-VIS": 4,
    "Espectrômetro Infravermelho": 6,
    "Espectrômetro de Massa": 4,
    "Microscópio": 6
}

EQUIP_DIA = {
    "Balança Analítica": {"hora": 0, "analise": " "},
    "Agitador Magnético": {"hora": 0, "analise": " "},
    "Cromatógrafo Líquido": {"hora": 0, "analise": " "},
    "Cromatógrafo Gasoso": {"hora": 0, "analise": " "},
    "Espectrofotômetro UV-VIS": {"hora": 0, "analise": " "},
    "Espectrômetro Infravermelho": {"hora": 0, "analise": " "},
    "Espectrômetro de Massa": {"hora": 0, "analise": " "},
    "Microscópio": {"hora": 0, "analise": " "},
}

def gerar_individuo(restricoes, equip_dia):
    # Inicializar uma solução no formato EQUIP_DIA
    solucao = equip_dia.copy()
    # Criar uma lista de equipamentos
    equipamentos = list(equip_dia.keys())
    equipamento_em_uso = []

    # Embaralhar a ordem dos equipamentos
    random.shuffle(equipamentos)

    # Iterar sobre as análises e alocar um equipamento para cada uma, respeitando as restrições
    for analise, equipamentos_necessarios in restricoes.items():
        for equipamento in equipamentos:
            if equipamento in equipamentos_necessarios and equipamento not in equipamento_em_uso:
                equipamento_em_uso.append(equipamento)
                solucao[equipamento]["analise"] = analise
                break
        else:
            solucao[equipamento]["analise"] = "0"
    for equipamento in equipamentos:
        solucao[equipamento]["hora"] += 1

    return solucao

def gerar_individuo1(restricoes, equip_dia):
    # Inicializar uma solução no formato EQUIP_DIA
    solucao = equip_dia.copy()
    
    # Criar uma lista de equipamentos
    equipamentos = list(equip_dia.keys())
    
    # Embaralhar a ordem dos equipamentos
    random.shuffle(equipamentos)
    
    # Embaralhar a ordem das análises
    analises_disponiveis = list(restricoes.keys())
    random.shuffle(analises_disponiveis)
    
    # Atribuir uma análise aleatória para cada equipamento
    for equipamento in equipamentos:
        # Selecionar uma análise aleatória
        analise_aleatoria = random.choice(analises_disponiveis)
        solucao[equipamento]["analise"] = analise_aleatoria
        
        # Remover a análise selecionada das análises disponíveis
        analises_disponiveis.remove(analise_aleatoria)
    for equipamento in equipamentos:
        solucao[equipamento]["hora"] += 1
    return solucao

def fitness(sol):
    # Definir o valor máximo de fitness
    max_fitness = len(restricoes) * 1  # Total de análises multiplicado pelo número máximo de horas
    
    # Inicializar o fitness atual
    current_fitness = 0
    
    # Contar o número de análises distintas realizadas em todos os equipamentos
    analises_realizadas = set()
    equipamentos_corretos = set()
    for equipamento, dados in sol.items():
        # Verificar se o equipamento não excedeu o tempo máximo de uso por dia
        if len(dados["analise"]) > 1:
            if equipamento in restricoes[dados["analise"]]:
                if dados["hora"] <= restricoes_max_horas[equipamento]:
                # Verificar se uma análise foi atribuída ao equipamento
                    if dados["analise"] != " ":
                        analises_realizadas.add(dados["analise"])
        else:
            pass       
                
                    
    # Calcular o fitness atual
    current_fitness = len(analises_realizadas) + len(equipamentos_corretos)
    
    # Normalizar o fitness para estar entre 0 e 1
    normalized_fitness = current_fitness / max_fitness
    
    return normalized_fitness



def mutacao(individuo):
    # Selecionar aleatoriamente dois equipamentos distintos
    equipamentos = list(individuo.keys())
    equipamento1, equipamento2 = random.sample(equipamentos, 2)
    
    # Trocar as análises entre os dois equipamentos
    individuo[equipamento1]["analise"], individuo[equipamento2]["analise"] = individuo[equipamento2]["analise"], individuo[equipamento1]["analise"]
    
    return individuo

# Gerar uma solução inicial
individuo = gerar_individuo1(restricoes, EQUIP_DIA)


# Imprimir a tabela da solução inicial
print("Equipamento\tHoras\tAnálise")
for equipamento, dados in individuo.items():
    print(f"{equipamento}\t{dados['hora']}\t\t{dados['analise']}")
print("\n\n")


print(fitness(individuo))    
