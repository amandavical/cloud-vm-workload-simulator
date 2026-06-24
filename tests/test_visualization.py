import unittest
from src.analysis.visualization import plotar_graficos_comparativos, imprimir_tabela_comparativa

class TestVisualization(unittest.TestCase):
    def test_visualization_stubs(self):
        with self.assertRaises(NotImplementedError):
            plotar_graficos_comparativos([])
            
        with self.assertRaises(NotImplementedError):
            imprimir_tabela_comparativa([])

if __name__ == "__main__":
    unittest.main()
