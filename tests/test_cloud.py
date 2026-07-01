import unittest
from src.core.models import Processo, VM
from src.simulation.cloud import Cloud

class TestCloud(unittest.TestCase):
    def test_inicializacao_vms(self):
        # OBJETIVO: Garantir que a Cloud cria o número correto de VMs com as configurações passadas
        nuvem = Cloud(quantidade_vms=3, capacidade_vms=2.0, overhead_vms=4.0)
        
        # 1. Verifica se foram criadas exatamente 3 VMs
        self.assertEqual(len(nuvem.vms), 3)
        
        # 2. Garante que todos os objetos na lista são instâncias da classe VM
        self.assertTrue(all(isinstance(v, VM) for v in nuvem.vms))
        
        # 3. Garante que a velocidade/capacidade de todas as VMs foi configurada para 2.0
        self.assertTrue(all(v.capacidade_processamento == 2.0 for v in nuvem.vms))
        
        # 4. Garante que o overhead de virtualização de todas as VMs foi configurado para 4.0
        self.assertTrue(all(v.overhead_virtualizacao == 4.0 for v in nuvem.vms))

    def test_escalonamento_round_robin(self):
        # OBJETIVO: Testar se o escalonador Round Robin distribui processos alternando as VMs de forma justa
        # Criamos dois processos de teste: P0 (tempo=5) e P1 (tempo=10)
        processos = [Processo(id=0, tempo_execucao=5), Processo(id=1, tempo_execucao=10)]
        
        # Criamos uma nuvem com 2 VMs
        nuvem = Cloud(quantidade_vms=2)
        
        # Executamos a distribuição Round Robin
        nuvem.escalonar_round_robin(processos)
        
        # 1. VM 0 deve ter exatamente 1 processo na fila
        self.assertEqual(len(nuvem.vms[0].fila_processos), 1)
        
        # 2. VM 1 deve ter exatamente 1 processo na fila
        self.assertEqual(len(nuvem.vms[1].fila_processos), 1)
        
        # 3. P0 (ID 0) deve estar na fila da VM 0
        self.assertEqual(nuvem.vms[0].fila_processos[0].id, 0)
        
        # 4. P1 (ID 1) deve estar na fila da VM 1
        self.assertEqual(nuvem.vms[1].fila_processos[0].id, 1)

    def test_executar_simulacao(self):
        # OBJETIVO: Validar a fórmula matemática de tempo de execução da VM
        # T_total = (Soma dos tempos dos processos / capacidade_processamento) + overhead
        nuvem = Cloud(quantidade_vms=1, capacidade_vms=2.0, overhead_vms=3.0)
        
        # Adicionamos manualmente dois processos na VM 0: P0 (tempo=10) e P1 (tempo=4)
        nuvem.vms[0].fila_processos.append(Processo(id=0, tempo_execucao=10))
        nuvem.vms[0].fila_processos.append(Processo(id=1, tempo_execucao=4))
        
        # Disparamos a simulação
        nuvem.executar_simulacao()
        
        # CÁLCULO ESPERADO:
        # Soma dos tempos = 10 + 4 = 14
        # Dividido pela capacidade (velocidade) = 14 / 2.0 = 7.0
        # Somado ao overhead de virtualização = 7.0 + 3.0 = 10.0 segundos
        self.assertEqual(nuvem.vms[0].tempo_total_execucao, 10.0)

if __name__ == "__main__":
    unittest.main()
