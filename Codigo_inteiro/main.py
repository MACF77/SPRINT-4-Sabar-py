# --- IMPORTS PARA MANIPULAÇÃO DE ARQUIVOS ---
import json
import os

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout 

Window.clearcolor = (0.9, 0.93, 0.98, 1)

KV = '''
# O KV continua exatamente o mesmo da versão anterior
ScreenManager:
    SplashScreen:
    MainScreen:
    AssessmentScreen:

<SplashScreen>:
    name: "splash"
    
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'background.png'

    FloatLayout:
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            spacing: dp(8)
            padding: dp(20)
            pos_hint: {'center_x': 0.5, 'y': 0.15}
            size_hint_x: 0.9
            md_bg_color: 1, 1, 1, 0.85 
            radius: [24,]

            MDLabel:
                text: "Bem-vindo ao Hospital Infantil Sabará"
                halign: "center"
                font_style: "H5"
                bold: True
                color: 0.2, 0.2, 0.2, 1 
                
            MDLabel:
                text: "Este é o nosso totem de autoatendimento."
                halign: "center"
                font_style: "Subtitle1"
                color: 0.3, 0.3, 0.3, 1
                adaptive_height: True
        
        MDSpinner:
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': 0.5, 'y': 0.35}
            color: app.theme_cls.primary_color

<MainScreen>:
    name: "main"

    MDFloatLayout:
        MDCard:
            size_hint: None, None
            size: dp(385), dp(525)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            md_bg_color: 173/255, 216/255, 230/255, 1
            radius: [28,]
            elevation: 0

        MDCard:
            id: form_card
            size_hint: None, None
            size: dp(380), dp(520)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            orientation: "vertical"
            padding: dp(25)
            spacing: dp(20)
            radius: [24,]
            elevation: 4

            MDLabel:
                text: "Formulário de Atendimento"
                halign: "center"
                font_style: "H4"
                size_hint_y: None
                height: self.texture_size[1]
                color: app.theme_cls.primary_color
                padding_y: dp(10)

            MDTextField:
                id: name_input
                hint_text: "Nome completo"
                icon_right: "account-circle-outline"
                max_text_length: 50
                mode: "fill"
                fill_color_normal: 0, 0, 0, 0.04
                radius: [12, 12, 0, 0]

            MDTextField:
                id: dob_input
                hint_text: "Data de nascimento (DD/MM/AAAA)"
                icon_right: "calendar-month-outline"
                on_text: root.schedule_format_dob()
                mode: "fill"
                fill_color_normal: 0, 0, 0, 0.04
                radius: [12, 12, 0, 0]

            MDTextField:
                id: rg_input
                hint_text: "Número do RG"
                icon_right: "card-account-details-outline"
                max_text_length: 15
                mode: "fill"
                fill_color_normal: 0, 0, 0, 0.04
                radius: [12, 12, 0, 0]

            MDTextField:
                id: contact_input
                hint_text: "Número de contato"
                icon_right: "phone-outline"
                max_text_length: 15
                input_filter: "int"
                mode: "fill"
                fill_color_normal: 0, 0, 0, 0.04
                radius: [12, 12, 0, 0]

            MDRaisedButton:
                text: "Iniciar Autoavaliação de Sintomas"
                size_hint_x: 1
                padding: dp(15)
                pos_hint: {"center_x": 0.5}
                on_release: root.validate_and_go()
                radius: [12,]

            MDFlatButton:
                text: "Sair"
                text_color: "gray"
                size_hint_x: 1
                pos_hint: {"center_x": 0.5}
                on_release: app.stop()

<AssessmentScreen>:
    name: "assessment"
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(15)
        spacing: dp(15)

        MDScrollView:
            MDBoxLayout:
                id: content_layout
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(12) 

                MDLabel:
                    text: "[b]Está com dor?[/b]"
                    markup: True
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(10)
                    MDCheckbox:
                        id: pain_yes
                        group: "pain"
                        size_hint_x: None
                        width: dp(48)
                    MDLabel:
                        text: "Sim"
                        valign: "middle"
                    MDCheckbox:
                        id: pain_no
                        group: "pain"
                        active: True
                    MDLabel:
                        text: "Não"
                        valign: "middle"
                MDTextField:
                    id: pain_level_input
                    hint_text: "Grau da dor (1 a 10)"
                    input_filter: "int"
                    max_text_length: 2
                    mode: "fill"
                    fill_color_normal: 0, 0, 0, 0.04
                    radius: [12, 12, 0, 0]

                MDLabel:
                    text: "[b]Está com febre?[/b]"
                    markup: True
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(10)
                    MDCheckbox:
                        id: fever_yes
                        group: "fever"
                        size_hint_x: None
                        width: dp(48)
                    MDLabel:
                        text: "Sim"
                        valign: "middle"
                    MDCheckbox:
                        id: fever_no
                        group: "fever"
                        active: True
                    MDLabel:
                        text: "Não"
                        valign: "middle"
                MDTextField:
                    id: temperature_input
                    hint_text: "Temperatura (°C)"
                    max_text_length: 4
                    on_text: root.format_temperature(self, self.text)
                    mode: "fill"
                    fill_color_normal: 0, 0, 0, 0.04
                    radius: [12, 12, 0, 0]

                MDLabel:
                    text: "[b]Está com náusea?[/b]"
                    markup: True
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(10)
                    MDCheckbox:
                        id: nausea_yes
                        group: "nausea"
                        size_hint_x: None
                        width: dp(48)
                    MDLabel:
                        text: "Sim"
                        valign: "middle"
                    MDCheckbox:
                        id: nausea_no
                        group: "nausea"
                        active: True
                    MDLabel:
                        text: "Não"
                        valign: "middle"

                MDLabel:
                    text: "[b]Está com vômito?[/b]"
                    markup: True
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(10)
                    MDCheckbox:
                        id: vomiting_yes
                        group: "vomiting"
                        size_hint_x: None
                        width: dp(48)
                    MDLabel:
                        text: "Sim"
                        valign: "middle"
                    MDCheckbox:
                        id: vomiting_no
                        group: "vomiting"
                        active: True
                    MDLabel:
                        text: "Não"
                        valign: "middle"
        
        MDRaisedButton:
            text: "Ver resultado"
            size_hint_y: None
            height: dp(50)
            pos_hint: {"center_x": 0.5}
            md_bg_color: app.theme_cls.primary_color
            on_release: root.process_assessment()
            radius: [12,]

        MDFlatButton:
            text: "Voltar"
            size_hint_y: None
            height: dp(40)
            pos_hint: {"center_x": 0.5}
            text_color: app.theme_cls.primary_color
            on_release:
                app.sm.current = "main"
'''

class SplashScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_main_screen, 4)

    def switch_to_main_screen(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'main'

class MainScreen(Screen):
    def schedule_format_dob(self):
        Clock.schedule_once(self.format_dob, 0)

    def format_dob(self, *args):
        field = self.ids.dob_input
        digits = ''.join(filter(str.isdigit, field.text))
        formatted = ''
        if len(digits) > 0:
            formatted += digits[:2]
        if len(digits) > 2:
            formatted += '/' + digits[2:4]
        if len(digits) > 4:
            formatted += '/' + digits[4:8]
        field.text = formatted

    def validate_and_go(self):
        self.manager.transition.direction = 'left'
        app = MDApp.get_running_app()
        name = self.ids.name_input.text.strip()
        dob = self.ids.dob_input.text.strip()
        rg = self.ids.rg_input.text.strip()
        contact = self.ids.contact_input.text.strip()

        missing = []
        if not name:
            missing.append("Nome completo")
        if not dob or len(dob) < 10:
            missing.append("Data de nascimento")
        if not rg:
            missing.append("Número do RG")
        if not contact:
            missing.append("Número de contato")

        if missing:
            dialog = MDDialog(
                title="Campos obrigatórios",
                text="Por favor preencha: " + ', '.join(missing),
                buttons=[MDFlatButton(text="OK")]
            )
            dialog.buttons[0].on_release = dialog.dismiss
            dialog.open()
        else:
            app.sm.current = "assessment"

class AssessmentScreen(Screen):
    def on_enter(self, *args):
        self.manager.transition.direction = 'right'

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
        try:
            if float(formatted.replace(',', '.')) > 42.2:
                formatted = "42,2"
        except (ValueError, TypeError):
            pass
        if instance.text != formatted:
            instance.text = formatted
            instance.cursor = (len(formatted), 0)

    def process_assessment(self):
        app = MDApp.get_running_app()
        main = app.root.get_screen("main")
        
        dor = self.ids.pain_yes.active
        grau_dor = 0
        try:
            grau_dor = int(self.ids.pain_level_input.text)
        except ValueError:
            grau_dor = 0
        if grau_dor > 10:
            grau_dor = 10

        febre = self.ids.fever_yes.active
        temp = 36.5
        try:
            temp = float(self.ids.temperature_input.text.replace(',', '.'))
        except (ValueError, TypeError):
            temp = 36.5
        if temp > 42.2:
            temp = 42.2

        nausea = self.ids.nausea_yes.active
        vomito = self.ids.vomiting_yes.active

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

        paciente_info = {
            'nome': main.ids.name_input.text,
            'rg': main.ids.rg_input.text,
            'urgencia': urgencia,
            'prioridade': prioridade
        }
        
        app.fila.append(paciente_info)
        app.fila.sort(key=lambda x: x['prioridade'])

        # --- CHAMADA PARA SALVAR A FILA ---
        # Após modificar a fila, nós a salvamos no arquivo.
        app.save_queue()

        posicao_fila = app.fila.index(paciente_info) + 1
        resumo = (
            "Nome: {}\n"
            "RG: {}\n\n"
            "Classificação: {}\n"
            "Sua posição na fila: {}º\n\n"
            "Por favor, aguarde na sala. Você será chamado em breve!"
        ).format(
            paciente_info['nome'],
            paciente_info['rg'],
            urgencia,
            posicao_fila
        )
        dialog = MDDialog(
            title="Resumo da Avaliação",
            text=resumo,
            size_hint=(0.9, None),
            height=dp(400),
            buttons=[MDFlatButton(text="OK")]
        )
        dialog.buttons[0].on_release = dialog.dismiss
        dialog.open()
        app.sm.current = "main"

class TotemApp(MDApp):
    # --- NOVAS FUNÇÕES E VARIÁVEIS PARA MANIPULAR ARQUIVOS ---
    
    # Nome do arquivo onde a fila será salva
    QUEUE_FILE = "patient_queue.json"

    def save_queue(self):
        """Salva a fila de pacientes atual no arquivo JSON."""
        try:
            with open(self.QUEUE_FILE, 'w') as f:
                json.dump(self.fila, f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar a fila: {e}")

    def load_queue(self):
        """Carrega a fila de pacientes do arquivo JSON, se ele existir."""
        if os.path.exists(self.QUEUE_FILE):
            try:
                with open(self.QUEUE_FILE, 'r') as f:
                    # Carrega a lista do arquivo
                    self.fila = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Erro ao carregar a fila ou arquivo corrompido: {e}")
                # Se houver erro, começa com uma fila vazia
                self.fila = []
        else:
            # Se o arquivo não existe, começa com uma fila vazia
            self.fila = []


    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.sm = Builder.load_string(KV)
        
        # --- CHAMADA PARA CARREGAR A FILA NA INICIALIZAÇÃO ---
        # Antes de rodar o app, carregamos os dados salvos.
        self.load_queue()

        self.sm.transition = SlideTransition()
        return self.sm

if __name__ == "__main__":
    TotemApp().run()