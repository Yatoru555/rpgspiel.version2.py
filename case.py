
import random
from colorama import Fore, Back, Style, init 

init(autoreset=True)


def rainbow_text(text):
    colors = [
        Fore.RED,
        Fore.YELLOW,
        Fore.GREEN,
        Fore.CYAN,
        Fore.BLUE,
        Fore.MAGENTA
    ]

    result = ""
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += color + char

    return result

class CaseSystem:
    def __init__(self):
        self.cases = {
            1: {
                "name": "обычный сундук",
                "price": 100,
                "rewards": [
                    {"type": "coins", "value": 75},
                    {"type": "coins", "value": 10},
                    {"type": "coins", "value": 150},
                    {"type": "hp", "value": 3},
                    {"type": "damage", "value": 2},
                ],
                "color": Fore.LIGHTBLACK_EX 
            },

            2: {
                "name": "необычный сундук",
                "price": 300,
                "rewards": [
                    {"type": "coins", "value": 225},
                    {"type": "coins", "value": 100},
                    {"type": "coins", "value": 400},
                    {"type": "hp", "value": 7},
                    {"type": "damage", "value": 7},
                ],
                "color": Fore.CYAN
            },

            3: {
                "name": "редкий сундук",
                "price": 800,
                "rewards": [
                    {"type": "coins", "value": 700},
                    {"type": "coins", "value": 300},
                    {"type": "coins", "value": 1000},
                    {"type": "hp", "value": 25},
                    {"type": "damage", "value": 20},
                ],
                "color": Fore.BLUE
            },

            4: {
                "name": "Эпический сундук",
                "price": 2500,
                "rewards": [
                    {"type": "coins", "value": 1250},
                    {"type": "coins", "value": 1800},
                    {"type": "coins", "value": 2500},
                    {"type": "coins", "value": 3300},
                    {"type": "coins", "value": 4000},
                    {"type": "hp", "value": 20},
                    {"type": "hp", "value": 30},
                    {"type": "hp", "value": 40},
                    {"type": "hp", "value": 55},
                    {"type": "hp", "value": 100},
                    {"type": "damage", "value": 30},
                    {"type": "damage", "value": 50},
                    {"type": "damage", "value": 75},
                    {"type": "damage", "value": 100},
                ],
                "color": Fore.MAGENTA
            },

            5: {
                "name": "Легендарный сундук",
                "price": 5000,
                "rewards": [
                    {"type": "coins", "value": 2000},
                    {"type": "coins", "value": 3000},
                    {"type": "coins", "value": 4000},
                    {"type": "coins", "value": 5500},
                    {"type": "coins", "value": 6600},
                    {"type": "hp", "value": 40},
                    {"type": "hp", "value": 66},
                    {"type": "hp", "value": 100},
                    {"type": "hp", "value": 200},
                    {"type": "hp", "value": 300},
                    {"type": "damage", "value": 50},
                    {"type": "damage", "value": 80},
                    {"type": "damage", "value": 140},
                    {"type": "damage", "value": 230},
                    {"type": "damage", "value": 300},

                ],
                "color": Fore.YELLOW
            },

            6: {
                "name": "Мифический сундук",
                "price": 7500,
                "rewards": [
                    {"type": "coins", "value": 4500},
                    {"type": "coins", "value": 5600},
                    {"type": "coins", "value": 7000},
                    {"type": "coins", "value": 8200},
                    {"type": "coins", "value": 10000},
                    {"type": "hp", "value": 130},
                    {"type": "hp", "value": 225},
                    {"type": "hp", "value": 300},
                    {"type": "hp", "value": 400},
                    {"type": "damage", "value": 75},
                    {"type": "damage", "value": 100},
                    {"type": "damage", "value": 150},
                    {"type": "damage", "value": 200},
                ],
                "color": Fore.RED
            },

            7: {
                "name": "Всемогущий сундук",
                "price": 15000,
                "rewards": [
                    {"type": "coins", "value": 10000},
                    {"type": "coins", "value": 12500},
                    {"type": "coins", "value": 14000},
                    {"type": "coins", "value": 16000},
                    {"type": "coins", "value": 20000},
                    {"type": "hp", "value": 350},
                    {"type": "hp", "value": 475},
                    {"type": "hp", "value": 600},
                    {"type": "damage", "value": 100},
                    {"type": "damage", "value": 160},
                    {"type": "damage", "value": 225},
                    {"type": "damage", "value": 300},
                ],
                "color": "rainbow"

            }

        }

    def show_case(self):
        print("\n== Сундук удачи ==")
        for key, case in self.cases.items():

            if case["color"] == "rainbow":
                text = f"{key}. {case['name']} - {case['price']} золота!"
                print(rainbow_text(text))
            else:
                print(f"{case['color']}{key}. {case['name']} - {case['price']} золота!")

    def open_case(self, hero):
        self.show_case()

        choice = input("выберите сундук:-> ")

        if not choice.isdigit():
            print("ошибка ввода. попробуйте еще раз!")
            return
        
        choice = int(choice)

        if choice not in self.cases:
            print("ошибка ввода")
            return
        
        selected_case = self.cases[choice]

        
        if hero.coins < selected_case["price"]:
            print("Недостаточно золота!")
            return

        hero.coins -= selected_case["price"]

        print("Открываем кейс: ")

        reward = random.choice(selected_case["rewards"])

        if reward["type"] == "coins":
            hero.coins += reward["value"]
            print(f"вы получили {reward['value']}")

        elif reward["type"] == "hp":
            hero.max_hp += reward["value"]
            hero.hp = hero.max_hp
            print(f"вы получили {reward['value']}")

        elif reward["type"] == "damage":
            hero.damage += reward["value"]
            print(f"урон увеличен на {reward['value']}")

        