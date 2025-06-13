# =============================================================================
# PROJETO: Totem de Autoatendimento Hospitalar
# DISCIPLINA: Computational Thinking With Python
#
# AUTORES:
#   - Leonardo Fernandes Mesquita, RM:559623 (https://github.com/leoGitFiap)
#   - Marco Antonio Caires Freire, RM:559256 (https://github.com/MACF77)
#   - Guilherme Augusto Caseiro, RM:559765 (https://github.com/Guiitens2005)
#
# DESCRIÇÃO: Este projeto é um protótipo funcional de um totem de autoatendimento
# para o Hospital Infantil Sabará. O objetivo é permitir que os pacientes
# façam uma triagem inicial de sintomas, inserindo seus dados e respondendo a um
# questionário. O sistema então classifica a urgência e organiza os pacientes
# em uma fila de atendimento.
# O projeto demonstra o uso de estruturas de dados, manipulação de arquivos
# e tratamento de exceções em Python com o framework Kivy/KivyMD.
# =============================================================================

# Imports para manipulação de arquivos JSON e verificação de existência de arquivos
import json
import os

# Imports do Kivy e KivyMD para a construção da interface gráfica
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.core.window import Window

# A classe SplashScreen é a minha tela de boas-vindas.
# Ela tem o objetivo de criar uma primeira impressão profissional
# e carregar a logo e o fundo do hospital.
class SplashScreen(Screen):
    # O método on_enter é chamado assim que a tela aparece.
    def on_enter(self, *args):
        # Aqui, eu uso o Clock.schedule_once para agendar a troca de tela.
        # Ele chama a função 'switch_to_main_screen' após 4 segundos.
        Clock.schedule_once(self.switch_to_main_screen, 4)

    def switch_to_main_screen(self, *args):
        # Defino a animação de transição e mudo para a tela principal.
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'main'

# A classe MainScreen gerencia a tela de formulário inicial.
class MainScreen(Screen):
    # Agendo a formatação da data para garantir que o Kivy já tenha processado
    # o campo de texto, evitando bugs.
    def schedule_format_dob(self):
        Clock.schedule_once(self.format_dob, 0)

    # Função para formatar o texto da data de nascimento com as barras (DD/MM/AAAA)
    def format_dob(self, *args):
        field = self.ids.dob_input
        # Pego apenas os dígitos do texto para formatar corretamente.
        digits = ''.join(filter(str.isdigit, field.text))
        formatted = ''
        if len(digits) > 0:
            formatted += digits[:2]
        if len(digits) > 2:
            formatted += '/' + digits[2:4]
        if len(digits) > 4:
            formatted += '/' + digits[4:8]
        field.text = formatted

    # Validação dos campos do formulário antes de prosseguir.
    def validate_and_go(self):
        self.manager.transition.direction = 'left'
        app = MDApp.get_running_app()
        
        # Uso uma LISTA para armazenar as mensagens de erro,
        # demonstrando o uso de estruturas de dados.
        missing = []
        if not self.ids.name_input.text.strip():
            missing.append("Nome completo")
        if not self.ids.dob_input.text.strip() or len(self.ids.dob_input.text) < 10:
            missing.append("Data de nascimento")
        if not self.ids.rg_input.text.strip():
            missing.append("Número do RG")
        if not self.ids.contact_input.text.strip():
            missing.append("Número de contato")

        # Se a lista 'missing' tiver algum item, exibo um diálogo de erro.
        if missing:
            dialog = MDDialog(
                title="Campos obrigatórios",
                text="Por favor preencha: " + ', '.join(missing),
                buttons=[MDFlatButton(text="OK")]
            )
            dialog.buttons[0].on_release = dialog.dismiss
            dialog.open()
        else:
            # Se tudo estiver correto, avanço para a tela de avaliação.
            self.manager.current = "assessment"

# A classe AssessmentScreen controla a tela do questionário de sintomas.
class AssessmentScreen(Screen):
    def on_enter(self, *args):
        # Defino a direção da transição para quando o usuário voltar.
        self.manager.transition.direction = 'right'

    # Função para formatar o campo de temperatura com vírgula.
    def format_temperature(self, instance, value):
        digits = ''.join(c for c in value if c.isdigit())
        if not digits:
            instance.text = ''
            return
        if len(digits) > 3:
            digits = digits[:3]
        if len(digits) <= 2:
            formatted = digits
        else:
            formatted = digits[:2] + ',' + digits[2]
        # Para garantir que o app não quebre, uso um bloco try-except.
        try:
            if float(formatted.replace(',', '.')) > 42.2:
                formatted = "42,2"
        except (ValueError, TypeError):
            pass
        if instance.text != formatted:
            instance.text = formatted
            instance.cursor = (len(formatted), 0)

    # Processa as respostas do questionário para classificar o paciente.
    def process_assessment(self):
        app = MDApp.get_running_app()
        main = self.manager.get_screen("main")
        
        dor = self.ids.pain_yes.active
        
        # REQUISITO: Tratamento de Exceções.
        # Uso um bloco try-except para converter a entrada de texto em número.
        # Se o usuário digitar um texto inválido (ex: 'abc'), o programa não quebra,
        # e o valor é definido como 0.
        grau_dor = 0
        try:
            grau_dor = int(self.ids.pain_level_input.text)
        except ValueError:
            grau_dor = 0
        if grau_dor > 10:
            grau_dor = 10

        febre = self.ids.fever_yes.active
        temp = 36.5
        # Outro exemplo de tratamento de exceção para a temperatura.
        try:
            temp = float(self.ids.temperature_input.text.replace(',', '.'))
        except (ValueError, TypeError):
            temp = 36.5
        if temp > 42.2:
            temp = 42.2

        nausea = self.ids.nausea_yes.active
        vomito = self.ids.vomiting_yes.active

        # Lógica de classificação de urgência.
        if grau_dor >= 9 or temp >= 40 or vomito:
            urgencia = "Muito Emergente"
            prioridade = 1
        elif grau_dor >= 7 or (febre and temp >= 39) or (nausea and vomito):
            urgencia = "Urgente"
            prioridade = 2
        elif grau_dor >= 5 or (febre and temp >= 38):
            urgencia = "Emergente"
            prioridade = 3
        else:
            urgencia = "Estável"
            prioridade = 4

        # REQUISITO: Estruturas de Dados.
        # Utilizo um DICIONÁRIO para organizar as informações do paciente
        # de forma estruturada.
        paciente_info = {
            'nome': main.ids.name_input.text,
            'rg': main.ids.rg_input.text,
            'urgencia': urgencia,
            'prioridade': prioridade
        }
        
        # Adiciono o dicionário do paciente à LISTA da fila.
        app.fila.append(paciente_info)
        # Ordeno a fila com base na prioridade.
        app.fila.sort(key=lambda x: x['prioridade'])

        # REQUISITO: Manipulação de Arquivos (Escrita).
        # Chamo a função para salvar a fila atualizada no arquivo JSON.
        app.save_queue()

        posicao_fila = app.fila.index(paciente_info) + 1
        resumo = (
            f"Nome: {paciente_info['nome']}\n"
            f"RG: {paciente_info['rg']}\n\n"
            f"Classificação: {urgencia}\n"
            f"Sua posição na fila: {posicao_fila}º\n\n"
            "Por favor, aguarde na sala. Você será chamado em breve!"
        )
        dialog = MDDialog(
            title="Resumo da Avaliação",
            text=resumo,
            buttons=[MDFlatButton(text="OK")]
        )
        dialog.buttons[0].on_release = dialog.dismiss
        dialog.open()
        self.manager.current = "main"

# Classe principal do meu aplicativo.
class TotemApp(MDApp):
    # Nome do arquivo onde a fila de pacientes será salva.
    QUEUE_FILE = "patient_queue.json"

    def save_queue(self):
        """Salva a fila de pacientes atual no arquivo JSON."""
        # Uso 'try-except' para lidar com possíveis erros de permissão de escrita.
        try:
            # O 'with open' garante que o arquivo seja fechado corretamente no final.
            with open(self.QUEUE_FILE, 'w', encoding='utf-8') as f:
                # json.dump serializa minha lista de dicionários para o formato JSON.
                # O indent=4 formata o arquivo para ser legível por humanos.
                json.dump(self.fila, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar a fila: {e}")

    def load_queue(self):
        """Carrega a fila de pacientes do arquivo JSON, se ele existir."""
        # Verifico se o arquivo de save já existe.
        if os.path.exists(self.QUEUE_FILE):
            # 'try-except' para o caso de o arquivo estar vazio ou corrompido.
            try:
                with open(self.QUEUE_FILE, 'r', encoding='utf-8') as f:
                    # json.load deserializa o JSON de volta para uma lista Python.
                    self.fila = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Erro ao carregar a fila ou arquivo corrompido: {e}")
                self.fila = []
        else:
            # Se o arquivo não existe, eu simplesmente inicio com uma fila vazia.
            self.fila = []

    # Método principal de construção da interface.
    def build(self):
        # Defino as configurações de tema e cor do app.
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        Window.clearcolor = (0.9, 0.93, 0.98, 1)

        # Chamo a função para carregar a fila salva assim que o app inicia.
        # Isso completa o ciclo de persistência de dados.
        self.load_queue()
        
        # O Kivy carrega o arquivo totem.kv automaticamente,
        # então o método build pode simplesmente retornar sem argumentos.
        return
        
# Ponto de entrada padrão para rodar a aplicação.
if __name__ == "__main__":
    TotemApp().run()