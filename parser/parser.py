from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

character_class = 'bard'
url_ttg = f'https://ttg.club/classes/{character_class}'

# _character_classes_ru = ['бард', 'варвар', 'воин', 'волшебник', 'друид', 'жрец', 'изобретатель', 'колдун', 'монах',
#                          'паладин', 'плут', 'следопыт', 'чародей']
#
# _character_classes_en = ['artificer', 'barbarian', 'bard', 'cleric', 'druid', 'fighter', 'monk', 'paladin', 'ranger',
#                          'rogue', 'sorcerer', 'warlock', 'wizard']


# class CharacterClass:
#     _character_classes_dict = {'бард': 'artificer', 'варвар': 'barbarian', 'воин': 'bard', 'волшебник': 'cleric',
#                                'друид': 'druid',
#                                'жрец': 'fighter', 'изобретатель': 'monk', 'колдун': 'paladin', 'монах': 'ranger',
#                                'паладин': 'rogue',
#                                'плут': 'sorcerer', 'следопыт': 'warlock', 'чародей': 'wizard'}


driver = webdriver.Chrome()
driver.get(url_ttg)

time.sleep(5)

element = driver.find_element(By.CLASS_NAME, "class-detail__body--inner")

# Получаем содержимое элемента
content = element.get_attribute("innerHTML")

# Закрываем браузер
driver.quit()

soup = BeautifulSoup(content, 'html.parser')
class_content = soup.find_all(class_='content')

data = []

for item in class_content:
    data.append(' '.join(item.stripped_strings))

print(data)
