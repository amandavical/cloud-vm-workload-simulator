import unittest
from src.core.models import Processo
from src.simulation.workload import generate_processes, define_workload_scenarios

class TestWorkloadGenerator(unittest.TestCase):
    def test_define_workload_scenarios(self):
        try:
            cenarios = define_workload_scenarios()
            self.assertIsInstance(cenarios, dict)
            self.assertIn("leve", cenarios)
            self.assertIn("media", cenarios)
            self.assertIn("pesada", cenarios)
        except NotImplementedError:
            self.skipTest("Trabalho do Integrante 2 (Cenários de Carga) ainda não implementado.")

    def test_generate_processes(self):
        try:
            processos = generate_processes(quantidade=10, cenario="media", seed=42)
            self.assertEqual(len(processos), 10)
            self.assertTrue(all(isinstance(p, Processo) for p in processos))
        except NotImplementedError:
            self.skipTest("Trabalho do Integrante 2 (Geração de Processos) ainda não implementado.")

if __name__ == "__main__":
    unittest.main()
