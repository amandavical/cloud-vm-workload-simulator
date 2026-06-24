from typing import List, Dict, Any, Optional
import random
from src.core.models import Processo

def define_workload_scenarios() -> Dict[str, Dict[str, Any]]:
    """
    Define os cenários de carga de trabalho (workload) do simulador.
    
    Cenários suportados:
    - leve: 50 processos
    - media: 200 processos
    - pesada: 500 processos
    
    Retorna:
        Dict[str, Dict[str, Any]]: Dicionário com as configurações dos cenários.
    """
    return {
        "leve": {
            "quantity": 50,
            "tempo_execucao_min": 1,
            "tempo_execucao_max": 100,
            "uso_cpu_min": 1,
            "uso_cpu_max": 100
        },
        "media": {
            "quantity": 200,
            "tempo_execucao_min": 1,
            "tempo_execucao_max": 100,
            "uso_cpu_min": 1,
            "uso_cpu_max": 100
        },
        "pesada": {
            "quantity": 500,
            "tempo_execucao_min": 1,
            "tempo_execucao_max": 100,
            "uso_cpu_min": 1,
            "uso_cpu_max": 100
        }
    }

def generate_processes(quantity: Optional[int] = None, cenario: str = "media", seed: Optional[int] = None) -> List[Processo]:
    """
    Gera uma lista de processos com identificadores únicos, tempos de execução
    e uso de CPU dentro de faixas realistas (1 a 100).
    
    Parâmetros:
        quantity: Número exato de processos a serem gerados.
        cenario: Nome do cenário de carga ("leve", "media"/"média", "pesada").
                 Usado apenas se quantity não for fornecido.
        seed: Semente opcional para geração determinística (reprodutível).
        
    Retorna:
        List[Processo]: Lista de objetos do tipo Processo gerados.
    """
    # Define as configurações padrão dos cenários
    cenarios = define_workload_scenarios()
    
    # Normalização do nome do cenário para ignorar diferenças de maiúsculas/minúsculas e acentuação
    cenario_normalizado = "media"
    if cenario:
        cenario_normalizado = cenario.lower().replace("á", "a")
    
    # Determinar a quantidade de processos a gerar
    qtde_final = quantity
    if qtde_final is None:
        if cenario_normalizado in cenarios:
            qtde_final = cenarios[cenario_normalizado]["quantity"]
        else:
            # Caso o cenário seja desconhecido, cai para o padrão "media" (200 processos)
            qtde_final = cenarios["media"]["quantity"]
            
    # Obter limites para os valores gerados
    conf_limites = cenarios.get(cenario_normalizado, cenarios["media"])
    
    t_min = conf_limites.get("tempo_execucao_min", 1)
    t_max = conf_limites.get("tempo_execucao_max", 100)
    cpu_min = conf_limites.get("uso_cpu_min", 1)
    cpu_max = conf_limites.get("uso_cpu_max", 100)
    
    # Configurar gerador pseudo-aleatório local
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()
        
    processos = []
    for i in range(qtde_final):
        tempo_exec = rng.randint(t_min, t_max)
        uso_cpu = rng.randint(cpu_min, cpu_max)
        # ID do processo começa em i para garantir unicidade simples no lote
        processos.append(
            Processo(
                id=i,
                tempo_execucao=tempo_exec,
                tempo_chegada=0,
                uso_cpu=uso_cpu
            )
        )
        
    return processos
