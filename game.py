class Room:
    def __init__(self, name) -> None:
        self.name=name
        self.south=None
        self.north=None
        self.west=None
        self.east=None
        self.character=None
        self.item=None
    def set_description(self, description):
        self.description=description
    def get_details(self):
        print(self.name)
        print('--------------------')
        print(self.description)
        if self.north!=None:
            print(f"The {self.north.name} is north")
        if self.south!=None:
            print(f"The {self.south.name} is south")
        if self.west!=None:
            print(f"The {self.west.name} is west")
        if self.east!=None:
            print(f"The {self.east.name} is east")   
    def set_character(self, char):
        self.character=char
    def get_character(self):
        return self.character
    def set_item(self, item):
        self.item=item
    def get_item(self):
        return self.item
    def move(self, command):
        if 'north'==command:
            return self.north
        if 'south'==command:
            return self.south
        if 'west'==command:
            return self.west
        if 'east'==command:
            return self.east
    def link_room(self, room, command):
        if 'north'==command:
            self.north=room
            room.south=self
        if 'south'==command:
            room.north=self
            self.south=room
        if 'west'==command:
            self.west=room
            room.east=self
        if 'east'==command:
            room.west=self
            self.east=room
class Character:
    def __init__(self, name, description) -> None:
        self.name=name
        self.description=description
    def set_conversation(self, conversation):
        self.conversation=conversation
    def talk(self):
        print(f"[{self.name} says]: {self.conversation}")
    def describe(self):
        print(f"{self.name} is here!")
        print(self.description)
defeated=0
class Enemy(Character):
    
    def __init__(self, name, description) -> None:
        super().__init__(name, description)
    def set_weakness(self, weakness):
        self.weakness=weakness
    def fight(self, item):
        global defeated
        if self.weakness==item:
            defeated+=1
        return self.weakness==item
    def get_defeated(self):
        global defeated
        return defeated
class Item:
    def __init__(self, name) -> None:
        self.name=name
    def set_description(self, description):
        self.description=description
    def describe(self):
        print(f"The [{self.name}] is here - {self.description}")
    def get_name(self):
        return self.name
    