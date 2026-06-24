# Simulador de Cargas de Trabalho em Nuvem (Simulador VM-Workload)

Este projeto foi desenvolvido como trabalho prático para a disciplina de **Sistemas Operacionais**. O objetivo é simular o impacto da quantidade de Máquinas Virtuais (VMs) alocadas no tempo de execução de cargas de trabalho (processos) em um ambiente de nuvem, comparando as políticas de escalonamento **Round Robin** e **Menor Fila (Least Loaded)**.

---

## 🚀 1. Ambiente Replicável (Instalação)

O projeto foi desenvolvido em **Python 3** e utiliza um ambiente virtual isolado para gerenciamento de dependências.

### Passo a Passo para Execução:

1. **Clonar ou baixar o repositório** do projeto.
2. **Criar o ambiente virtual** na raiz do projeto:
   ```bash
   python3 -m venv .venv
   ```
3. **Ativar o ambiente virtual**:
   * No Linux/macOS:
     ```bash
     source .venv/bin/env/activate  # ou source .venv/bin/activate
     ```
   * No Windows (Prompt de Comando):
     ```cmd
     .venv\Scripts\activate
     ```
4. **Instalar as dependências** necessárias (ex: `matplotlib` para gráficos):
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔄 2. Executando a Simulação

O script principal realiza a simulação de execução de **200 processos** sobre cenários configurados com **1, 2, 4, 8 e 16 VMs**, testando ambos os algoritmos de escalonamento.

Para rodar a simulação e gerar os relatórios e gráficos:
```bash
python3 main.py
```
* **Saída Esperada no Console**: Uma tabela comparativa exibindo o *Makespan*, *Tempo Médio de Espera* e *Desvio de Carga* para cada cenário.
* **Saída em Arquivo**: O gráfico comparativo de curvas de desempenho é salvo automaticamente na raiz do projeto com o nome `resultados_desempenho.png`.

---

## 🧪 3. Casos de Teste (Entradas e Saídas Mapeadas)

A suite de testes automatizados valida as lógicas de negócio do projeto, servindo como documentação viva de **Entradas** e **Saídas** esperadas para cada módulo.

Para rodar todos os testes unitários do sistema:
```bash
python3 -m unittest discover -s tests
```

### Exemplos de Casos de Teste Mapeados no Código:

#### Caso de Teste 1: Escalonamento Round Robin (`tests/test_cloud.py`)
* **Entrada**: 
  * 2 VMs vazias (IDs 0 e 1).
  * Lista de 2 processos: `P0` (tempo = 5) e `P1` (tempo = 10).
* **Processamento**: Distribuição sequencial alternada (Round Robin).
* **Saída Esperada**:
  * VM 0 deve conter apenas o processo `P0` em sua fila local.
  * VM 1 deve conter apenas o processo `P1` em sua fila local.

#### Caso de Teste 2: Escalonamento Menor Fila (`tests/test_scheduler.py`)
* **Entrada**: 
  * 2 VMs vazias (IDs 0 e 1).
  * Lista de 4 processos: `P0` (tempo = 5), `P1` (tempo = 10), `P2` (tempo = 2), `P3` (tempo = 8).
* **Processamento**: Distribuição dinâmica (aloca o processo na VM com menor carga acumulada no momento).
* **Saída Esperada**:
  * VM 0: Fila local deve conter `[P0, P2, P3]` (carga total = 15).
  * VM 1: Fila local deve conter `[P1]` (carga total = 10).

#### Caso de Teste 3: Lógica de Simulação de Execução (`tests/test_cloud.py`)
* **Entrada**:
  * 1 VM com capacidade de processamento = 2.0 e overhead de virtualização = 3.0.
  * Fila local da VM contendo: `P0` (tempo = 10) e `P1` (tempo = 4).
* **Processamento**: Aplicação da fórmula temporal:
  $$T_{execucao} = \frac{\sum T_{processos}}{\text{capacidade}} + \text{overhead}$$
* **Cálculo**:
  $$T_{execucao} = \frac{10 + 4}{2.0} + 3.0 = 7.0 + 3.0 = 10.0$$
* **Saída Esperada**: O tempo total de execução da VM deve ser exatamente `10.0`.

#### Caso de Teste 4: Métricas do Sistema (`tests/test_metrics.py`)
* **Entrada**:
  * VM 0 com tempo de execução = 12.0.
  * VM 1 com tempo de execução = 8.0.
* **Saída Esperada (Makespan)**: `12.0` (tempo máximo gasto para concluir todas as VMs).
