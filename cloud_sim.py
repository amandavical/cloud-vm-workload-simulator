import random
import matplotlib.pyplot as plt


# -------------------------
# PROCESSO
# -------------------------
class Processo:
    def __init__(self, pid, tempo_execucao):
        self.pid = pid
        self.tempo = tempo_execucao


# -------------------------
# VM
# -------------------------
class VM:
    def __init__(self, vid):
        self.vid = vid
        self.fila = []
        self.tempo_total = 0

    def executar(self, overhead_vm=2):
        tempo = 0
        for p in self.fila:
            tempo += p.tempo
        self.tempo_total = tempo + overhead_vm


# -------------------------
# CLOUD (NUVEM)
# -------------------------
class Cloud:
    def __init__(self, num_vms, overhead_vm=2):
        self.vms = [VM(i) for i in range(num_vms)]
        self.overhead_vm = overhead_vm

    # balanceamento simples (menor fila)
    def distribuir(self, processos):
        for p in processos:
            vm = min(self.vms, key=lambda v: len(v.fila))
            vm.fila.append(p)

    def executar(self):
        for vm in self.vms:
            vm.executar(self.overhead_vm)

    def tempo_total(self):
        return max(vm.tempo_total for vm in self.vms)


# -------------------------
# GERAR PROCESSOS
# -------------------------
def gerar_processos(n):
    processos = []
    for i in range(n):
        tempo = random.randint(1, 10)
        processos.append(Processo(i, tempo))
    return processos


# -------------------------
# EXPERIMENTO
# -------------------------
def simular():
    num_processos = 200
    processos = gerar_processos(num_processos)

    configs = [1, 2, 4, 8, 16]
    resultados = []

    for vms in configs:
        cloud = Cloud(vms)

        cloud.distribuir(processos)
        cloud.executar()

        tempo = cloud.tempo_total()
        resultados.append(tempo)

        print(f"VMs: {vms} -> Tempo total: {tempo}")

    # gráfico
    plt.plot(configs, resultados, marker='o')
    plt.title("Impacto da quantidade de VMs no desempenho")
    plt.xlabel("Número de VMs")
    plt.ylabel("Tempo total de execução")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    simular()