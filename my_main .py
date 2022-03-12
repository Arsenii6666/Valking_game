import game
"""S.t.a.l.k.e.r 2. Pre alpha, free to play mobile version"""

print("""Час: 04:53, 18.06.2015, альтернативна історія.
Місце: Кордон Чорнобильської зони відчудження. Ви за периметром самої Зони.
Ви: агент СБУ під прикриттям.
Задача: знайти й ліквідувати сталкера з призвіськом "Лімур".
За наявною інформацією, він корегує надходження в Зону великої кількості зброї,
що заважає проведенню операцій на її території.
За свідчиннями інформатора, він має скоро прибути до Кордону за новою партією.
Легенда: ви звичайний сталкер-авантюрист, який з батьківським ПМ-ом і певними накопиченнями намагається проникнути за периметр.
Тут ви хочете розбагатіти, витративши гроші на спорядження. З собою маєте певний мінімальний набір.
Основне спорядження для завдання можна забрати у спеціальному сховищі на колишньому елеваторі.
Інформатор чекає вас і готовий привести на зустріч, аби ви купили спорядження зразу на місці.
Протягом гри доступні команди: бій, говорити, північ, південь, схід, захід, інвентар, квести""")

def Death():
    global dead
    dead=True

def Change_current_room(room):
    global current_room
    current_room=room

Perimetr=game.Room("Перед Зоною")
Perimetr.set_description("На горизонті чисто. Поки. Треба спішити.")

Inside=game.Room("Місце зустрічі з інформатором")
Inside.set_description("Галявина, є кілька густих кущів. На них ростуть ягоди, які я б не їв.")

Vilage=game.Room("Табір новачків")
Vilage.set_description("Всі, хто вперше прибувають в зону зупиняються тут.")

Elevator=game.Room("Елеватор")
Elevator.set_description("Колишній елеватор. Нічого цікавого тут немає, якщо не знати, де шукати.")

Field=game.Room("Поле")
Field.set_description("Просто пусте поле. Іноді тут чутно собачий гавкіт.")

Kpp=game.Room("КПП")
Kpp.set_description("Давно зайнятий бандитами колишній КПП. Натяк, що пускати справи Зони на самоплив не варто.")

Perimetr.link_room(Inside, "north")
Inside.link_room(Vilage, "north")
Elevator.link_room(Vilage, "south")
Vilage.link_room(Field, "east")
Elevator.link_room(Kpp, "east")
Field.link_room(Kpp, "north")

current_room = Perimetr
backpack=[]
quest_list=[]
dead = False

Pistol=game.Item("Пм")
Pistol.set_description("В умовах Зони ним можна вбити лише або обеззброєного, або надто довірливого.")
Perimetr.set_item(Pistol)

Sniper_rifle=game.Item("Снайперська гвинтівка")
Sniper_rifle.set_description("Для ліквідації вашої цілі. Дуже обмежений боєзапас, не витрачайте його впусту.")
Elevator.set_item(Sniper_rifle)

Hunting_rifle=game.Item("Мисливська гвинтівка")
Hunting_rifle.set_description("Гарний варіант для вбивства різного роду мутантів.")

Limur=game.Enemy("Лімур","Твоя ціль.")
Limur.set_conversation("Ти де? Якщо не з'явишся в найблищий час, я відміню договір.")
Limur.set_weakness("Снайперська гвинтівка")

Dogs=game.Enemy("Сліпі собаки", "Мутанти")
Dogs.set_conversation("Гав! Гав!")
Dogs.set_weakness("Мисливська гвинтівка")
Field.set_character(Dogs)

Sidorovich=game.Character("Сидорович","Жадібний жирний торгаш.")
Sidorovich.set_conversation("Хабар приніс?")
Vilage.set_character(Sidorovich)

Informator=game.Event("Ти зустрів інформатора.",
"""[Інформатор каже]: О, добре що ти тут. Везучий ти, що на патруль не нарвався. Ходімо за мною
Ти можеш його зараз вбити. Однак пам'ятай, що ти ще не знаєш, як дібратись до Лемура.
Команди: Так/Ні """,
#Yes
[ 
    (backpack==[],
        #True
        ["Він мертвий. Це до кращого - нема ризику, що тебе вб'ють.", True],
        #False
        ["В тебе не було зброї, тому тобі нічого не вдалось. Ти мертвий", Death]
    )
],
#No
[
"Ти пішов за ним",
[Change_current_room, Vilage]
],
#When it happend
True)
Inside.set_event(Informator)

In_village=game.Event("Ви в таборі новачків. Що він планує?",
"""Інформатор спустився в якийсь бункер, не далеко від табору. Через певний час він повернувся.
[Інформатор каже]: Я про все домовився, Лемур нас чекає. Ходімо. Зустрінемось з ним на КПП, підемо через поля.
Ви підете з ним? (в іншому випадку, вам доведеться прибрати його, як небажаного свідка.)
Команди: Так/Ні """,
#Yes
[ 
    "Ви пішли в поля",
    Kpp.set_character(Limur),
    [Change_current_room, Field],
    True
],
#No
[
    (backpack==[],
        #True
        ["Ти пустив йому кулю в голову. Інші сталкери це помітили й подібної поведінки не зрозуміли й вбили тебе", Death],
        #False
        ["В тебе не було зброї, тому тобі нічого не вдалось. Ти мертвий.", Death]
    )
],
#When it happend
Informator.Event_ansver)
Vilage.set_event(In_village)

On_field=game.Event("Ви вийшли на поле",
"""Поряд нема свідків. Це можливість позбутися від вже не потрібного інформатора. Ви будете це робити?
Команди: Так/Ні """,
#Yes
[ 
    "3 кулі в потилицю закінчили життя цього бідолаги. Його труп з'їдять місцеві собаки.",
    True
],
#No
[
    "Ви прийшли на зустріч. На щастя, вас не запідозрили в зраді, але ціль зникла. Завдання провалено.",
    Death
],
#When it happend
not Informator.Event_ansver
)
Field.set_event(On_field)

Hunting_dogs=game.Quest("Охота на сліпих собак",
"""для всіх новеньких я маю невелике завданнячко: вбити сліпих собак в полі на схід від табору.
Як справишся, доведеш, що вартий більшого. Я допоможу тобі вийти на контакт з одною особою,
яка допоможе тобі з більш серйозною зброєю. Й якості передплати, візьмеш мою стару мисливську рушницю.""",
Field.character==None,
#Revard
[
    "[На КПК прийшло повідомлення від Сидоровича]: Гарна робота, йди на закинутий КПП. Тебе вже чекають.",
    Kpp.set_character(Limur) 
],
#What happand if you take it
[
    Vilage.set_item(Hunting_rifle)
]
)

while dead == False:
    print("\n")
    current_room.get_details()

    inhabitant = current_room.get_character()
    if inhabitant is not None:
        event =inhabitant.describe()

    item = current_room.get_item()
    if item is not None:
        item.describe()
    if current_room.event!=None:
        if not current_room.event.triggering():
            command = input("> ")
        else:
            current_room.event=None
            continue
    else:
        command = input("> ")

    if command in ["північ", "південь", "схід", "захід"]:
        # Move in the given direction
        current_room = current_room.move(command)
    elif command == "говорити":
        # Talk to the inhabitant - check whether there is one!
        if inhabitant is not None:
            if inhabitant.talk():
                quest_list.append(inhabitant.quest)
                inhabitant.quest=None
    elif command == "бій":
        if inhabitant is not None:
            # Fight with the inhabitant, if there is one
            print("Що вибереш для бою?")
            fight_with = input()

            # Do I have this item?
            if fight_with in backpack:

                if inhabitant.fight(fight_with) == True:
                    # What happens if you win?
                    print("Вітаю! Противник знешкоджений.")
                    current_room.character = None
                    if inhabitant.get_defeated():
                        print("Вітаю! Місія виконана.")
                        dead = True
                else:
                    # What happens if you lose?
                    print("О ні, ти програв.")
                    print("Кінець гри")
                    dead = True
            else:
                print("В тебе немає " + fight_with)
        else:
            print("Тут нема ворогів")
    elif command == "взяти":
        if item is not None:
            print("Ти взяв " + item.get_name() + " з собою.")
            backpack.append(item.get_name())
            current_room.set_item(None)
        else:
            print("Пусто. Нема чого взяти.")
    elif command=="інвентар":
        for i in backpack:
            print(i)
    else:
        print("Я не знаю команди " + command)
    for quest in quest_list:
        quest.check_compliting()
