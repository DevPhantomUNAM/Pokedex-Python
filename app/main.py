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

        self.offset = 0

        self.create_elements()
        self.load_async_data()
        self.validate_previus_command()
    
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

    def load_async_pokemon(self, pokemon):
        thread = threading.Thread(target=self.load_pokemon,args=[pokemon])
        thread.start()

    def load_pokemon(self,pokemon):
        path = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon)
        response = requests.get(path)
        if response: 

            result = response.json()

            name = result['forms'][0]['name']
            abilities = list()

            for ability in abilities:
                name_ability = ability['ability']['name']
                abilities.append(name_ability)
            
            sprite = result['sprites']['front_default']

        else: 
            print("Error al hacer petición al servidor")

            

    def load_data(self):
        self.data.clear()
        path = 'https://pokeapi.co/api/v2/pokemon?offset={}&limit=20'.format(self.offset)

        response = requests.get(path)
        if response: 

            result = response.json()

            for pokemon in result['results']:
                name = pokemon['name']
                self.data.append(name)
        else: 
            print("Error al hacer petición al servidor")

        self.table.data = self.data

    #CALLBACKS
    def select_element(self,widget,row):
        if row:
            self.load_async_pokemon(row.name)
            print(row.name)

    def next(self, widget):
        self.offset +=1
        self.handler_command(widget)    
    
    def previus(self,widget):
        self.offset -=1
        self.handler_command(widget)

    def handler_command(self,widget):
        widget.enable = False

        self.load_async_data()

        widget.enable = True

        self.validate_previus_command()

    def validate_previus_command(self):
        self.previus_command.enable = not self.offset == 0

if __name__ == '__main__':
    pokedex = PokeDex('Pokedex','com.devphantom.org')
    pokedex.main_loop()