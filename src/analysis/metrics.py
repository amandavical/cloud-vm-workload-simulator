from math import sqrt
from typing import List

from src.core.models import VM


def calcular_makespan(vms: List[VM]) -> float:
    """
    Calcula o tempo total da simulação.

    O makespan é o maior tempo de execução entre todas as VMs.
    """
    if not vms:
        return 0.0

    return max(vm.tempo_total_execucao for vm in vms)


def calcular_tempo_espera_medio(vms: List[VM], total_processos: int) -> float:
    """
    Calcula o tempo médio de espera dos processos nas filas das VMs.

    Como o simulador usa modelo analítico acumulado, a espera de cada processo
    é a soma dos tempos dos processos anteriores na mesma fila FIFO.
    """
    if total_processos <= 0:
        return 0.0

    espera_total = 0.0

    for vm in vms:
        tempo_acumulado = 0.0

        for processo in vm.fila_processos:
            espera_total += tempo_acumulado
            tempo_acumulado += processo.tempo_execucao

    return espera_total / total_processos


def calcular_throughput(vms: List[VM], total_processos: int) -> float:
    """
    Calcula a vazão da simulação em processos concluídos por unidade de tempo.
    """
    makespan = calcular_makespan(vms)

    if total_processos <= 0 or makespan <= 0:
        return 0.0

    return total_processos / makespan


def calcular_desvio_carga(vms: List[VM]) -> float:
    """
    Calcula o desvio padrão amostral da carga alocada entre as VMs.

    A carga de uma VM é a soma dos tempos de execução dos processos em sua fila.
    """
    if len(vms) < 2:
        return 0.0

    cargas = [
        sum(processo.tempo_execucao for processo in vm.fila_processos)
        for vm in vms
    ]
    media = sum(cargas) / len(cargas)
    variancia_amostral = sum((carga - media) ** 2 for carga in cargas) / (len(cargas) - 1)

    return sqrt(variancia_amostral)
