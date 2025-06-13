# TOTEM DE AUTOATENDIMENTO - HOSPITAL SABARÁ
##INTEGRANTES:
Guilherme Augusto Caseiro - RM: 559765
Leonardo Fernandes Mesquita - RM: 559623
Marco Antonio Caires Freire - RM: 559256


Este projeto foi desenvolvido em Python com os frameworks Kivy e KivyMD como parte da disciplina de Computational Thinking With Python.

##  OBJETIVO
Automatizar o processo de triagem de pacientes por meio de um totem interativo. A solução permite que o próprio paciente insira seus dados e realize uma autoavaliação de sintomas, após a qual o sistema realiza uma classificação automática por prioridade de atendimento e organiza uma fila de forma persistente.

##  FUNCIONALIDADES PRINCIPAIS
- **Tela de Boas-Vindas:** Uma tela de abertura profissional com a identidade visual do hospital, que dura 4 segundos antes de transicionar para o formulário.
- **Formulário de Cadastro:** Interface moderna para coleta de dados essenciais do paciente (Nome, Data de Nascimento, RG, Contato).
- **Autoavaliação de Sintomas:** Questionário interativo sobre Dor (com escala de 1 a 10), Febre, Náusea e Vômito.
- **Classificação de Risco:** Lógica interna que atribui um nível de urgência (Muito Emergente, Urgente, Emergente, Estável) com base nas respostas.
- **Fila de Atendimento Persistente:** A fila é organizada por prioridade e salva em um arquivo `patient_queue.json`, garantindo que os dados não se percam ao fechar o aplicativo.
- **Validação e Tratamento de Erros:** O sistema valida os formulários para garantir que todos os campos sejam preenchidos e utiliza tratamento de exceções para prevenir crashes por entradas inválidas.

##  Como Executar o Projeto

#### Pré-requisitos
- **Python 3.9+** instalado no computador. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).

#### Passo a Passo para Execução

**1. Clone o Repositório**

Abra um terminal (Git Bash, cmd, PowerShell) e clone o repositório para o seu computador.
```bash
git clone [https://github.com/MACF77/SPRINT-4-Sabar-py.git](https://github.com/MACF77/SPRINT-4-Sabar-py.git)
```

**2. Navegue até a Pasta do Projeto**
```bash
cd SPRINT-4-Sabar-py
```

**3. Crie e Ative um Ambiente Virtual (venv)**

Um ambiente virtual isola as dependências do projeto e é uma boa prática de desenvolvimento para evitar conflitos.

* **No Windows (Prompt de Comando/PowerShell):**
  ```bash
  # Cria o ambiente virtual na pasta 'venv'
  python -m venv venv
  # Ativa o ambiente
  venv\Scripts\activate
  ```

* **No Windows (Git Bash) ou macOS/Linux:**
  ```bash
  # Cria o ambiente virtual na pasta 'venv'
  python -m venv venv
  # Ativa o ambiente
  source venv/Scripts/activate
  ```
  *( funcionou quando vir `(venv)` no início da linha do terminal).*

**4. Instale as Dependências**

Com o ambiente virtual ativado, instale as bibliotecas Kivy e KivyMD nas versões exatas usadas no projeto para garantir total compatibilidade:
```bash
pip install kivy==2.3.1 kivymd==1.1.1
```

**5. Execute o Aplicativo**

Finalmente, execute o arquivo principal para iniciar o totem:
```bash
python main.py
```

## 🛠️ Tecnologias Utilizadas
- **Python 3**
- **Kivy 2.3.1**
- **KivyMD 1.1.1**

## 👥 Desenvolvedores
* **Leonardo Fernandes Mesquita**, RM: 559623 - [GitHub](https://github.com/leoGitFiap)
* **Marco Antonio Caires Freire**, RM: 559256 - [GitHub](https://github.com/MACF77)
* **Guilherme Augusto Caseiro**, RM: 559765 - [GitHub](https://github.com/Guiitens2005)
