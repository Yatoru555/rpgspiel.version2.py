


# shop.py
class Item:
    def __init__(self, name, price, hp_bonus=0, damage_bonus=0):
        self.name = name
        self.price = price
        self.hp_bonus = hp_bonus
        self.damage_bonus = damage_bonus


class Shop:
    def __init__(self):
        self.items = [
            Item("⚔️Меч ржавый             ⭐☆☆☆☆", 500, damage_bonus=15),
            Item("⚔️Меч воина              ⭐⭐☆☆☆", 3000, damage_bonus=50),
            Item("⚔️Меч самурая            ⭐⭐⭐☆☆", 10000, damage_bonus=150),
            Item("⚔️Меч демона             ⭐⭐⭐⭐☆", 50000, damage_bonus=400),
            Item("⚔️Меч владыки            ⭐⭐⭐⭐⭐", 200000, damage_bonus=800),
            Item("🛡️Броня разбитая          ⭐☆☆☆☆", 350, hp_bonus=70),
            Item("🛡️Броня рыцаря            ⭐⭐☆☆☆", 2500, hp_bonus=175),
            Item("🛡️Броня Полководца        ⭐⭐⭐☆☆", 10000, hp_bonus=400),
            Item("🛡️Броня архидемона        ⭐⭐⭐⭐☆", 50000, hp_bonus=1200),
            Item("🛡️Броня Владыки           ⭐⭐⭐⭐⭐", 125000, hp_bonus=3000),
            Item("👢Сапоги крестианина      ⭐☆☆☆☆", 200, hp_bonus=40),
            Item("👢Сапоги Рыцаря           ⭐⭐☆☆☆", 800, hp_bonus=90),
            Item("👢Сапоги Полководца       ⭐⭐⭐☆☆", 4000, hp_bonus=500),
            Item("👢Сапоги архидемона       ⭐⭐⭐⭐☆", 10000, hp_bonus=1200),
            Item("👢Сапоги владыки          ⭐⭐⭐⭐⭐", 25000, hp_bonus=2500),
            Item("💍Ожирелье раба            ⭐☆☆☆☆", 2000, hp_bonus=200),
            Item("💍Кольцо дворянина         ⭐⭐☆☆☆", 7000, hp_bonus=700),
            Item("💍Кольцо полководца        ⭐⭐⭐☆☆", 12000, damage_bonus=100, hp_bonus=1200),
            Item("💍Кольцо силы демона       ⭐⭐⭐⭐☆", 25000, hp_bonus=2000),
            Item("💍Кольцо владыки теней     ⭐⭐⭐⭐⭐", 60000, damage_bonus=250, hp_bonus=5000),
            Item("🐾Питомец Дворняшка        ⭐☆☆☆☆", 1000, damage_bonus=50, hp_bonus=100),
            Item("🐾Питомец Гиена            ⭐⭐☆☆☆", 4000, damage_bonus=125, hp_bonus=350),
            Item("🐾Питомец Волк             ⭐⭐⭐☆☆", 15000, damage_bonus=250, hp_bonus=500),
            Item("🐾Питомец 3-х головая змея ⭐⭐⭐⭐☆", 30000, hp_bonus=1000),
            Item("🐉питомец Дракон           ⭐⭐⭐⭐⭐", 80000, damage_bonus=300, hp_bonus=1500),
        ]


    def show_items(self):
        print("\n== Магазин ==")

        for idx, item in enumerate(self.items, start=1):
            bonuses = []

            if item.hp_bonus:
                bonuses.append(f"+{item.hp_bonus} HP")
            if item.damage_bonus:
                bonuses.append(f"+{item.damage_bonus} Урон")

            print(f"{idx}. {item.name} ({', '.join(bonuses)}) - {item.price} золота")
        print("0. Выйти")


    def buy_item(self, hero):
        while True:
            self.show_items()

            choice = input("Выберите предмет для покупки:-> ")

            if not choice.isdigit():
                print("Ошибка ввода!")
                continue

            choice = int(choice)

            if choice == 0:
                break
            
            if 1 <= choice <= len(self.items):
                item = self.items[choice - 1]
                if hero.coins >= item.price:
                    hero.coins -= item.price
                    hero.max_hp += item.hp_bonus
                    hero.hp += item.hp_bonus
                    hero.damage += item.damage_bonus
                    hero.inventory.append(item)
                    print(f"Вы купили {item.name}!")
                else:
                    print("Недостаточно золота!")
            else:
                print("Такого предмета нет.")