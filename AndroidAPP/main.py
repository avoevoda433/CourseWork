import json

import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField


class MainApp(MDApp):
    def build(self):
        sm.add_widget(MainScreen())
        return sm


class MainScreen(Screen):
    def __init__(self):
        super().__init__()

        def check_connection(self):
            url = f"http://{input_setting1.text}:{input_setting2.text}/check"
            with open('data.json', 'w') as json_file:
                data_to_serialize = {
                    'ip': input_setting1.text,
                    'port': input_setting2.text,
                    'network': input_setting3.text
                }
                json.dump(data_to_serialize, json_file)
            try:
                response = requests.get(url)
                response.raise_for_status()
                status_text.theme_text_color = "Custom"
                status_text.text_color = 'green'
                status_text.text = 'OK'
                return 1
            except requests.RequestException as e:
                status_text.theme_text_color = "Custom"
                status_text.text_color = 'red'
                status_text.text = 'Error: check ip, port values'
                return 0

        def get_additional_pc_info(self, ip):
            end_ip = ip.text[4:15]+':5200'
            url = f"http://{input_setting1.text}:{input_setting2.text}/computer?ip={end_ip}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                self.data = response.json()
                try:
                    popup = Popup(title='Info about PC',
                                  title_color='blue',
                                  title_size=24,
                                  content=MDLabel(text=f'\nIP: {self.data["IP"]}\n'
                                                       f'Hostname: {self.data["Host Name"]}\n'
                                                       f'Processor: {self.data["Processor"]}\n'
                                                       f'RAM: {self.data["Memory"]} GB\n'
                                                       f'Total drive space: {self.data["Total"]} GB\n'
                                                       f'Used drive space: {self.data["Used"]} GB\n'
                                                       f'Available drive space: {self.data["Free"]} GB\n'),
                                  size_hint=(None, None), size=(340, 300),
                                  background="white")
                except:
                    popup = Popup(title='Info about PC',
                                  title_size=24,
                                  title_color='blue',
                                  content=MDLabel(text='The information collection program is not installed on the computer'),
                                  size_hint=(None, None), size=(340, 170),
                                  background="white")
                popup.open()
            except requests.RequestException as e:
                return {"error": str(e)}

        def get_info(self):
            url = f"http://{input_setting1.text}:{input_setting2.text}/computers?ip_range={input_setting3.text}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                self.data = response.json()
                pc_list.clear_widgets()
                for pc in self.data:
                    pc_list.add_widget(MDFlatButton(text=f'IP: {pc["ip"]}\n Hostname: {pc["hostname"]}',
                                                    size_hint=(0.8, None), on_press=lambda ip=pc['ip']: get_additional_pc_info(self, ip)))
            except requests.RequestException as e:
                return {"error": str(e)}

        input_setting1 = MDTextField(hint_text='Server IP address')
        input_setting2 = MDTextField(hint_text='Server port')
        input_setting3 = MDTextField(hint_text='Scan network')
        try:
            with open('data.json', 'r') as json_file:
                loaded_data = json.load(json_file)
                input_setting1.text, input_setting2.text, input_setting3.text = loaded_data.values()
        except:
            pass
        status_text = MDLabel(halign='center')
        check_btn = MDFlatButton(text="Check connection",
                                 theme_text_color="Custom",
                                 md_bg_color='blue',
                                 text_color='white',
                                 size_hint=(1, None),
                                 on_press=check_connection)

        update_btn = MDFlatButton(text="Update info",
                                  theme_text_color="Custom",
                                  md_bg_color='blue',
                                  text_color='white',
                                  size_hint=(1, None),
                                  on_press=get_info)

        main_layout = FloatLayout()
        setting_layout = GridLayout(padding=30,
                                    spacing=20,
                                    cols=1,
                                    rows=5)

        pc_layout = BoxLayout(padding=30,
                              spacing=20,
                              orientation='vertical')

        pc_info_layout = MDScrollView()
        pc_list = MDList(spacing=20)

        pc_info_nav_item = MDBottomNavigationItem(
                           name='Main',
                           text='PCInfo',
                           icon='pc.png')

        setting_nav_item = MDBottomNavigationItem(
                           name='second',
                           text='Settings',
                           icon='set.png')

        self.add_widget(main_layout)
        BottomBar = MDBottomNavigation()

        setting_layout.add_widget(input_setting1)
        setting_layout.add_widget(input_setting2)
        setting_layout.add_widget(input_setting3)
        setting_layout.add_widget(check_btn)
        setting_layout.add_widget(status_text)

        pc_info_layout.add_widget(pc_list)
        pc_info_nav_item.add_widget(pc_info_layout)
        pc_info_nav_item.add_widget(update_btn)
        setting_nav_item.add_widget(setting_layout)

        BottomBar.add_widget(pc_info_nav_item)
        BottomBar.add_widget(setting_nav_item)

        main_layout.add_widget(BottomBar)


sm = ScreenManager()

if __name__ == '__main__':
    MainApp().run()