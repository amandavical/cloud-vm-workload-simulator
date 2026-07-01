import argparse
import unittest

from main import (
    CENARIOS_QUATRO_GRAFICOS,
    nome_arquivo_resultado,
    quantidade_positiva
)


class TestMainCli(unittest.TestCase):
    def test_nome_arquivo_resultado(self):
        self.assertEqual(
            nome_arquivo_resultado("pesada", 200),
            "resultados_pesada_200.png"
        )

    def test_quantidade_positiva(self):
        self.assertEqual(quantidade_positiva("1000"), 1000)

        with self.assertRaises(argparse.ArgumentTypeError):
            quantidade_positiva("0")

    def test_cenarios_quatro_graficos(self):
        self.assertEqual(
            CENARIOS_QUATRO_GRAFICOS,
            [
                ("media", 200),
                ("media", 1000),
                ("pesada", 200),
                ("pesada", 1000),
            ]
        )


if __name__ == "__main__":
    unittest.main()
