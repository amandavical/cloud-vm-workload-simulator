import unittest
import tempfile
from pathlib import Path

from src.analysis.visualization import plotar_graficos_comparativos, imprimir_tabela_comparativa

class TestVisualization(unittest.TestCase):
    def test_imprimir_tabela_comparativa(self):
        resultados = [{
            "num_vms": 1,
            "algoritmo": "Round Robin",
            "makespan": 12.0,
            "espera_media": 2.0,
            "throughput": 0.25,
            "desvio_carga": 0.0
        }]

        imprimir_tabela_comparativa(resultados)

    def test_plotar_graficos_comparativos(self):
        resultados = [
            {
                "num_vms": 1,
                "algoritmo": "Round Robin",
                "makespan": 12.0,
                "espera_media": 2.0,
                "throughput": 0.25,
                "desvio_carga": 0.0
            },
            {
                "num_vms": 2,
                "algoritmo": "Round Robin",
                "makespan": 8.0,
                "espera_media": 1.0,
                "throughput": 0.375,
                "desvio_carga": 2.0
            }
        ]

        with tempfile.TemporaryDirectory() as diretorio:
            caminho_imagem = Path(diretorio) / "grafico.png"

            plotar_graficos_comparativos(resultados, caminho_imagem=str(caminho_imagem))

            self.assertTrue(caminho_imagem.exists())

if __name__ == "__main__":
    unittest.main()
