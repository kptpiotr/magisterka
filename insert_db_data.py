"""
Insert some example data to the database
"""

import db
import utils
import datetime

if __name__ == "__main__":
    created_at, created_by_id = utils.get_info()
    # db.insert_user(created_at, created_by_id, "Piotr", "Bańko", "piotrbanko@test.com", "piotrbanko",
    #                "$2b$12$WuANhvok3KabiOdC538pA.NsaCA5EeJIcIt7cdeyddC0J.b3q4Yq6", "Administrator")
    # db.insert_user(created_at, created_by_id, "Zygmunt", "Szczeciński", "zygszczec@test.com", "zygmuntszczecinski",
    #                "$2b$12$WuANhvok3KabiOdC538pA.NsaCA5EeJIcIt7cdeyddC0J.b3q4Yq6", "Dyrektor")
    #
    # db.insert_trade_order(created_at, created_by_id, "Oczekujące", "Dwójniki", 312, "Zlecenie zewnętrzne", "Polmex SA", "Może być nierdzewka",
    #                    5, 5, datetime.datetime(2023, 11, 17), "Potwierdzić za 2 dni", "11000", "25000")
    # db.insert_trade_order(created_at, created_by_id, "Zakończone", "Uchwyty czołowe", 302, "Zlecenie zewnętrzne", "Polmex SA", "A35",
    #                    12, 12, datetime.datetime(2023, 8, 11), "", "6000", "9000")
    # db.insert_trade_order(created_at, created_by_id, "Zakończone", "ETK-341", 308, "Zlecenie zewnętrzne", "Stalotron", "A35",
    #                    3, 3, datetime.datetime(2023, 3, 19), "", "6500", "8000")
    #
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 1, 1), "Nowy Rok")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 1, 2), "URLOP 1")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 4, 10), "Poniedziałek Wielkanocny")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 5, 1), "Święto Konstytucji 3 Maja")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 5, 3), "Święto Pracy")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 1, 6), "Trzech Króli")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 6, 8), "Boże Ciało")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 8, 15), "Święto WP")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 11, 1), "Wszystkich Świętych")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 11, 11), " Święto Niepodległości")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 12, 25), "Boże Narodzenie")
    # db.insert_holiday(created_at, created_by_id, datetime.datetime(2023, 12, 26), "Boże Narodzenie 2")
    #
    # db.insert_material_action(created_at, created_by_id, 'Przyjęcie z zamówienia zbiorczego #011/2023', 0, 'przyjecie',
    #                           'TI-6AL-4V-3.5"x4.5"x30.00"-AMS4928', 25, datetime.datetime(2023, 4, 11), "")
    # db.insert_material_action(created_at, created_by_id, 'Wydanie pod zamówienie 251/2023 I', 1, 'wydanie',
    #                           'TI-6AL-4V-3.5"x4.5"x30.00"-AMS4928', -3, datetime.datetime(2023, 4, 11), "")
    # db.insert_material_action(created_at, created_by_id, 'Wydanie pod zamówienie 221/2023 I', 2, 'wydanie',
    #                           'TI-6AL-4V-3.5"x4.5"x30.00"-AMS4928', -5, datetime.datetime(2023, 5, 21), "")
    # db.insert_material_action(created_at, created_by_id, 'Wydanie pod zamówienie 231/2023 I', 1, 'wydanie',
    #                           'TI-6AL-4V-3.5"x4.5"x30.00"-AMS4928', -6, datetime.datetime(2023, 6, 17), "")
    # db.insert_material_action(created_at, created_by_id, 'Wydanie pod zamówienie 228/2023 I', 2, 'wydanie',
    #                           'TI-6AL-4V-3.5"x4.5"x30.00"-AMS4928', -2, datetime.datetime(2023, 7, 1), "")
    # db.insert_material_action(created_at, created_by_id, 'Przyjęcie z zamówienia zbiorczego #012/2023', 0, 'przyjecie',
    #                           'TI-6AL-4V-3.5"x4.5"x30.00"-AMS4928', 15, datetime.datetime(2023, 7, 11), "")
    # db.insert_material_action(created_at, created_by_id, 'Wydanie pod zamówienie 281/2023 I', 1, 'wydanie',
    #                           'TI-6AL-4V-3.5"x4.5"x30.00"-AMS4928', -3, datetime.datetime(2023, 8, 11), "")
    #
    # db.insert_material_action(created_at, created_by_id, 'Przyjęcie z zamówienia zbiorczego #011/2023', 0, 'przyjecie',
    #                           'TI-6AL-4V-5"x4.5"x30.00"-AMS4928', 11, datetime.datetime(2023, 4, 11), "")
    # db.insert_material_action(created_at, created_by_id, 'Przyjęcie z zamówienia zbiorczego #011/2023', 0, 'przyjecie',
    #                           'TI-6AL-4V-5"x6"x30.00"-AMS4928', 11, datetime.datetime(2023, 4, 11), "")
    #
    #
    # db.insert_tool(created_at, created_by_id, "Frez kątowy", "DIN1833-B60X20-HSS", "60ST-X-20")
    # db.insert_tool(created_at, created_by_id, "Frez palcowy", "WL400060340", "6Lr15Lc58.4Z4")
    # db.insert_tool(created_at, created_by_id, "Głowica frezarska X3", "220.299.032", "44R6-FR-SKLAD-3GNIAZDA")
    # db.insert_tool(created_at, created_by_id, "Frez węglikowy do stali", "BR011650P", "16R0Lr50Lc100Z4")
    # db.insert_tool(created_at, created_by_id, "Frez kulowy", "DORMER-S511-8.00-MZ", "8R4Lr19Lo72Lc102")
    # db.insert_tool(created_at, created_by_id, "Fazownik VHM", "208105.12_MZ", "12x90Dc12Z4")
    #
    # db.insert_machine(created_at, created_by_id, "MAZAK HCN 10800", "Frezarka", 175)
    # db.insert_machine(created_at, created_by_id, "MAZAK VARIAXIS I-1050T", "Tokarko-frezarka", 155)
    # db.insert_machine(created_at, created_by_id, "MAZAK J-600/5X", "Frezarka", 150)
    # db.insert_machine(created_at, created_by_id, "MAZAK INTEGREX I-400ST", "Tokarko-frezarka", 130)
    # db.insert_machine(created_at, created_by_id, "HAAS VF-5/40", "Frezarka", 110)
    # db.insert_machine(created_at, created_by_id, "HAAS VF-5/40", "Frezarka", 110)
    # db.insert_machine(created_at, created_by_id, "HAAS VF-5/40", "Frezarka", 110)
    # db.insert_machine(created_at, created_by_id, "HAAS VF-2DHE", "Frezarka", 100)
    # db.insert_machine(created_at, created_by_id, "HAAS VF-2DHE", "Frezarka", 100)
    # db.insert_machine(created_at, created_by_id, "FADAL VMC 3016", "Frezarka", 90)
    # db.insert_machine(created_at, created_by_id, "HAAS ST-30", "Tokarka", 80)
    # db.insert_machine(created_at, created_by_id, "HAAS ST-30", "Tokarka", 80)
    # db.insert_machine(created_at, created_by_id, "DOOSAN LYNX 220LM", "Tokarka", 100)
    # db.insert_machine(created_at, created_by_id, "MAZAK QT-250MY", "Tokarka", 130)
    # db.insert_machine(created_at, created_by_id, "SHEFFIELD DISCOVERY D12-II", "Maszyna pomiarowa", 50)
    #
    # db.insert_employee(created_at, created_by_id, "Adam", "Guc", 55, "Ślusarz")
    # db.insert_employee(created_at, created_by_id, "Piotr", "Kaznodziej", 55, "Ślusarz")
    # db.insert_employee(created_at, created_by_id, "Michał", "Gurbacz", 55, "Ślusarz")
    # db.insert_employee(created_at, created_by_id, "Michał", "Karamowicz", 65, "Operator CNC")
    # db.insert_employee(created_at, created_by_id, "Paweł", "Baran", 65, "Operator CNC")
    # db.insert_employee(created_at, created_by_id, "Maciej", "Kołacz", 65, "Operator CNC")
    # db.insert_employee(created_at, created_by_id, "Zbigniew", "Gurbisz", 65, "Operator CNC")
    # db.insert_employee(created_at, created_by_id, "Stanisław", "Polak", 65, "Operator CNC")
    # db.insert_employee(created_at, created_by_id, "Piotr", "Torman", 90, "Programista CNC")
    # db.insert_employee(created_at, created_by_id, "Łukasz", "Krupa", 100, "Programista CNC")
    # db.insert_employee(created_at, created_by_id, "Stanisław", "Neumann", 85, "Specjalista ds. jakości")
    #
    # db.insert_production_order(created_at, created_by_id, "Dwójniki POLMEX SA", 1, 1, 5, datetime.datetime(2023, 7, 17), datetime.datetime(2023, 11, 14), 60, 'TI-6AL-4V-3.5"x4.5"x30.00"-AMS4928', "W trakcie", "")
    # db.insert_production_order(created_at, created_by_id, "Uchwyty czołowe POLMEX SA", 2, 1, 5, datetime.datetime(2023, 6, 17), datetime.datetime(2023, 8, 11), 100, 'TI-6AL-4V-3.5"x4.5"x30.00"-AMS4928', "Zakończone", "")



