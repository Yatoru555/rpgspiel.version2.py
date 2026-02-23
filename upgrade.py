

class UpgradeSystem:
    def __init__(self):
        self.base_hp_cost = 50
        self.base_damage_cost = 75


    def upgrade_menu(self, hero):
        while True:

            hp_price= self.base_hp_cost + (hero.level * 10)
            dmg_price = self.base_damage_cost + (self.level * 15)


            print("\n== прокачка героя ==")
            print(f"золото: {hero.coins}")
            print(f"1. +10 HP ({hp_price} золота)")
            print(f"2. +5 урона ({dmg_price} золота)")
            print("3. выйти")

            choice = input("выберите действие:-> ")

            if not choice.isdigit():
                print("ошибка ввода. попробуйте еще раз!")
                continue

            choice = int(choice)

            if choice == 1:
                if hero.coins >= hp_price:
                    hero.coins -= hp_price
                    hero.max_hp += 10
                    hero.hp += 10
                    print("успешно. HP увеличен")
                else:
                    print("Недостаточно золота")

            elif choice == 2:

                if hero.coins >= dmg_price:
                    hero.coins -= dmg_price
                    self.damage += 5
                    print("успешно. урон +5")
                else:
                    print("недостаточно золота")


            elif choice == 3:
                print("назад")
                break
            else:
                print("ошибка ввода. попробуйте еще раз!") 