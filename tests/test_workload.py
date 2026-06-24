import unittest
from src.core.models import Processo
from src.simulation.workload import generate_processes, define_workload_scenarios

class TestWorkloadGenerator(unittest.TestCase):
    def test_define_workload_scenarios(self):
        # Validação da definição dos cenários
        cenarios = define_workload_scenarios()
        self.assertIsInstance(cenarios, dict)
        self.assertIn("leve", cenarios)
        self.assertIn("media", cenarios)
        self.assertIn("pesada", cenarios)
        
        # Validação dos tamanhos definidos nos requisitos
        self.assertEqual(cenarios["leve"]["quantity"], 50)
        self.assertEqual(cenarios["media"]["quantity"], 200)
        self.assertEqual(cenarios["pesada"]["quantity"], 500)

    def test_generate_processes_quantity(self):
        # Geração da quantidade correta de processos via parâmetro quantity
        processos = generate_processes(quantity=10)
        self.assertEqual(len(processos), 10)
        self.assertTrue(all(isinstance(p, Processo) for p in processos))
        
        processos_large = generate_processes(quantity=25)
        self.assertEqual(len(processos_large), 25)

    def test_generate_processes_ids_unicos(self):
        # IDs únicos nos processos gerados
        processos = generate_processes(quantity=100)
        ids = [p.id for p in processos]
        self.assertEqual(len(ids), len(set(ids)))

    def test_reprodutibilidade_seed(self):
        # Reprodutibilidade usando a mesma seed
        p1 = generate_processes(quantity=50, seed=42)
        p2 = generate_processes(quantity=50, seed=42)
        
        self.assertEqual(len(p1), len(p2))
        for proc1, proc2 in zip(p1, p2):
            self.assertEqual(proc1.id, proc2.id)
            self.assertEqual(proc1.tempo_execucao, proc2.tempo_execucao)
            self.assertEqual(proc1.uso_cpu, proc2.uso_cpu)
            self.assertEqual(proc1.tempo_chegada, proc2.tempo_chegada)

    def test_geracao_aleatoria_sem_seed(self):
        # Geração aleatória sem seed (deve diferir na grande maioria dos casos)
        p1 = generate_processes(quantity=100, seed=None)
        p2 = generate_processes(quantity=100, seed=None)
        
        # Pelo menos um tempo_execucao ou uso_cpu deve ser diferente devido à aleatoriedade
        valores_diferentes = any(
            proc1.tempo_execucao != proc2.tempo_execucao or proc1.uso_cpu != proc2.uso_cpu
            for proc1, proc2 in zip(p1, p2)
        )
        self.assertTrue(valores_diferentes)

    def test_valida_cenarios(self):
        # Validação dos cenários leve, média e pesada
        p_leve = generate_processes(cenario="leve")
        self.assertEqual(len(p_leve), 50)
        
        # Sem acento
        p_media = generate_processes(cenario="media")
        self.assertEqual(len(p_media), 200)
        
        # Com acento
        p_media_acento = generate_processes(cenario="média")
        self.assertEqual(len(p_media_acento), 200)
        
        p_pesada = generate_processes(cenario="pesada")
        self.assertEqual(len(p_pesada), 500)

    def test_faixas_atributos(self):
        # Validação dos limites dos atributos tempo_execucao e uso_cpu [1, 100]
        processos = generate_processes(quantity=1000, seed=123)
        for p in processos:
            self.assertTrue(1 <= p.tempo_execucao <= 100)
            self.assertTrue(1 <= p.uso_cpu <= 100)

if __name__ == "__main__":
    unittest.main()
