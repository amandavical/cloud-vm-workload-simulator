import copy
import sys
from typing import List, Dict, Any

from src.simulation.workload import generate_processes
from src.simulation.cloud import Cloud
from src.analysis.metrics import (
    calcular_makespan,
    calcular_tempo_espera_medio,
    calcular_throughput,
    calcular_desvio_carga
)
from src.analysis.visualization import imprimir_tabela_comparativa, plotar_graficos_comparativos

def executar_simulador():
    """
    Ponto central de integração e orquestração do experimento (Líder Técnico).
    Coordenará a chamada aos submódulos para rodar os diferentes cenários.
    """
    print("Iniciando Simulação Simplificada de Nuvem...")
    
    # Configurações do Experimento
    config_vms = [1, 2, 4, 8, 16]
    quantidade_processos = 200
    cenario_carga = "media"
    
    resultados: List[Dict[str, Any]] = []
    
    try:
        # 1. Módulo Geração de Carga (Integrante 2)
        processos_originais = generate_processes(quantity=quantidade_processos, cenario=cenario_carga, seed=42)
        print(f"Carga única de {len(processos_originais)} processos gerada.")
        
        # Cenários de Escalonamento (Integrante 3)
        algoritmos = ["Round Robin", "Menor Fila (Least Loaded)"]
        
        for algoritmo in algoritmos:
            for num_vms in config_vms:
                # Copiar os processos para garantir o mesmo estado inicial
                processos = copy.deepcopy(processos_originais)
                
                # 2. Módulo Nuvem & Escalonamento & Execução (Integrante 3)
                nuvem = Cloud(quantidade_vms=num_vms, capacidade_vms=1.0, overhead_vms=2.0)
                
                # Escalonamento
                if algoritmo == "Round Robin":
                    nuvem.escalonar_round_robin(processos)
                else:
                    nuvem.escalonar_menor_fila(processos)
                    
                # Execução
                nuvem.executar_simulacao()

                # 3. Módulo Métricas (Integrante 4)
                makespan = calcular_makespan(nuvem.vms)
                espera_media = calcular_tempo_espera_medio(nuvem.vms, len(processos_originais))
                throughput = calcular_throughput(nuvem.vms, len(processos_originais))
                desvio = calcular_desvio_carga(nuvem.vms)

                # Armazenamento de resultados
                resultados.append({
                    "num_vms": num_vms,
                    "algoritmo": algoritmo,
                    "makespan": makespan,
                    "espera_media": espera_media,
                    "throughput": throughput,
                    "desvio_carga": desvio
                })

        # 4. Módulo Visualização (Integrante 4)
        imprimir_tabela_comparativa(resultados)
        plotar_graficos_comparativos(resultados, caminho_imagem="resultados_desempenho.png")

        print("Experimento finalizado com sucesso!")
        
    except NotImplementedError as e:
        print(f"\n[INTEGRAÇÃO] Execução pausada: módulo incompleto detectado.", file=sys.stderr)
        print(f"  -> {e}", file=sys.stderr)
        print("Cada integrante do grupo deve preencher sua respectiva lógica TODO para rodar por completo.", file=sys.stderr)
    except Exception as e:
        print(f"[ERRO] Erro crítico no simulador: {e}", file=sys.stderr)


if __name__ == "__main__":
    executar_simulador()
