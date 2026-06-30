# src/simulation/cloud.py

from typing import List
from src.core.models import Processo, VM


class Cloud:

    def __init__(
        self,
        quantidade_vms: int = 3,
        capacidade_vms: float = 1.0,
        overhead_vms: float = 2.0
    ):
        """
        Inicializa a infraestrutura de VMs.
        """

        self.vms: List[VM] = []

        for i in range(quantidade_vms):
            self.vms.append(
                VM(
                    id=i,
                    capacidade_processamento=capacidade_vms,
                    overhead_virtualizacao=overhead_vms
                )
            )

    def _alocar_processo_na_vm(
        self,
        processo: Processo,
        vm: VM
    ) -> None:
        """
        Adiciona um processo à fila de execução da VM.
        """

        vm.fila_processos.append(processo)

    def _carga_vm(self, vm: VM) -> float:
        """
        Calcula a carga acumulada de uma VM.

        A carga é definida como a soma dos tempos
        de execução dos processos alocados.
        """

        return sum(
            processo.tempo_execucao
            for processo in vm.fila_processos
        )

    def escalonar_round_robin(
        self,
        processos: List[Processo]
    ) -> None:
        """
        Distribui processos alternadamente entre as VMs.
        """

        indice_vm = 0

        for processo in processos:

            vm = self.vms[indice_vm]

            self._alocar_processo_na_vm(
                processo,
                vm
            )

            indice_vm = (
                indice_vm + 1
            ) % len(self.vms)

    def escalonar_menor_fila(
        self,
        processos: List[Processo]
    ) -> None:
        """
        Sempre escolhe a VM menos carregada.
        """

        for processo in processos:

            vm_escolhida = min(
                self.vms,
                key=self._carga_vm
            )

            self._alocar_processo_na_vm(
                processo,
                vm_escolhida
            )

    def _executar_vm(
        self,
        vm: VM
    ) -> float:
        """
        Simula a execução dos processos de uma VM.
        """
        if not vm.fila_processos:
            vm.tempo_total_execucao = 0.0
            return 0.0

        soma_tempos = sum(processo.tempo_execucao for processo in vm.fila_processos)
        tempo_total = (soma_tempos / vm.capacidade_processamento) + vm.overhead_virtualizacao
        vm.tempo_total_execucao = tempo_total
        return tempo_total

    def executar_simulacao(self) -> None:
        """
        Executa todas as VMs já escalonadas.
        """

        for vm in self.vms:
            self._executar_vm(vm)