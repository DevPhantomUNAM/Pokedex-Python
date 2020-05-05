import toga
import requests
import threading


from const import *

class PokeDex(toga.App):
    def __init__(self,title,id):
        toga.App.__init__(self,title,id)

        self.title = title
        self.size = (WIDTH, HEIGHT)

        self.heading = ['Name']
        self.data = list()

        self.create_elements()
        self.load_async_data()
    
    def startup(self):
        self.main_window = toga.MainWindow('main', title=self.title, size=(self.size))

        box = toga.Box()
        split = toga.SplitContainer()
        split.content = [self.table, box]

        self.main_window.content = split
        self.main_window.toolbar.add(self.previus_command, self.next_command)

        self.main_window.show()

    def create_elements(self):
        self.create_table()
        self.create_toolbar()

    def create_toolbar(self):
        self.create_next_command()
        self.create_previus_command()

    def create_next_command(self):
        self.next_command = toga.Command(self.next, label='Next', icon=BULBASAUR_ICON)

    def create_previus_command(self):
        self.previus_command = toga.Command(self.previus, label='Previus', icon=METAPOD_ICON)


    def create_table(self):
        self.table = toga.Table(self.heading, data=self.data, on_select=self.select_element)

    def load_async_data(self): 
        thread = threading.Thread(target=self.load_data)
        thread.start()

    def load_data(self):
        path = 'https://pokeapi.co/api/v2/pokemon/'

        response = requests.get(path)
        if response: 

            result = response.json()

            for pokemon in result['results']:
                name = pokemon['name']
                self.data.append(name)
        else: 
            print("None")

        self.table.data = self.data

    #CALLBACKS
    def select_element(self,widget,row):
        if row:
            print(row.name)

    def next(self, widget):
        print("next")
    
    def previus(self,widget):
        print("Previus")

if __name__ == '__main__':
    pokedex = PokeDex('Pokedex','com.devphantom.org')
    pokedex.main_loop()