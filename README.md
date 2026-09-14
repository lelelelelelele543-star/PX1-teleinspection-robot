# PX-1 Teleinspection Robot

## Текущий комплект

Единственный действующий master и документация: [current/](current/README.md).

Механический эталон — Proteus CRP-150. Электроника собственная, на готовых модулях. Текущий статус: **HOLD — рабочая конструкция к изготовлению не выпущена**. Успех CAD-экспорта не означает PASS механики.

- [Общий STEP](current/CAD/PX1_Current_Master.step)
- [Текущая BOM](current/PX1_Current_BOM.csv)
- [Validation](current/PX1_Current_Validation.json)
- [Чертежи и CAD-виды](current/PX1_Drawings_Current.pdf)
- [PDF-документация](current/PX1_Documentation_Current.pdf)
- [Электрические соединения и распиновки](current/ELECTRICAL_Current.md)
- [Сборка, герметизация и испытания](current/ASSEMBLY_AND_TESTS_Current.md)
- [Источники размеров](current/SOURCE_REGISTER.md)
- [Журнал изменений](current/PX1_Change_Log.md)

Шесть колёс; станции X50/X150/X250; десять Z50; два двигателя; Z16→Z40→задняя ось→Z50. Ручной лифт, отдельная герметичная камера, съёмный PRESSURE/LIFT. Оба кабеля ровно шестижильные; основной tether без коаксиала. Своей PCB, кассет и внешних шарниров открытия корпуса нет.

Предыдущие Rev и WB сохранены как история. Их пометки active/PASS не имеют приоритета над current. Перед любым изготовлением сверять HOLD и исходный SHA в validation.
