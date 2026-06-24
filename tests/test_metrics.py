import unittest
from src.core.models import Processo, VM
from src.analysis.metrics import (
    calcular_makespan,
    calcular_tempo_espera_medio,
    calcular_throughput,
    calcular_desvio_carga
)

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.vms = [
            VM(id=0, tempo_total_execucao=12.0),
            VM(id=1, tempo_total_execucao=8.0)
        ]
        self.vms[0].fila_processos = [Processo(id=1, tempo_execucao=6), Processo(id=2, tempo_execucao=4)]
        self.vms[1].fila_processos = [Processo(id=3, tempo_execucao=6)]

    def test_makespan(self):
        try:
            m = calcular_makespan(self.vms)
            self.assertEqual(m, 12.0)
        except NotImplementedError:
            self.skipTest("Trabalho do Integrante 4 (Makespan) ainda não implementado.")

    def test_tempo_espera_medio(self):
        try:
            esp = calcular_tempo_espera_medio(self.vms, total_processos=3)
            self.assertEqual(esp, 2.0)
        except NotImplementedError:
            self.skipTest("Trabalho do Integrante 4 (Espera Média) ainda não implementado.")

    def test_throughput(self):
        try:
            tp = calcular_throughput(self.vms, total_processos=3)
            self.assertEqual(tp, 0.25)
        except NotImplementedError:
            self.skipTest("Trabalho do Integrante 4 (Throughput) ainda não implementado.")

    def test_desvio_carga(self):
        try:
            d = calcular_desvio_carga(self.vms)
            self.assertAlmostEqual(d, 2.8284, places=4)
        except NotImplementedError:
            self.skipTest("Trabalho do Integrante 4 (Desvio Carga) ainda não implementado.")

if __name__ == "__main__":
    unittest.main()
