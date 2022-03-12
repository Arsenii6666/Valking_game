def activation(list_of_effects, event=None):
    for effect in list_of_effects:
        if effect is True:
            event.set_true_event_ansver()
            continue
        if type(effect)==str:
            print(effect)
            continue
        if type(effect)==tuple:
            if effect[0]:
                activation(effect[1], event)
            else:
                activation(effect[2], event)
            continue
        if type(effect)==list:
            effect[0](effect[1])
            continue
        effect()

class Room:
    def __init__(self, name) -> None:
        self.name=name
        self.south=None
        self.north=None
        self.west=None
        self.east=None
        self.character=None
        self.item=None
        self.event=None
    def set_description(self, description):
        self.description=description
    def get_details(self):
        print(self.name)
        print('--------------------')
        print(self.description)
        if self.north!=None:
            print(f"{self.north.name} на півночі")
        if self.south!=None:
            print(f"{self.south.name} на півдні")
        if self.west!=None:
            print(f"{self.west.name} на заході")
        if self.east!=None:
            print(f"{self.east.name} на сході")   
    def set_character(self, char):
        self.character=char
    def get_character(self):
        return self.character
    def set_item(self, item):
        self.item=item
    def get_item(self):
        return self.item
    def set_event(self, event):
        self.event=event
    def move(self, command):
        if 'північ'==command:
            return self.north
        if 'південь'==command:
            return self.south
        if 'захід'==command:
            return self.west
        if 'схід'==command:
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
    def __init__(self, name, description, quest=None) -> None:
        self.name=name
        self.description=description
        self.quest=quest
    def set_conversation(self, conversation):
        self.conversation=conversation
    def talk(self):
        if self.quest==None:
            print(f"[{self.name} каже]: {self.conversation}")
            return False
        else:
            print(f"[{self.name} каже]: {self.quest.description} Візьмешся? (Так/Ні)")
            while True:
                command = input("> ")
                if command=="Так":
                    print(f"У вас нове завдання: {self.quest.name}")
                    activation(self.quest.taking_event)
                    return True
                if command=="Ні":
                    print(f"[{self.name} каже]: Шкода.")
                    return False
                print("Нерозумію. Спробуй ще.")
    def set_quest(self, quest):
        self.quest=quest

    def describe(self):
        print(f"Тут є {self.name}!")
        print(self.description)

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
        if self.name=="Лімур":
            return True
        return False

class Item:
    def __init__(self, name) -> None:
        self.name=name
    def __str__(self) -> str:
        return f"{self.name}. {self.description}."
    def set_description(self, description):
        self.description=description
    def describe(self):
        print(f"Тут є [{self.name}] - {self.description}.")
    def get_name(self):
        return self.name

class Quest:
    def __init__(self, name, description, request, reward, taking_event) -> None:
        self.name=name
        self.request=request
        self.description=description
        self.reward=reward
        self.taking_event=taking_event
    def check_compliting(self):
        if self.request:
            activation(self.reward)
    def __str__(self) -> str:
        return f"Назва: {self.name}. Розмова з замовником: {self.description}."

class Event:
    def __init__(self, name, pretext, Yes, No, condition) -> None:
        self.name=name
        self.condition=condition
        self.Event_ansver=False
        self.pretext=pretext
        self.Yes=Yes
        self.No=No
    def triggering(self):
        if self.condition:
            print(f"Сталося наступне: {self.name}")
            print(self.pretext)
            while True:
                command = input("> ")
                if command=="Так":
                    activation(self.Yes, self)
                    break
                if command=="Ні":
                    activation(self.No, self)
                    break
                print("Нерозумію. Спробуй ще.")
            return True
        return False
    def set_true_event_ansver(self):
        self.Event_ansver=True
    def set_add_choise(self, choise):
        self.choises.append(choise)
