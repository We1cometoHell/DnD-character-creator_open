import json

_character_classes_ru = ["Бард", "Варвар", "Воин", "Волшебник", "Друид", "Жрец", "Изобретатель", "Колдун", "Монах",
                         "Паладин", "Плут", "Следопыт", "Чародей"]
_character_classes_en = ["Bard", "Barbarian", "Fighter", "Wizard", "Druid", "Cleric", "Artificer", "Warlock", "Monk",
                         "Paladin", "Rogue", "Ranger", "Sorcerer"]

with open('default_list.json', 'r', encoding='utf-8') as file:
    list_personage = json.load(file)

_class_personage = list_personage['info']
_name_character = input('Как будут звать вашего героя?')
