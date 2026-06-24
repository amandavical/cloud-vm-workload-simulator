from dataclasses import dataclass, field
from typing import List

@dataclass
class Processo:
    """
    Representa uma carga de trabalho (processo) individual.
    
    Campos:
        id: Identificador único do processo (PID).
        tempo_execucao: Tempo de CPU necessário para concluir a tarefa (ciclos ou segundos).
        tempo_chegada: Instante em que o processo chega ao sistema (padrão é 0).
    """
    id: int
    tempo_execucao: int
    tempo_chegada: int = 0
    uso_cpu: int = 100


@dataclass
class VM:
    """
    Representa uma Máquina Virtual (VM) simulada.
    
    Campos:
        id: Identificador único da VM (VID).
        capacidade_processamento: Multiplicador de velocidade (ex: 2.0 processa duas vezes mais rápido).
        overhead_virtualizacao: Tempo fixo de overhead do hipervisor para esta VM.
        fila_processos: Lista de processos atualmente alocados para rodar nesta VM.
        tempo_total_execucao: Tempo total final que esta VM levou para terminar sua fila.
    """
    id: int
    capacidade_processamento: float = 1.0
    overhead_virtualizacao: float = 2.0
    fila_processos: List[Processo] = field(default_factory=list)
    tempo_total_execucao: float = 0.0
