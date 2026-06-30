from typing import Any, Dict, List


def imprimir_tabela_comparativa(resultados: List[Dict[str, Any]]) -> None:
    """
    Imprime uma tabela comparativa com os resultados da simulação.
    """
    if not resultados:
        print("Nenhum resultado disponível para exibição.")
        return

    cabecalho = (
        f"{'VMs':>5} | "
        f"{'Algoritmo':<26} | "
        f"{'Makespan':>10} | "
        f"{'Espera Média':>13} | "
        f"{'Throughput':>10} | "
        f"{'Desvio Carga':>13}"
    )
    separador = "-" * len(cabecalho)

    print(separador)
    print(cabecalho)
    print(separador)

    for resultado in resultados:
        print(
            f"{resultado['num_vms']:>5} | "
            f"{resultado['algoritmo']:<26} | "
            f"{resultado['makespan']:>10.2f} | "
            f"{resultado['espera_media']:>13.2f} | "
            f"{resultado['throughput']:>10.4f} | "
            f"{resultado['desvio_carga']:>13.2f}"
        )

    print(separador)


def plotar_graficos_comparativos(
    resultados: List[Dict[str, Any]],
    caminho_imagem: str = "resultados_desempenho.png"
) -> None:
    """
    Gera gráficos comparativos das métricas da simulação e salva em disco.
    """
    if not resultados:
        return

    import matplotlib.pyplot as plt

    algoritmos = sorted({resultado["algoritmo"] for resultado in resultados})
    metricas = [
        ("makespan", "Makespan"),
        ("espera_media", "Tempo Médio de Espera"),
        ("throughput", "Throughput"),
        ("desvio_carga", "Desvio de Carga"),
    ]

    figura, eixos = plt.subplots(2, 2, figsize=(12, 8))
    eixos = eixos.flatten()

    for eixo, (chave_metrica, titulo) in zip(eixos, metricas):
        for algoritmo in algoritmos:
            dados_algoritmo = sorted(
                (
                    resultado
                    for resultado in resultados
                    if resultado["algoritmo"] == algoritmo
                ),
                key=lambda resultado: resultado["num_vms"],
            )

            eixo.plot(
                [resultado["num_vms"] for resultado in dados_algoritmo],
                [resultado[chave_metrica] for resultado in dados_algoritmo],
                marker="o",
                label=algoritmo,
            )

        eixo.set_title(titulo)
        eixo.set_xlabel("Quantidade de VMs")
        eixo.set_ylabel(titulo)
        eixo.grid(True, linestyle="--", alpha=0.4)
        eixo.legend()

    figura.tight_layout()
    figura.savefig(caminho_imagem)
    plt.close(figura)
