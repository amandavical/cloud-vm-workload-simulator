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
        # CONFIGURAÇÃO DE TESTE COMUM (Roda antes de cada caso de teste abaixo)
        # VM 0: levou 12.0 segundos no total. Fila: P1 (tempo=6), P2 (tempo=4)
        # VM 1: levou 8.0 segundos no total. Fila: P3 (tempo=6)
        self.vms = [
            VM(id=0, tempo_total_execucao=12.0),
            VM(id=1, tempo_total_execucao=8.0)
        ]
        # P1 e P2 na VM 0 (VM 0 tem velocidade padrão de 1.0)
        self.vms[0].fila_processos = [Processo(id=1, tempo_execucao=6), Processo(id=2, tempo_execucao=4)]
        # P3 na VM 1 (VM 1 tem velocidade padrão de 1.0)
        self.vms[1].fila_processos = [Processo(id=3, tempo_execucao=6)]

    def test_makespan(self):
        # OBJETIVO: Garantir que o Makespan seja o tempo da VM mais lenta (gargalo do sistema)
        m = calcular_makespan(self.vms)
        
        # CÁLCULO ESPERADO:
        # VM 0 levou 12.0s. VM 1 levou 8.0s.
        # O Makespan (tempo total do banco terminar) deve ser o maior deles: 12.0s
        self.assertEqual(m, 12.0)

    def test_tempo_espera_medio(self):
        # OBJETIVO: Testar se a média de tempo de fila dos processos está correta
        esp = calcular_tempo_espera_medio(self.vms, total_processos=3)
        
        # CÁLCULO ESPERADO:
        # VM 0:
        #   - P1 (ID 1) é o primeiro. Espera = 0.0s
        #   - P2 (ID 2) é o segundo. Espera = tempo do P1 = 6.0s (pois a VM tem velocidade 1.0)
        # VM 1:
        #   - P3 (ID 3) é o primeiro. Espera = 0.0s
        # Soma total de esperas = 0 + 6.0 + 0 = 6.0 segundos
        # Média = Soma das esperas / total de processos (3) = 6.0 / 3 = 2.0 segundos
        self.assertEqual(esp, 2.0)

    def test_throughput(self):
        # OBJETIVO: Testar a vazão do sistema (processos concluídos por segundo)
        tp = calcular_throughput(self.vms, total_processos=3)
        
        # CÁLCULO ESPERADO:
        # Vazão = total de processos / Makespan
        # Vazão = 3 processos / 12.0 segundos = 0.25 processos por segundo
        self.assertEqual(tp, 0.25)

    def test_desvio_carga(self):
        # OBJETIVO: Testar se o cálculo estatístico de desvio padrão amostral está correto
        d = calcular_desvio_carga(self.vms)
        
        # CÁLCULO ESPERADO:
        # Carga da VM 0 (soma de processos) = 6 + 4 = 10
        # Carga da VM 1 (soma de processos) = 6
        # Cargas = [10, 6] -> Média das cargas = 8.0
        # Variância Amostral = ((10 - 8)^2 + (6 - 8)^2) / (N - 1)
        # Variância Amostral = (4 + 4) / 1 = 8.0
        # Desvio Padrão Amostral = Raiz quadrada de 8.0 = 2.828427...
        self.assertAlmostEqual(d, 2.8284, places=4)

if __name__ == "__main__":
    unittest.main()
