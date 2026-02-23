

import random
from enemies import level_farm
from Shop import Shop
import json
from upgrade import UpgradeSystem 
import case

SAVE_FILE = "savegame.json" #======= сохраняем данные игрока =========

def save_game(game):
    data = {
        "profile": {"name": game.player.name, "age": game.player.age},
        "hero": {
            "class": type(game.hero).__name__,
            "name": game.hero.name,
            "level": game.hero.level,
            "hp": game.hero.hp,
            "max_hp": game.hero.max_hp,
            "damage": game.hero.damage,
            "xp": game.hero.xp,
            "coins": game.hero.coins,
            "inventory": [item.name for item in game.hero.inventory]
        },
        "current_level": game.current_level,
        "completed_levels": list(game.completed_levels)
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Игра сохранена!")

def load_game(game):
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        
        game.player.name = data["profile"]["name"]
        game.player.age = data["profile"]["age"]

        
        cls_name = data["hero"]["class"]
        hero_classes = {
            "Assassin": Assassin,
            "Warrior": Warrior,
            "Archer": Archer,
            "Monk": Monk,
            "Berserk": Berserk
        }

        game.hero = hero_classes[cls_name](game.player.name)
        hero_data = data["hero"]
        game.hero.level = hero_data["level"]
        game.hero.hp = hero_data["hp"]
        game.hero.max_hp = hero_data["max_hp"]
        game.hero.damage = hero_data["damage"]
        game.hero.xp = hero_data["xp"]
        game.hero.coins = hero_data["coins"]
        game.hero.inventory = [type("Item", (), {"name": name})() for name in hero_data["inventory"]]

        game.current_level = data["current_level"]
        game.completed_levels = set(data["completed_levels"])

        print("Игра загружена!")
    except FileNotFoundError:
        print("Сохранений нет.")

#=======  конец сохранения данных   ========

#=== создание профиля
class Profile:
    def __init__(self):
        self.name = None
        self.age = None
    
    def set_name(self):
        while True:
            name = input("придумайте юзер:-> ")
            if name.replace(" ", "").isalpha():
                self.name = name
                print(f" ваше имя: {self.name}")
                break
            else:
                print("ошибка ввода. попробуйте еще раз!")

    def set_age(self):
        while True:
            age = input("введите ваш возраст:-> ")
            if age.isdigit():
                age = int(age)
                if 6 <= age <= 80:
                    self.age = age
                    print(f" ваш возраст: {self.age}")
                    break
                else:
                    print("ошибка ввода возраста")
            else:
                print("ошибка ввода. попробуйте еще раз!")

#=== изменить профиль
    def edit_profile(self):
        while True:
            print("\n== изменить профиль ==")
            print("1. юзер")
            print("2. возраст")
            print("3. ничего. выйти")

            choice = input("выберите действие:-> ")

            if not choice.isdigit():
                print("ошибка ввода. попробуйте еще раз!")
                continue

            choice = int(choice)

            if choice == 1:
                self.set_name()
                break

            elif choice == 2:
                self.set_age()
                break

            elif choice == 3:
                print("выйти")
                break
            else:
                print("ошибка ввода. попробуйте еще раз!")

#создаем характеристику 
class Character:
    def __init__(self, name, hp, damage):
        self.name = name
        self.max_hp = hp
        self.damage = damage
        self.hp = hp
        self.xp = 0
        self.coins = 0
        self.level = 1
        self.inventory = []

    def gain_coins(self, amount):
        self.coins += amount
        print(f" вы получили: {amount} золота!")
        
    
    def gain_exp(self, amount):
        self.xp += amount
        print(f" вы получили: {amount} exp!")

        while self.xp >= self.level * 30:
            self.xp -= self.level * 30
            self.level += 1
            self.max_hp += 10
            self.damage += 5
            self.hp = self.max_hp
            print(f"ур. героя повышен: {self.level}!")

    
    def attack(self, enemy):
        enemy.take_damage(self.damage)


    def take_damage(self, amount):
        self.hp -= amount


    def reset(self):
        self.hp = self.max_hp


# Враги
def create_enemy(level):
    data = level_farm.get(level)
    if not data:
        # Если уровня нет — создаём базового врага
        return Character(f"враг уровня {level}", 10 + level*5, 5 + level*3)
    
    enemy = Character(data["name"], data["hp"], data["damage"])
    # добавляем награды прямо из словаря
    enemy.gold_reward = data["gold"]
    enemy.xp_reward = data["exp"]
    return enemy


#============== Полоска HP
def show_hp_bar(character):
    bar_length = 20
    hp_ratio = character.hp / character.max_hp
    filled = int(hp_ratio * bar_length)
    empty = bar_length - filled
    print(f"{character.name} HP: [{'█'*filled}{' '*empty}] {character.hp}/{character.max_hp}")


#============ Герои ============
class Assassin(Character):
    def __init__(self, name):
        super().__init__(name, hp=90, damage=30)
        self.crit_chance = 20

    def attack(self, enemy):
        if random.randint(1, 100) <= self.crit_chance:
            print("КРИТ УДАР!") #=========== Шанс крит удара для Ассассина
            enemy.take_damage(self.damage * 2)
        else:
            super().attack(enemy)



class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, hp=130, damage=18)
        self.dodge_chance = 20

#====== шанс уклониться от удара
    def take_damage(self, amount):
        if random.randint(1, 100) <= self.dodge_chance:
            print("воин пропустил удар!")
        else:
            super().take_damage(amount)



class Archer(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, damage=27)
        self.double_hit_chance = 20

#========= шанс на двойной удар
    def attack(self, enemy):
        hits = 2 if random.randint(1, 100) <= self.double_hit_chance else 1
        for _ in range(hits):
            super().attack(enemy)



class Monk(Character):
    def __init__(self, name):
        super().__init__(name, hp=145, damage=15)
        self.heal_chance = 20

#======== исцеление для монаха
    def take_damage(self, amount):
        super().take_damage(amount)
        if random.randint(1, 100) <= self.heal_chance:
            heal = int(self.max_hp * 0.2)
            self.hp = min(self.max_hp, self.hp + heal)
            print(f" монах исцеляется на {heal} hp!")



class Berserk(Character):
    def __init__(self, name):
        super().__init__(name, hp=105, damage=27)
    
#========== ярость ==========
    def attack(self, enemy):
        if self.hp < self.max_hp * 0.3:
            print("Берсерк в ярости!")
            enemy.take_damage(int(self.damage * 1.5))
        else:
            super().attack(enemy)



class Game:
    def __init__(self):
        self.player = Profile()
        self.hero = None
        self.current_level = 1
        self.max_level = 101
        self.completed_levels = set()
        self.shop = Shop()
        self.upgrade_system = UpgradeSystem()
        self.case_system = case.CaseSystem()
        

#====== Выбор героев ========
    def choose_class(self):
        while True:
            print("\n== выбор героя ==")
            print("1. убийца:   (крит. удар)")
            print("2. воин:     (защита)")
            print("3. стрелок:  (двойной удар)")
            print("4. монах:    (исцеление)")
            print("5. берсерк:  (ярость)")
            print("6. выйти:    (меню)")

            choice = input("выберите героя:-> ")

            if not choice.isdigit():
                print("ошибка ввода. попробуйте еще раз!")
                continue

            choice = int(choice)

            if choice == 1:
                self.hero = Assassin(self.player.name)
                break

            elif choice == 2:
                self.hero = Warrior(self.player.name)
                break

            elif choice == 3:
                self.hero = Archer(self.player.name)
                break

            elif choice == 4:
                self.hero = Monk(self.player.name)
                break

            elif choice == 5:
                self.hero = Berserk(self.player.name)
                break

            elif choice == 6:
                print("выйти")
                break
            else:
                print("ошибка ввода. попробуйте еще раз!")


#======= битва =========
    def battle(self, enemy):
        print(f" битва: {self.player.name} vs {enemy.name}")

        while self.hero.hp > 0 and enemy.hp > 0:
            input("Enter - атаковать:-> ")

            self.hero.attack(enemy)
            show_hp_bar(enemy)

            if enemy.hp <= 0:
                self.hero.gain_coins(enemy.gold_reward)
                self.hero.gain_exp(enemy.xp_reward)
                print("вы победили!")
                return True

            enemy.attack(self.hero)
            show_hp_bar(self.hero)

            if self.hero.hp <= 0:
                print("вы проиграли")
                return False
            

# ========= Первое меню, стартовое меню =========
    def start_menu(self):
        while True:
            print("\n== Старт меню ==")
            print("1. создать профиль")
            print("2. изменить профиль")
            print("3. выбрать героя")
            print("4. рассказы о героях")
            print("5. главное меню->> ")
            print("6. загрузить игру")
            print("7. сохранить игру")
            print("8. выйти из игры")
            

            choice = input("выберите действие:-> ")

            if not choice.isdigit():
                print("ошибка ввода. попробуйте еще раз!")
                continue

            choice = int(choice)

            if choice == 1:
                self.player.set_name()
                self.player.set_age()


            elif choice == 2:
                if not self.player.name:
                    print("сначала создайте профиль")
                else:
                    self.player.edit_profile()


            elif choice == 3:
                if not self.player.name:
                    print("ошибка. сначала создайте профиль")
                else:
                    self.choose_class()


            elif choice == 4:
                while True:
                    print("\n=== История героев ===")
                    print("1. история - Ассассина")
                    print("2. история - о воине")
                    print("3. история - о девочке стрелке")
                    print("4. история - о монашке")
                    print("5. история - берсерка")
                    print("6. выйти")

                    choice = input("выберите историю или (выйти):-> ")

                    if not choice.isdigit():
                        print("ошибка ввода. попробуйте еще раз!")
                        continue

                    choice = int(choice)

                    if choice == 1:
                        print("""
Ассассин вырос в гильдии теней, где детей учили не говорить лишнего
и не показывать эмоций. С юных лет он изучал яды, скрытность
и искусство молниеносного удара.
Он не ищет славы — его имя знают только те,
кто видел его последним.
Тьма — его союзник, а страх врага — его оружие.
""")
                        
                    elif choice == 2:
                        print("""
Воин прошёл сотни сражений и пережил больше битв,
чем многие могут представить.
Его тело покрыто шрамами — каждый из них
напоминает о тяжёлой победе.
Он стоит на передовой, защищая союзников
и не отступает даже перед смертью.
Честь и сила — его главный путь.
""")
                    
                    elif choice == 3:
                        print("""
С детства она тренировалась с луком,
мечтая доказать, что сила не зависит от размера.
Её стрелы летят быстрее ветра,
а глаз никогда не ошибается.
Она предпочитает держаться на расстоянии,
наблюдая за полем боя как хищная птица.
Спокойствие — её главное оружие.
""")
                        
                    elif choice == 4:
                        print("""
Монашка посвятила свою жизнь свету и знаниям.
Она обучалась в древнем ордене,
где исцеление и защита считались высшей силой.
Но если потребуется, она способна направить
силу света против своих врагов.
Её вера делает её сильнее любого оружия.
""")
                        
                    elif choice == 5:
                        print("""
Берсерк — воин ярости и разрушения.
В бою он теряет контроль,
и его сила возрастает с каждой раной.
Он не боится боли —
он питается ею.
Когда берсерк впадает в ярость,
враги начинают сожалеть,
что вообще вышли на поле боя.
""")
                        
                    elif choice == 6:
                        break
                    else:
                        print("ошибка ввода. попробуйте еще раз!")


            elif choice == 5:
                if self.hero is None:
                    print("сначала создайте героя")
                else:
                    self.main_menu()

            elif choice == 6:
                load_game(self)

            elif choice == 7:
                save_game(self)


            elif choice == 8:
                print("выход")
                break
            else:
                print("ошибка ввода. попробуйте еще раз!")


# ========= Второе меню, главное меню =========
    def main_menu(self):
        while True:
            print("\n== Главное меню ==")
            print("1. исследование - 101 уровень")
            print("2. Таверна / Инвентарь")
            
            print("3. ваш профиль ")
            print("4. назад - старт меню")
            
            choice = input("выберите действие:-> ")

            if not choice.isdigit():
                print("ошибка ввода. попробуйте еще раз!")
                continue

            choice = int(choice)

            if choice == 1:
                while True:
                    #======== Уровни ========
                    
                    print(f"макс. доступный уровень {self.current_level}")
                    print("доступные уровни:", end=" ")
                    for lvl in range(1, self.current_level + 1):
                        print(lvl, end=" ")
                    print("0. выйти")

                    level_choice = input("выберите уровень:-> ")

                    if not level_choice.isdigit():
                        print("ошибка ввода. попробуйте еще раз!")
                        continue

                    level_choice = int(level_choice)

                    if level_choice == 0:
                        print("выйти")
                        break

                    if 1 <= level_choice <= self.current_level:
                        enemy = create_enemy(level_choice)
                        self.hero.reset()
                        result = self.battle(enemy)

                        if result:

                            print(f" уровень {level_choice} пройден")
                            self.completed_levels.add(level_choice)

                            if level_choice == self.current_level and self.current_level < self.max_level:
                                self.current_level += 1
                                print(f" открыт новый уровень: {self.current_level}!")
                        

                    else:
                        print("уровень недоступен!")




            elif choice == 2:
                self.shop_menu()         


            

            #======= Профиль =======
            elif choice == 3:
                if self.hero is None:
                    print("сначала выберите героя")
                else:
                    print("\=== Ваш профиль ============")
                    print()
                    print(f"\n===  {self.hero.name}  ===")
                    print()
                    print("\n===========================")
                    print(f"герой: {self.hero}")
                    print(f"Уровень героя: {self.hero.level}")
                    print(f"Золото: {self.hero.coins}")
                    print(f"Ур. Исследования: {self.current_level}")
                    print("\=============================")
                    print("\n==== Характеристи ===")
                    print(f"урон: {self.hero.damage}")
                    print(f"жизнь: {self.hero.max_hp}")
                    print("\n==============================")


            
            elif choice == 4:
                print("назад")
                break
            else:
                print("ошибка ввода. попробуйте еще раз!")


#============ Магазин меню ==========
    def shop_menu(self):
        while True:
            print("\n== Таверна / Инвентарь ==")
            print("1. Таверна")
            print("2. прокачка героя")
            print("3. Сундуки")
            print("4. Инвентарь")
            print("5. назад")

            choice = input("выберите действие:-> ")

            if not choice.isdigit():
                print("ошибка ввода. попробуйте еще раз!")
                continue

            choice = int(choice)

            if choice == 1:
                self.shop.buy_item(self.hero)

            elif choice == 2:
                if self.hero is None:
                    print("у вас нет героя")
                else:
                    self.upgrade_system.upgrade_menu(self.hero)

            
            elif choice == 4:
                if self.hero is None:
                    print("сначала выберите героя:-> ")
                else:
                    self.case_system.open_case(self.hero)


            elif choice == 4:
                if not self.hero.inventory:
                    print("инвентарь пуст")
                else:
                    print(" ваш инвентарь: ")

                    for item in self.hero.inventory:
                        print(f"- {item.name}")


            elif choice == 5:
                print("назад")
                break
            else:
                print("ошибка ввода. попробуйте еще раз!")


game = Game()
game.start_menu()
