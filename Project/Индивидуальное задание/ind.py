#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Выполнить индивидуальное задание лабораторной работы 4.5, использовав классы данных,
а также загрузку и сохранение данных в формат XML.
Использовать словарь, содержащий следующие ключи: название пункта назначения рейса;
номер рейса; тип самолета. Написать программу, выполняющую следующие действия: ввод
с клавиатуры данных в список, состоящий из словарей заданной структуры; записи должны
быть размещены в алфавитном порядке по названиям пунктов назначения; вывод на экран
пунктов назначения и номеров рейсов, обслуживаемых самолетом, тип которого введен с
клавиатуры; если таких рейсов нет, выдать на дисплей соответствующее сообщение.
"""

from dataclasses import dataclass, field
import sys
from typing import List
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class Plane:
    destination: str
    num: int
    typ: str


@dataclass
class Staff:
    planes: List[Plane] = field(default_factory=lambda: [])

    def add(self, destination, num, typ):
        self.planes.append(
            Plane(
                destination=destination,
                num=num,
                typ=typ
            )
        )

        self.planes.sort(key=lambda plane: plane.destination)

    def __str__(self):
        # Заголовок таблицы.
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолета"
            )
        )
        table.append(line)

        # Вывести данные о всех самолетах.
        for idx, plane in enumerate(self.planes, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    plane.destination,
                    plane.num,
                    plane.typ
                )
            )

        table.append(line)

        return '\n'.join(table)

    def select(self, jet):
        # Получить текущую дату.
        result = []
        for plane in self.planes:
            if plane.typ.lower() == str(jet):
                result.append(plane)

        return result

    def load(self, filename):
        with open(filename, 'r', encoding='utf8') as fin:
            xml = fin.read()

        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)

        self.planes = []
        for plane_element in tree:
            destination, num, typ = None, None, None

            for element in plane_element:
                if element.tag == 'destination':
                    destination = element.text
                elif element.tag == 'num':
                    num = int(element.text)
                elif element.tag == 'typ':
                    typ = element.text

                if destination is not None and num is not None \
                        and typ is not None:
                    self.planes.append(
                        Plane(
                            destination=destination,
                            num=num,
                            typ=typ
                        )
                    )

    def save(self, filename):
        root = ET.Element('planes')
        for plane in self.planes:
            plane_element = ET.Element('plane')

            destination_element = ET.SubElement(plane_element, 'destination')
            destination_element.text = plane.destination

            num_element = ET.SubElement(plane_element, 'num')
            num_element.text = str(plane.num)

            typ_element = ET.SubElement(plane_element, 'typ')
            typ_element.text = plane.typ

            root.append(plane_element)

        tree = ET.ElementTree(root)
        with open(filename, 'wb') as fout:
            tree.write(fout, encoding='utf8', xml_declaration=True)


if __name__ == '__main__':
    # Список работников.
    staff = Staff()

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о самолёте.
            destination = input("Пункт назначения:  ")
            num = int(input("Номер рейса: "))
            typ = input("Тип самолёта: ")

            # Добавить самолёт.
            staff.add(destination, num, typ)

        elif command == 'list':
            # Вывести список.
            print(staff)

        elif command.startswith('select '):
            # Разбить команду на части для выделения типа самолёта.
            parts = command.split(maxsplit=1)
            # Запросить самолёты.
            selected = staff.select(parts[1])

            # Вывести результаты запроса.
            if selected:
                for idx, plane in enumerate(selected, 1):
                    print(
                        '{:>4}: {} - №{}'.format(idx, plane.destination, plane.num)
                    )

            else:
                print("Самолёты заданного типа не найдены.")

        elif command.startswith('load '):
            # Разбить команду на части для имени файла.
            parts = command.split(maxsplit=1)
            # Загрузить данные из файла.
            staff.load(parts[1])

        elif command.startswith('save '):
            # Разбить команду на части для имени файла.
            parts = command.split(maxsplit=1)
            # Сохранить данные в файл.
            staff.save(parts[1])

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить самолёт;")
            print("list - вывести список самолётов;")
            print("select <тип> - запросить самолёты нужного типа;")
            print("load <имя_файла> - загрузить данные из файла;")
            print("save <имя_файла> - сохранить данные в файл;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)
