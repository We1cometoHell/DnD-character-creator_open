"""Модуль с методами для работы с БД."""

import asyncio

from dataclasses import dataclass
from models import db

classes = {
    'Бард': {
        'static': {
            'hit-die': 'd8',
            'base_code': 'cha',
            'armor': ('Легкий доспех',),
            'weapons': ('Простое оружие', 'Длинные мечи', 'Короткие мечи', 'Рапира', 'Арбалет, ручной'),
            'saves': ('dex', 'cha'),
        },
        'choice': {
            'инструменты': {'Музыкальный инструмент': 3},
            'навыки': {
                'skills': (
                    'Атлетика', 'Акробатика', 'Лoвкость рук', 'Скрытность', 'Магия', 'История', 'Анализ', 'Природа',
                    'Религия', 'Уход за животными', 'Проницательность', 'Медицина', 'Внимательность', 'Выживание',
                    'Обман', 'Запугивание', 'Выступление', 'Убеждение'),
                'count': 3},
            'начальное снаряжение': (
                ('Рапира', 'Длинный меч', 'Простое оружие'),
                ('Набор дипломата', 'Набор артиста'),
                ('Лютня', 'Музыкальный иснтрумент'),
                'Кожанный доспех', 'Кинжал'),
        },
        '1_level': ('Вдохновение барда:\nСвоими словами или музыкой вы можете вдохновлять других. Для этого вы должны '
                    'бонусным действием выбрать одно существо, отличное от вас, в пределах 60 футов, которое может вас '
                    'слышать. Это существо получает кость бардовского вдохновения — к6.В течение следующих 10 минут '
                    'это существо может один раз бросить эту кость и добавить результат к своему броску. Добавлять '
                    'можно к проверке характеристики, атаке или спасброску. Существо может принять решение о броске '
                    'кости вдохновения уже после броска к20, но должно сделать это прежде, чем Мастер объявит '
                    'результат броска. Как только кость бардовского вдохновения брошена, она исчезает. Существо может '
                    'иметь только одну такую кость одновременно.Вы можете использовать это умение количество раз, '
                    'равное модификатору вашей Харизмы, но как минимум один раз. Потраченные использования этого '
                    'умения восстанавливаются после продолжительного отдыха.\nВаша Кость бардовского вдохновения '
                    'изменяется с ростом вашего уровня в этом классе. Она становится к8 на 5 уровне, к10 на 10 уровне '
                    'и к12 на 15 уровне.',)
    },
    'Варвар': {
        'hit-die': 'd12',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Воин': {
        'hit-die': 'd10',
        'armor': ('Легкий доспех', 'Средний доспех', 'Тяжелый доспех', 'Щит')
    },
    'Волшебник': {
        'hit-die': 'd6',
        'base_code': 'int'
    },
    'Друид': {
        'hit-die': 'd8',
        'base_code': 'wis',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Жрец': {
        'hit-die': 'd8',
        'base_code': 'wis',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Изобретатель': {
        'hit-die': 'd8',
        'base_code': 'int',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Колдун': {
        'hit-die': 'd8',
        'base_code': 'cha',
        'armor': ('Легкий доспех',)
    },
    'Монах': {
        'hit-die': 'd8'
    },
    'Паладин': {
        'hit-die': 'd10',
        'base_code': 'cha',
        'armor': ('Легкий доспех', 'Средний доспех', 'Тяжелый доспех', 'Щит')
    },
    'Плут': {
        'hit-die': 'd8',
        'armor': ('Легкий доспех',)
    },
    'Следопыт': {
        'hit-die': 'd10',
        'base_code': 'wis',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Чародей': {
        'hit-die': 'd6',
        'base_code': 'cha'
    },
}

races = {
    'Гном': {
        'general': {
            'speed': 25,
            'languages': ('Общий', 'Гномий'),
            'abilities': 'Гномья хитрость\n'
                         'Вы совершаете с преимуществом спасброски Интеллекта, Мудрости и Харизмы '
                         'против магии.',
            'other_info': 'Тип: гуманоид\n'
                          'Размер: Маленький\n'
                          'Темное зрение: 60ф'
        },
        'variety': {
            'Лесной': {
                'stats': {
                    'int': 2,
                    'dex': 1
                },
                'additional abilities': 'Природная иллюзия\n'
                                        'Вы знаете заговор малая иллюзия.\n'
                                        'Базовой характеристикой для его использования является Интеллект.\n\n'
                                        'Общение с маленькими зверями\n'
                                        'С помощью звуков и жестов вы можете передавать простые понятия Маленьким или '
                                        'ещё меньшим зверям. Лесные гномы любят животных и часто держат белок, '
                                        'барсуков, кроликов, кротов, дятлов и других животных в качестве питомцев.\n\n'
            },
            'Скальный': {
                'stats': {
                    'int': 2,
                    'con': 1
                },
                'additional abilities': 'Ремесленные знания\n'
                                        'При совершении проверки Интеллекта (История) применительно к магическому, '
                                        'алхимическому или технологическому объекту, вы можете добавить к проверке '
                                        'удвоенный бонус мастерства вместо обычного.\n\n'
                                        'Жестянщик\n'
                                        'Вы владеете ремесленными инструментами (инструменты жестянщика). С их помощью '
                                        'вы можете, потратив 1 час времени и материалы на сумму в 10 зм, создать '
                                        'Крошечное механическое устройство (КД 5, 1 хит). Это устройство перестаёт '
                                        'работать через 24 часа '
                                        '(если вы не потратите 1 час на поддержание его работы). Вы можете Действием '
                                        'разобрать его; в этом случае вы можете получить обратно использованные '
                                        'материалы.\n'
                                        'Одновременно вы можете иметь не более трёх таких устройств.\n'
                                        'При создании устройства выберите один из следующих вариантов:\n'
                                        'Заводная игрушка. Эта заводная игрушка изображает животное, чудовище или '
                                        'существо, вроде лягушки, мыши, птицы, дракона или солдатика. Поставленная на '
                                        'землю, она проходит 5 футов в случайном направлении за каждый ваш ход, '
                                        'издавая звуки, соответствующие изображаемому существу.\n'
                                        'Зажигалка. Это устройство производит миниатюрный огонёк, с помощью которого '
                                        'можно зажечь свечу, факел или костёр. Использование этого устройства требует '
                                        'Действия.\n'
                                        'Музыкальная шкатулка. При открытии эта шкатулка проигрывает мелодию средней '
                                        'громкости. Шкатулка перестаёт играть если мелодия закончилась или если '
                                        'шкатулку закрыли.'
            }
        }
    },
    'Дварф': {
        'general': {
            'speed': 25,
            'languages': ('Общий', 'Дварфский'),
            'abilities': 'Дварфская устойчивость\n'
                         'Вы совершаете с преимуществом спасброски от яда, и вы получаете сопротивление к урону '
                         'ядом\n\n'
                         'Знание камня\n'
                         'Если вы совершаете проверку Интеллекта (История), связанную с происхождением работы по камню,'
                         ' вы считаетесь владеющим навыком История, и добавляете к проверке удвоенный бонус мастерства '
                         'вместо обычного.',
            'weapons': ('Боевой топор', 'Ручной топор', 'Легкий топор', 'Боевой молот'),
            'choice': {
                'инструменты': {
                    'tools': ('Инструменты кузнеца', 'Инструменты пивовара', 'Инструменты каменьщика'),
                    'count': 1
                },
            },
            'other_info': 'Тип: гуманоид\n'
                          'Размер: Маленький\n'
                          'Темное зрение: 60ф'
        },
        'variety': {
            'Горный': {
                'stats': {
                    'con': 2,
                    'str': 2
                },
                'armor': ('Легкие доспехи', 'Средние доспехи'),
            },
            'Холмовой': {
                'stats': {
                    'con': 2,
                    'wis': 1
                },
                'hp_modify': 1,
                'additional abilities': 'Дварфская выдержка\n'
                                        'Максимальное значение ваших хитов увеличивается на 1, и вы получаете 1 '
                                        'дополнительный хит с каждым новым уровнем.'
            }
        }
    }
}

backgrounds = {
    'Артист': {
        'static': {
            'skills': ('Акробатика', 'Выступление'),
            'tools': ('Набор для грима',),
            'equip': ('Костюм', 'Кошель'),
            'money': 15,
            'description': 'Вам нравится выступать на публике. Вы знаете, как их развлечь, очаровать и даже '
                           'воодушевить. Ваша поэзия может трогать сердца слушателей, пробуждать в них горе или '
                           'радость, смех или гнев.\n\n'
                           'Ваша музыка ободряет их или заставляет скорбеть. Ваши танцы захватывают, а шутки всегда '
                           'смешны. Чем бы вы ни занимались, ваша жизнь тесно связана с искусством.',
            'ability': 'По многочисленным просьбам\n\n'
                       'Вы всегда можете найти место для выступления. Обычно это таверна или постоялый двор, но это '
                       'может быть цирк, театр или даже двор знатного господина. В этом месте вы получаете '
                       'бесплатный постой и еду по скромным или комфортным стандартам (в зависимости от качества '
                       'заведения), если вы выступаете каждый вечер. Кроме того, ваши выступления делают вас '
                       'местной знаменитостью. Когда посторонние узнают вас в городе, в котором вы давали '
                       'представление, они, скорее всего, будут к вам относиться хорошо.'
        },
        'choice': {
            'инструменты': {'Музыкальный инструмент': 1},
            'снаряжение': (
                {'Музыкальный инструмент': 1},
                {'подарок от поклонницы': ('любовное письмо', 'локон волос', 'безделушка')}
            ),
            'personalization': {
                'type': {
                    'description': 'Номера артиста\n\n'
                                   'Хороший артист обладает разнообразными номерами. Выберите от одного до трёх амплуа '
                                   'из приведённых, чтобы определить, чем вы развлекаете публику.',
                    'variants': (
                        'Акробат', 'Актер', 'Жонглер', 'Музыкант', 'Певец',
                        'Пожиратель огня', 'Поэт', 'Рассказчик', 'Танцор', 'Шут'
                    )
                },
                'description': 'Успешные артисты могут овладевать вниманием публики, поэтому у них яркий или '
                               'напористый характер. Они могут быть романтичными, и в искусстве и красоте часто '
                               'обращаются к возвышенным идеалам.',
                'incident': {
                    'title': 'Я стал артистом, потому что...',
                    'variants': ('Моя семья зарабатывала на жизнь выступлениями на сцене, и я последовал их примеру.',
                                 'Я всегда понимал других людей достаточно хорошо, чтобы заставить их смеяться или '
                                 'плакать от моих историй или песен.',
                                 'Я сбежал из дома с труппой бродячих актёров.',
                                 'Однажды я увидел выступление барда, и в тот момент понял, для чего был рождён.',
                                 'Я зарабатывал гроши, выступая на улицах, и в конечном итоге стал известным.',
                                 'Бродячий актёр подобрал меня и обучил этому ремеслу.')
                },
                'personality': {
                    'variants': ('Для любой ситуации я найду подходящий рассказ.',
                                 'Куда бы я ни пришёл, я начинаю собирать местные слухи и распространять сплетни.',
                                 'Я безнадёжный романтик, всегда ищущий «кого-то особого».',
                                 'Никто не сердится на меня или возле меня подолгу, так как я могу разрядить любую '
                                 'напряжённую обстановку.',
                                 'Мне нравятся оскорбления, даже если они направлены на меня.',
                                 'Мне обидно, если я не нахожусь в центре внимания.',
                                 'Превыше всего я ценю совершенство.',
                                 'Моё настроение и намерения меняются так же быстро как ноты в музыке.')
                },
                'ideals': {
                    'variants': ('Красота. Выступая, я делаю мир лучше. (Добрый)',
                                 'Традиции. Рассказы, легенды и песни прошлого не должны забываться, так как они учат '
                                 'нас тому, кто мы такие. (Законный)',
                                 'Творчество. Миру нужны новые идеи и смелые действия. (Хаотичный)',
                                 'Жадность. Я занимаюсь всем этим ради денег и славы. (Злой)',
                                 'Народ. Мне нравится видеть улыбки на лицах во время выступления. В этом-то всё дело. '
                                 '(Нейтральный)',
                                 'Честность. Искусство должно отражать душу; оно должно идти изнутри и показывать, чем '
                                 'мы являемся. (Любой)')
                },
                'bonds': {
                    'variants': ('Мой инструмент — самое драгоценное, что у меня есть, и он напоминает мне о моей '
                                 'любви.',
                                 'Кто-то украл мой драгоценный инструмент, и когда-нибудь я верну его.',
                                 'Я хочу быть знаменитым, чего бы это ни стоило.',
                                 'Я боготворю героя старых рассказов, и всегда сравниваю свои поступки с его.',
                                 'Я всё сделаю, чтобы доказать превосходство над ненавистным конкурентом.',
                                 'Я сделаю что угодно для других членов моей старой труппы.')
                },
                'flaws': {
                    'variants': ('Я пойду на всё ради славы и известности.',
                                 'Не могу устоять перед смазливым личиком.',
                                 'Я не могу вернуться домой из-за скандала. Неприятности такого рода словно преследуют '
                                 'меня.',
                                 'Однажды я высмеял дворянина, который всё ещё хочет оторвать мне голову. Это была '
                                 'ошибка, но я могу повторить её ещё неоднократно.',
                                 'Я не могу скрывать свои истинные чувства. Острый язык всегда приносит мне '
                                 'неприятности.',
                                 'Я очень стараюсь исправиться, но друзьям не стоит на меня полагаться.')
                },
            },
        }
    },
    'Беспризорник': {
        'static': {
            'skills': ('Лoвкость рук', 'Скрытность'),
            'tools': ('Воровские инструменты', 'Набор для грима'),
            'equip': ('Маленький нож', 'Карта города, в котором вы выросли', 'Ручная мышь',
                      'Безделушка в память о родителях', 'Комплект повседневной одежды', 'Кошель'),
            'money': 10,
            'description': 'Вы выросли на улице в бедности и одиночестве, лишённые родителей. Никто не присматривал и '
                           'не заботился о вас, и вам пришлось научиться делать это самому. Вам приходилось постоянно '
                           'бороться за еду и следить за другими неприкаянными душами, способными обокрасть вас.\n\n'
                           'Вы спали на чердаках и в переулках, мокли под дождём и боролись с болезнями, не получая '
                           'медицинской помощи или приюта. Вы выжили, невзирая на все трудности, и сделали это '
                           'благодаря своей сноровке, силе или скорости.\n\n'
                           'Вы начинаете приключение с суммой денег, достаточной, чтоб скромно, но уверенно прожить '
                           'десять дней. Как вы получили эти деньги? Что позволило вам перейти к нормальной жизни, '
                           'преодолев нищету?',
            'ability': 'Городские тайны\n\n'
                       'Вы знаете тайные лазы и проходы городских улиц, позволяющие пройти там, где другие не увидят '
                       'пути. Вне боя вы (и ведомые вами союзники) можете перемещаться по городу вдвое быстрее '
                       'обычного.'
        },
        'choice': {
            'personalization': {
                'description': 'Жизнь в нищете оставляет свой отпечаток на беспризорниках. В них, как правило, сильна '
                               'привязанность к людям, с которыми они делили тяготы уличной жизни, или они исполнены '
                               'желанием добиться лучшей доли, и, возможно, расквитаться с богачами, от которых они '
                               'натерпелись.',
                'incident': {
                    'title': 'Я стал беспризорником, потому что...',
                    'variants': ('Жажда странствий заставила меня покинуть семью, чтобы увидеть свет. '
                                 'Я заботился о себе сам.',
                                 'Я сбежал от невыносимой домашней обстановки и нашёл свой собственный путь в мире.',
                                 'Монстры истребили мою деревню, и я был единтвенным уцелевшим. Мне надо было найти '
                                 'способ выжить.',
                                 'Известный вор заботился обо мне и других сиротах, и мы шпионили и воровали, '
                                 'чтобы оставаться вместе с ним.',
                                 'Однажды я проснулся на улице, один, голодный и без воспоминаний о моём раннем '
                                 'детстве.',
                                 'Мои родители умерли, и не осталось никого, кто мог бы обо мне позаботиться. '
                                 'Я вырос самостоятельно.')
                },
                'personality': {
                    'variants': ('В моих карманах полно побрякушек и объедков.',
                                 'Я задаю очень много вопросов.',
                                 'Я часто забиваюсь в узкие закутки, где никто не сможет добраться до меня.',
                                 'Я всегда сплю, прижавшись спиной к стене или дереву, сжимая узелок со всеми своими '
                                 'пожитками в руках.',
                                 'Я не воспитан, и ем как свинья.',
                                 'Я убеждён, что все, кто проявляют доброту ко мне, на самом деле скрывают злые '
                                 'намерения.',
                                 'Я не люблю мыться.',
                                 'Я прямо говорю о том, на что прочие предпочитают лишь намекнуть, или промолчать.')
                },
                'ideals': {
                    'variants': ('Уважение. Все люди, богатые ли они, или бедные, достойны уважения. (Добрый)',
                                 'Общность. Вы должны заботиться друг о друге, ведь никто другой этого не сделает. '
                                 '(Законный)',
                                 'Перемены. Убогие возвысятся, а великие падут. Перемены в природе вещей. (Хаотичный)',
                                 'Возмездие. Нужно показать богачам, чего стоит жизнь и смерть в трущобах. (Злой)',
                                 'Люди. Я помогаю тем, кто помогает мне. Это позволяет нам выжить. (Нейтральный)',
                                 'Устремление. Я готов доказать, что достоин лучшей жизни. (Любой)')
                },
                'bonds': {
                    'variants': ('Мой город или деревня это мой дом, и я буду защитить его.',
                                 'Я спонсирую приют, чтобы оградить других от того, что пришлось пережить мне.',
                                 'Я выжил лишь благодаря другому беспризорнику, что передал мне знания, как вести '
                                 'себя на улицах.',
                                 'Я в неоплатном долгу перед человеком, что сжалился и помог мне.',
                                 'Я избавился от нищеты, ограбив важного человека, и меня разыскивают.',
                                 'Никто не должен пережить те трудности, через которые пришлось пройти мне.')
                },
                'flaws': {
                    'variants': ('Если я в меньшинстве, то я убегу из битвы.',
                                 'Золото в любом виде выглядит для меня как большая куча денег, и я сделаю всё, '
                                 'чтобы его у меня стало больше.',
                                 'Я никогда не доверяю полностью кому бы то ни было, кроме себя.',
                                 'Я предпочту убить кого-нибудь во сне, нежели в честном поединке.',
                                 'Это не воровство, если я взял то, в чём нуждаюсь больше, чем кто-либо другой.',
                                 'Те, кто не могут позаботиться о себе, получат то, что заслужили.')
                },
            },
        }
    },
    'Благородный': {

    },
    'Гильдейский Ремесленник': {

    },
    'Гладиатор': {

    },
    'Купец Гильдии': {

    },
    'Моряк': {

    },
    'Мудрец': {

    },
    'Народный Герой': {

    },
    'Отшельник': {

    },
    'Пират': {

    },
    'Преступник': {

    },
    'Прислужник': {

    },
    'Рыцарь': {
        'static': {
            'skills': ('История', 'Убеждение'),
            'equip': ('Комплект отличной одежды', 'Кольцо-печатка', 'Свиток с генеалогическим древом', 'Кошель'),
            'money': 25,
            'description': 'Во многих обществах рыцари — низший слой благородного сословия, но это всё равно путь в '
                           'высший свет. Если хотите быть рыцарем, возьмите умение Слуги (смотрите во врезке) вместо '
                           'Привилегированности. Один из ваших слуг заменяется сквайром, помогающим вам, и при этом '
                           'учащимся рыцарству. Двое оставшихся могут ухаживать за вашим конём и доспехом (а также они '
                           'будут помогать его надевать).\n\n'
                           'Будучи символом благородства и идеалом галантной любви, вы можете добавить в снаряжение '
                           'знамя или подарок от леди, которой вы вручили своё сердце '
                           '(она может быть вашей привязанностью).',
            'ability': ('Привилегированность\n\n'
                        'Благодаря знатному происхождению, другие хорошо к вам относятся. Вас принимают в высшем '
                        'обществе, и считается, что у вас есть право посещать любые места. Обыватели изо всех '
                        'сил стараются сделать вам приятно и избежать вашего гнева, а другие высокородные '
                        'считают вас своей ровней. Если нужно, вы можете получить аудиенцию местного дворянина.',
                        'Альтернативное умение: Слуги\n\n'
                        'Если у вашего персонажа предыстория благородного, вы можете выбрать это умение вместо '
                        'Привилегированности. На вас работают трое слуг, преданных вашей семье. Это могут быть '
                        'помощники и слуги, а один может быть дворецким. Это обыватели, выполняющие за вас простую '
                        'работу, но они не будут за вас сражаться, не пойдут за вами в опасные места '
                        '(такие как подземелья), и они покинут вас, если их будут подвергать опасности или с '
                        'ними будут плохо обращаться.')
        },
        'choice': {
            'языки': {
                'count': 1
            },
            'personalization': {
                'personality': {
                    'variants': ('Я применяю так много лести, что все, с кем я разговариваю, чувствуют себя '
                                 'самыми чудесными и важными персонами в мире.',
                                 'Обыватели любят меня за доброту и великодушие.',
                                 'Один лишь взгляд на мои регалии заставляет перестать сомневаться в том, '
                                 'что я выше немытого отребья.',
                                 'Я много трачу на то, чтобы выглядеть потрясающе, и по последнему слову моды.',
                                 'Мне не нравится марать руки, и я не хочу умереть в каком-нибудь неподобающем месте.',
                                 'Несмотря на благородное рождение, я не ставлю себя выше народа. '
                                 'У всех нас течёт одинаковая кровь.',
                                 'Потеряв мою милость, обратно её не вернёшь.',
                                 'Оскорбишь меня, и я сотру тебя в порошок, уничтожу твоё имя, и сожгу твои поля.')
                },
                'ideals': {
                    'variants': ('Уважение. Уважение — мой долг. Кем бы ты ни был, к другим нужно относиться '
                                 'с уважением, невзирая на их происхождение. (Добрый)',
                                 'Ответственность. Я должен уважать тех, кто выше меня, а те, кто ниже меня, '
                                 'должны уважать меня. (Законный)',
                                 'Независимость. Я должен доказать, что справлюсь и без заботы своего ордена. '
                                 '(Хаотичный)',
                                 'Власть. Если соберу много власти, никто не посмеет указывать мне, что делать. (Злой)',
                                 'Семья. Настоящая кровь гуще. (Любое)',
                                 'Благородный долг. Я должен защищать тех, кто ниже меня, и заботиться о них. (Добрый)')
                },
                'bonds': {
                    'variants': ('Я пойду на любой риск, лишь бы заслужить признание семьи.',
                                 'Союз моего дома с другой благородной семьёй нужно поддерживать любой ценой.',
                                 'Нет никого важнее других членов моего ордена.',
                                 'Я влюблён в наследницу семейства, презираемого моей роднёй.',
                                 'Моя преданность правителю непоколебима.',
                                 'Обыватели должны считать меня своим героем.')
                },
                'flaws': {
                    'variants': ('Я втайне считаю всех ниже себя.',
                                 'Я скрываю позорную тайну, которая может уничтожить мою семью.',
                                 'Я слишком часто слышал завуалированные оскорбления и угрозы, и потому быстро '
                                 'впадаю в гнев.',
                                 'У меня неустанная страсть к плотским удовольствиям.',
                                 'Весь мир вращается вокруг меня.',
                                 'Я часто навлекаю позор на свою семью словами и действиями.')
                },
            },
        }
    },
    'Солдат': {

    },
    'Чужеземец': {

    },
    'Шарлатан': {

    },
    'Шпион': {

    },
}


@dataclass
class ManagerCollection:
    collection: str
    _id: str

    async def add_doc(self) -> None:
        await db[self.collection].insert_one({'_id': self._id})

    async def update_doc(self, doc: dict) -> None:
        await db[self.collection].update_one({'_id': self._id}, {'$set': doc})

    async def get_doc(self, key: str) -> dict:
        doc = await db[self.collection].find_one({'_id': self._id})
        return doc.get(key)


mc = ManagerCollection('backgrounds_ru', 'backgrounds')

asyncio.run(mc.update_doc(backgrounds))
