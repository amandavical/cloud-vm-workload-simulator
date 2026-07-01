import unittest
import tempfile
from pathlib import Path
from src.analysis.visualization import plotar_graficos_comparativos, imprimir_tabela_comparativa

class TestVisualization(unittest.TestCase):
    def test_imprimir_tabela_comparativa(self):
        # OBJETIVO: Garantir que a função de imprimir tabela no console funciona sem disparar exceções (erros)
        resultados = [{
            "num_vms": 1,
            "algoritmo": "Round Robin",
            "makespan": 12.0,
            "espera_media": 2.0,
            "throughput": 0.25,
            "desvio_carga": 0.0
        }]
        
        # Apenas chamamos a função. Se ela rodar sem levantar exceções, o teste é bem-sucedido
        imprimir_tabela_comparativa(resultados)

    def test_plotar_graficos_comparativos(self):
        # OBJETIVO: Garantir que a função plotar_graficos_comparativos gera o arquivo PNG do gráfico corretamente
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

        # Usamos uma pasta temporária (tempfile) para salvar a imagem do teste e não sujar a raiz do projeto
        with tempfile.TemporaryDirectory() as diretorio:
            caminho_imagem = Path(diretorio) / "grafico.png"

            # Gera o gráfico na pasta temporária
            plotar_graficos_comparativos(resultados, caminho_imagem=str(caminho_imagem))

            # Verifica se o arquivo PNG realmente foi criado fisicamente no disco
            self.assertTrue(caminho_imagem.exists())

if __name__ == "__main__":
    unittest.main()
