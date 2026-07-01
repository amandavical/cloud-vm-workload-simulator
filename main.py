import argparse
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
from src.analysis.visualization import (
    imprimir_tabela_comparativa,
    plotar_graficos_comparativos
)


CENARIOS_QUATRO_GRAFICOS = [
    ("media", 200),
    ("media", 1000),
    ("pesada", 200),
    ("pesada", 1000),
]


def quantidade_positiva(valor: str) -> int:
    """
    Valida o argumento de quantidade informado pela linha de comando.
    """
    quantidade = int(valor)

    if quantidade <= 0:
        raise argparse.ArgumentTypeError("a quantidade deve ser maior que zero")

    return quantidade


def nome_arquivo_resultado(cenario_carga: str, quantidade_processos: int) -> str:
    """
    Monta o nome do arquivo de gráfico para um cenário de carga.
    """
    return f"resultados_{cenario_carga}_{quantidade_processos}.png"


def executar_experimento(cenario_carga: str, quantidade_processos: int) -> None:
    """
    Ponto central de integração e orquestração do experimento (Líder Técnico).
    Coordenará a chamada aos submódulos para rodar os diferentes cenários.
    """
    print(
        "[Líder Técnico] Iniciando Simulação Simplificada de Nuvem "
        f"({cenario_carga}, {quantidade_processos} processos)..."
    )
    
    # Configurações do Experimento
    config_vms = [1, 2, 4, 8, 16]
    
    resultados: List[Dict[str, Any]] = []
    
    try:
        # 1. Módulo Geração de Carga (Integrante 2)
        processos_originais = generate_processes(quantity=quantidade_processos, cenario=cenario_carga)
        print(f"[Orquestrador] Carga única de {len(processos_originais)} processos gerada.")
        
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
        caminho_imagem = nome_arquivo_resultado(cenario_carga, quantidade_processos)

        imprimir_tabela_comparativa(resultados)
        plotar_graficos_comparativos(resultados, caminho_imagem=caminho_imagem)

        print(f"[Líder Técnico] Gráfico salvo em: {caminho_imagem}")
        print("[Líder Técnico] Experimento finalizado com sucesso!")
        
    except NotImplementedError as e:
        print(f"\n[INTEGRAÇÃO] Execução pausada: módulo incompleto detectado.", file=sys.stderr)
        print(f"  -> {e}", file=sys.stderr)
        print("Cada integrante do grupo deve preencher sua respectiva lógica TODO para rodar por completo.", file=sys.stderr)
    except Exception as e:
        print(f"[ERRO] Erro crítico no simulador: {e}", file=sys.stderr)


def criar_parser() -> argparse.ArgumentParser:
    """
    Cria o parser de argumentos da linha de comando.
    """
    parser = argparse.ArgumentParser(
        description="Executa a simulação de cargas em VMs e gera gráficos comparativos."
    )
    parser.add_argument(
        "--cenario",
        choices=["leve", "media", "pesada"],
        default="media",
        help="Cenário de carga usado para gerar os processos."
    )
    parser.add_argument(
        "--quantidade",
        type=quantidade_positiva,
        default=200,
        help="Quantidade de processos gerados para o experimento."
    )
    parser.add_argument(
        "--gerar-quatro",
        action="store_true",
        help="Gera os gráficos para media/pesada com 200 e 1000 processos."
    )

    return parser


def executar_simulador() -> None:
    """
    Interpreta argumentos de linha de comando e executa um ou mais experimentos.
    """
    parser = criar_parser()
    args = parser.parse_args()

    if args.gerar_quatro:
        for cenario_carga, quantidade_processos in CENARIOS_QUATRO_GRAFICOS:
            executar_experimento(cenario_carga, quantidade_processos)
        return

    executar_experimento(args.cenario, args.quantidade)


if __name__ == "__main__":
    executar_simulador()
