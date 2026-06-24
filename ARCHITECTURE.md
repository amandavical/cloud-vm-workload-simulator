# Arquitetura Simplificada: Simulador de Carga de Trabalho em Nuvem

Este documento descreve a especificação arquitetural para o projeto **"Impacto da quantidade de máquinas virtuais na execução de cargas de trabalho em uma nuvem simulada"**. A arquitetura foi otimizada para reduzir pontos de falha de integração, mantendo a separação conceitual de responsabilidades entre os **4 integrantes do grupo**.

---

## 📁 1. Estrutura de Pastas e Módulos do Projeto

Para reduzir a complexidade e evitar problemas de integração cruzada, os antigos submódulos de escalonador, executor e infraestrutura foram consolidados em um único arquivo `cloud.py`. O fluxo é sequencial e direto.

```
cloud-vm-workload-simulator/
│
├── ARCHITECTURE.md             # Este documento de especificação simplificada
├── main.py                     # Ponto central de integração (Líder Técnico)
├── requirements.txt            # Dependências de terceiros (ex: matplotlib)
│
├── src/                        # Código-fonte principal
│   ├── __init__.py
│   │
│   ├── core/                   # Modelos de Dados Comuns
│   │   ├── __init__.py
│   │   └── models.py           # Classes de dados Processo e VM (Líder Técnico)
│   │
│   ├── simulation/             # Módulo de Carga e Núcleo Operacional da Nuvem
│   │   ├── __init__.py
│   │   ├── workload.py         # Geração de processos e cenários de carga (Integrante 2)
│   │   └── cloud.py            # Criação de VMs, Escalonamento e Execução (Integrante 3)
│   │
│   └── analysis/               # Métricas e Visualização de Gráficos (Integrante 4)
│       ├── __init__.py
│       ├── metrics.py          # Cálculo de Makespan, Throughput, Espera e Desvio
│       └── visualization.py    # Geração de gráficos (Matplotlib) e Tabelas
│
└── tests/                      # Suite de testes para validação individual
    ├── __init__.py
    ├── test_workload.py        # Valida a geração de cargas (Integrante 2)
    ├── test_cloud.py           # Valida as VMs, o escalonador e execução (Integrante 3)
    ├── test_metrics.py         # Valida os cálculos de métricas (Integrante 4)
    └── test_visualization.py   # Valida a plotagem (Integrante 4)
```

---

## 👥 2. Divisão de Responsabilidades Simplificada

### Integrante 1 (Líder Técnico)
* **Responsabilidades**:
  * Desenhar a arquitetura de fluxos simplificados e padronizar contratos de dados.
  * Desenvolver as classes fundamentais de modelos em `models.py`.
  * Integrar os módulos de todos no arquivo `main.py` gerenciando exceções e fluxo.
* **Arquivos**:
  * [src/core/models.py](file:///Users/amandavieira/Dev/projects/cloud-vm-workload-simulator/src/core/models.py) (Estruturas `Processo` e `VM`)
  * [main.py](file:///Users/amandavieira/Dev/projects/cloud-vm-workload-simulator/main.py) (Orquestrador)

### Integrante 2 - Geração de Cargas de Trabalho
* **Responsabilidades**:
  * Definir cenários de carga ('leve', 'media', 'pesada') definindo limites e tamanhos de CPU.
  * Implementar a geração determinística de listas de processos de carga de trabalho.
* **Arquivos**:
  * [src/simulation/workload.py](file:///Users/amandavieira/Dev/projects/cloud-vm-workload-simulator/src/simulation/workload.py) (Funções `generate_processes` e `define_workload_scenarios`)

### Integrante 3 - Núcleo da Nuvem (Escalonador e Executor)
* **Responsabilidades**:
  * Inicializar a lista de VMs dinamicamente dentro da classe `Cloud`.
  * Desenvolver os algoritmos de alocação de processos (Round Robin e Menor Fila) usando métodos auxiliares para manter a legibilidade.
  * Simular a execução temporal baseada no modelo analítico de soma direta de tempos.
* **Arquivos**:
  * [src/simulation/cloud.py](file:///Users/amandavieira/Dev/projects/cloud-vm-workload-simulator/src/simulation/cloud.py) (Classe `Cloud` contendo a lista de VMs, escalonadores e executor combinados)

### Integrante 4 - Métricas, Análise e Visualização
* **Responsabilidades**:
  * Implementar funções de estatística para calcular Makespan, Throughput, Tempo de Espera Médio e Desvio de Carga.
  * Gerar tabelas formatadas no console e plotar gráficos comparativos salvando em disco.
* **Arquivos**:
  * [src/analysis/metrics.py](file:///Users/amandavieira/Dev/projects/cloud-vm-workload-simulator/src/analysis/metrics.py)
  * [src/analysis/visualization.py](file:///Users/amandavieira/Dev/projects/cloud-vm-workload-simulator/src/analysis/visualization.py)

---

## 💾 3. Modelos de Dados Padronizados

Os modelos principais em `src/core/models.py` são as únicas dependências de estrutura compartilhadas.

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Processo:
    id: int                # Identificador único (PID)
    tempo_execucao: int    # Demanda de CPU (ciclos ou segundos)
    tempo_chegada: int = 0  # Instante de chegada à nuvem

@dataclass
class VM:
    id: int
    capacidade_processamento: float = 1.0  # Velocidade (ex: 2.0 executa em metade do tempo)
    overhead_virtualizacao: float = 2.0    # Custo fixo de gerenciamento da VM
    fila_processos: List[Processo] = field(default_factory=list) # Fila local de execução
    tempo_total_execucao: float = 0.0      # Tempo final acumulado
```

---

## ⏱️ 4. Modelo de Tempo de Simulação (Muito Importante)

Para evitar ambiguidades no desenvolvimento e na avaliação dos resultados, a simulação adota o **Modelo de Soma Direta de Tempos (Modelo Analítico Acumulado)** em vez de simulação baseada em clock discreto (*ticks*).

* **Funcionamento**: A simulação calcula diretamente o tempo acumulado no final do lote de processos. Cada processo na fila local de uma VM é executado em sequência.
* **Fórmula de Tempo de Execução de uma VM**:
  $$T_{total\_execucao} = \frac{\sum_{p \in fila} p.tempo\_execucao}{capacidade\_processamento} + overhead\_virtualizacao$$
  *(Se a fila de processos da VM estiver vazia, o tempo total de execução é zero).*
* **Por que esta abordagem?**: Reduz a complexidade de concorrência ou loops infinitos de clock no código, mantendo o determinismo absoluto e simplificando o cálculo de métricas para o Integrante 4.

---

## 🤝 5. Contratos de Interface (Assinaturas das Funções)

Para garantir que a integração ocorra de forma transparente no `main.py`, respeite as seguintes assinaturas de classe e funções:

```python
# Módulo: workload.py (Integrante 2)
def generate_processes(quantidade: int, cenario: str = "media", seed: int = 42) -> List[Processo]: ...
def define_workload_scenarios() -> Dict[str, Dict[str, Any]]: ...

# Módulo: cloud.py (Integrante 3)
class Cloud:
    def __init__(self, quantidade_vms: int, capacidade_vms: float = 1.0, overhead_vms: float = 2.0):
        self.vms: List[VM] = []
    
    # Métodos privados recomendados para legibilidade:
    def _alocar_processo_na_vm(self, processo: Processo, vm: VM) -> None: ...
    def _executar_vm(self, vm: VM) -> None: ...
    
    # Métodos públicos de escalonamento e execução:
    def escalonar_round_robin(self, processos: List[Processo]) -> None: ...
    def escalonar_menor_fila(self, processos: List[Processo]) -> None: ...
    def executar_simulacao(self) -> None: ...

# Módulo: metrics.py (Integrante 4)
def calcular_makespan(vms: List[VM]) -> float: ...
def calcular_tempo_espera_medio(vms: List[VM], total_processos: int) -> float: ...
def calcular_throughput(vms: List[VM], total_processos: int) -> float: ...
def calcular_desvio_carga(vms: List[VM]) -> float: ...

# Módulo: visualization.py (Integrante 4)
def plotar_graficos_comparativos(resultados: List[Dict[str, Any]], caminho_imagem: str) -> None: ...
def imprimir_tabela_comparativa(resultados: List[Dict[str, Any]]) -> None: ...
```

---

## 🔄 6. Fluxo de Simulação Simplificado

O fluxo se torna direto e livre de importações cíclicas:

1. **main.py** orquestra e chama `generate_processes` (Integrante 2).
2. **main.py** inicializa a classe `Cloud` instanciando as VMs (Integrante 3).
3. **main.py** chama o escalonador e executor dentro da própria classe `Cloud` (Integrante 3).
4. **main.py** envia o estado final das VMs para as funções de métrica e visualização (Integrante 4).
5. **main.py** imprime tabelas e gera arquivos de gráficos comparativos automaticamente.
