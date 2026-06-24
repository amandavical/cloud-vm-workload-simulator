import unittest
from src.core.models import Processo, VM
from src.simulation.cloud import Cloud

class TestCloud(unittest.TestCase):
    def test_inicializacao_vms(self):
        try:
            nuvem = Cloud(quantidade_vms=3, capacidade_vms=2.0, overhead_vms=4.0)
            self.assertEqual(len(nuvem.vms), 3)
            self.assertTrue(all(isinstance(v, VM) for v in nuvem.vms))
            self.assertTrue(all(v.capacidade_processamento == 2.0 for v in nuvem.vms))
            self.assertTrue(all(v.overhead_virtualizacao == 4.0 for v in nuvem.vms))
        except NotImplementedError:
            self.skipTest("Trabalho do Integrante 3 (Cloud Init) ainda não implementado.")

    def test_escalonamento_round_robin(self):
        processos = [Processo(id=0, tempo_execucao=5), Processo(id=1, tempo_execucao=10)]
        try:
            nuvem = Cloud(quantidade_vms=2)
            nuvem.escalonar_round_robin(processos)
            self.assertEqual(len(nuvem.vms[0].fila_processos), 1)
            self.assertEqual(len(nuvem.vms[1].fila_processos), 1)
            self.assertEqual(nuvem.vms[0].fila_processos[0].id, 0)
            self.assertEqual(nuvem.vms[1].fila_processos[0].id, 1)
        except NotImplementedError:
            self.skipTest("Trabalho do Integrante 3 (Round Robin) ainda não implementado.")

    def test_executar_simulacao(self):
        try:
            nuvem = Cloud(quantidade_vms=1, capacidade_vms=2.0, overhead_vms=3.0)
            nuvem.vms[0].fila_processos.append(Processo(id=0, tempo_execucao=10))
            nuvem.vms[0].fila_processos.append(Processo(id=1, tempo_execucao=4))
            
            nuvem.executar_simulacao()
            
            # (10 + 4)/2 + 3 = 10.0
            self.assertEqual(nuvem.vms[0].tempo_total_execucao, 10.0)
        except NotImplementedError:
            self.skipTest("Trabalho do Integrante 3 (Execução) ainda não implementado.")

if __name__ == "__main__":
    unittest.main()
