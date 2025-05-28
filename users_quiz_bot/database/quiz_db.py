import psycopg2

from os import getenv
from dotenv import load_dotenv

load_dotenv()

class PostgresSQL:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            host=getenv("DB_HOST"),
            port=getenv("DB_PORT")
        )
        self.curr = self.conn.cursor()

    def execute(self, query, values):
        with self.conn:
            self.curr.execute(query, values)
        return self.curr

    def create_category(self, name: str):
        self.execute("""INSERT INTO category(name) VALUES (%s); """, (name,))

    def create_subcategory(self, category_id: int, name: str):
        self.execute(""" 
                INSERT INTO subcategory(category_id, name) VALUES (%s, %s); """, (category_id, name))

    def create_quiz(self, subcategory_id: int, question: str):
        self.execute(""" 
                INSERT INTO quiz(subcategory_id, question) VALUES (%s, %s); """, (subcategory_id, question))

    def create_options(self, quiz_id: int, text: str, is_correct: bool):
        self.execute(""" 
                   INSERT INTO "option"(quiz_id, text, is_correct) VALUES (%s, %s, %s); """,
                     (quiz_id, text, is_correct))

    def create_users(self, fullname: str, age: int):
        self.execute(""" 
                   INSERT INTO users(fullname, age) VALUES (%s, %s); """, (fullname, age))

    def create_user_answers(self, user_id, quiz_id, option_id):
        self.execute("""INSERT INTO user_answers(user_id, quiz_id, option_id) VALUES (%s, %s, %s)""",
                     (user_id, quiz_id, option_id))

    def get_category(self):
        self.curr.execute("""SELECT name, id FROM category""")
        return self.curr.fetchall()

    def get_subcategory(self, cat_id):
        self.curr.execute(f"""SELECT name, id FROM subcategory WHERE category_id={cat_id}""")
        return self.curr.fetchall()

    def get_quiz(self, sub_id):
        self.curr.execute(f"""SELECT question, id FROM quiz WHERE subcategory_id={sub_id}""")
        return self.curr.fetchall()

    def get_question_text(self, quiz_id):
        self.curr.execute(f"""SELECT question from quiz WHERE id={quiz_id};""")
        result = self.curr.fetchone()
        return result[0] if result else None

    def get_option(self, quiz_id, option_id=None):
        if option_id:
            self.curr.execute(f"""SELECT text, is_correct FROM "option" WHERE quiz_id={quiz_id} and id={option_id}""")
            return self.curr.fetchone()
        else:
            self.curr.execute(f"""SELECT text, id FROM "option" WHERE quiz_id={quiz_id}""")
            return self.curr.fetchall()

    def register(self, chat_id, fullname):
        self.curr.execute(f"""INSERT INTO users (chat_id, full_name) VALUES (%s, %s)""", (chat_id, fullname))
        self.conn.commit()

    def find_id_by_chat_id(self, chat_id):
        self.curr.execute("SELECT id FROM users WHERE chat_id=%s", (chat_id,))
        data = self.curr.fetchone()
        return data[0] if data else None

    def save_answer(self, user_id, quiz_id, option_id):
        self.curr.execute("INSERT INTO user_answers (user_id, quiz_id, option_id) VALUES (%s, %s, %s)",(user_id, quiz_id, option_id))
        self.conn.commit()
# categories = ["Fanlar", "Texnologiyalar", "Sport turlari", "San’at"]
#
# for name in categories:
#     db.create_category(name)


# subcategories = {
#     1: ["Matematika", "Fizika", "Kimyo", "Biologiya"],
#     2: ["Rassomchilik", "Musiqa", "Haykaltaroshlik", "Teatr"],
#     3: ["Futbol", "Basketbol", "Tennis", "Suzish"],
#     4: ["Kompyuter", "Mobil ilovalar", "Sun’iy intellekt", "Internet texnologiyalari"]
# }
#
# for category_id, subcat_list in subcategories.items():
#     for subcat in subcat_list:
#         db.create_subcategory(category_id, subcat)

# quizzes = {
#     1: [
#         "1 + 1 nechiga teng?",
#         "5 * 2 nechiga teng?",
#         "10 / 2 nechiga teng?",
#         "3^2 nechiga teng?",
#         "9 - 4 nechiga teng?"
#     ],
#     2: [
#         "Yorug‘lik tezligi qancha?",
#         "Og‘irlik kuchi qanday o‘lchanadi?",
#         "Ohm qonuni nima?",
#         "Tezlanma formulasi qanday?",
#         "Energiyaning o‘lchov birligi nima?"
#     ],
#     3: [
#         "H2O bu nima?",
#         "Oltinning kimyoviy belgisi nima?",
#         "CO2 nimani bildiradi?",
#         "NaCl bu nima?",
#         "Kimyo fani nimani o‘rganadi?"
#     ],
#     4: [
#         "DNK nima?",
#         "Odamda nechta suyak bor?",
#         "Qaysi organ nafas olishga javobgar?",
#         "Qon aylanish tizimini kim kashf etgan?",
#         "Yurak nechta bo‘limdan iborat?"
#     ],
#     5: [
#         "Eng mashhur rassom kim?",
#         "Ranglarning asosiy turlari nima?",
#         "Portret nima?",
#         "Akvarel nima?",
#         "Mozaika nima?"
#     ],
#     6: [
#         "Nota nima?",
#         "Eng katta cholg‘u asbobi qaysi?",
#         "Simfonik orkestrda qancha cholg‘u bo‘ladi?",
#         "Do re mi fa so la si nima?",
#         "Kim musiqa yozadi?"
#     ],
#     7: [
#         "Haykal nima?",
#         "Haykal yasash uchun nima kerak?",
#         "Eng mashhur haykal qaysi?",
#         "Bronza bu nima?",
#         "Skulptor kim?"
#     ],
#     8: [
#         "Teatr nima?",
#         "Aktyor nima qiladi?",
#         "Scena nima?",
#         "Dramaturg kim?",
#         "Rejissor nima qiladi?"
#     ],
#     9: [
#         "Futbolda necha o‘yinchi bo‘ladi?",
#         "To‘p necha daqiqa o‘ynaladi?",
#         "Offside nima?",
#         "VAR nima?",
#         "Messi qaysi jamoada o‘ynaydi?"
#     ],
#     10: [
#         "Basketbolda necha ochko beriladi?",
#         "NBA nima?",
#         "Basketbol maydoni qanchalik katta?",
#         "To‘p qanday o‘ynaladi?",
#         "LeBron James kim?"
#     ],
#     11: [
#         "Tennisda necha set bo‘ladi?",
#         "Raketa nima?",
#         "Wimbledon nima?",
#         "Servis nima?",
#         "Kim eng kuchli tennischi?"
#     ],
#     12: [
#         "Suzishning turlari nima?",
#         "Olimpiya havzasi uzunligi qancha?",
#         "Suzuvchi qanday nafas oladi?",
#         "Kraul nima?",
#         "Michael Phelps kim?"
#     ],
#     13: [
#         "Kompyuter nima?",
#         "CPU nima?",
#         "RAM nima qiladi?",
#         "SSD va HDD farqi nima?",
#         "Operatsion tizim nima?"
#     ],
#     14: [
#         "Mobil ilova nima?",
#         "Android nima?",
#         "iOS nima?",
#         "Play Market nima?",
#         "Mobil ilova qanday yoziladi?"
#     ],
#     15: [
#         "Sun’iy intellekt nima?",
#         "AI qayerda ishlatiladi?",
#         "ChatGPT nima?",
#         "Mashina o‘rganishi nima?",
#         "AI xavflimi?"
#     ],
#     16: [
#         "Internet nima?",
#         "IP manzil nima?",
#         "Web brauzer nima?",
#         "HTTP nima?",
#         "Veb-sayt qanday ishlaydi?"
#     ]
# }
#
# for subcategory_id, questions in quizzes.items():
#     for question in questions:
#         db.create_quiz(subcategory_id, question)

# options_by_id = {
#     1: [("2", True), ("1", False), ("3", False), ("0", False)],
#     2: [("10", True), ("7", False), ("12", False), ("5", False)],
#     3: [("5", True), ("2", False), ("10", False), ("1", False)],
#     4: [("9", True), ("6", False), ("3", False), ("12", False)],
#     5: [("5", True), ("6", False), ("3", False), ("4", False)],
#     6: [("300 000 km/s", True), ("150 000 km/s", False), ("100 000 km/s", False), ("1 000 km/s", False)],
#     7: [("Nyuton", True), ("Kilogramm", False), ("Joul", False), ("Metr", False)],
#     8: [("U = IR", True), ("F = ma", False), ("E = mc^2", False), ("V = IR^2", False)],
#     9: [("a = Δv / t", True), ("s = vt", False), ("F = ma", False), ("v = a / t", False)],
#     10: [("Joul", True), ("Vat", False), ("Nyuton", False), ("Kelvin", False)],
#     11: [("Suv", True), ("Havo", False), ("Gaz", False), ("Zarralar", False)],
#     12: [("Au", True), ("Ag", False), ("O", False), ("G", False)],
#     13: [("Uglerod(IV) oksid", True), ("Suv", False), ("Azot", False), ("Oksid", False)],
#     14: [("Tuz", True), ("Soda", False), ("Kislota", False), ("Suv", False)],
#     15: [("Moddalar tuzilishi va xossalarini", True), ("Hayvonlar", False), ("Raqamlar", False), ("Yulduzlar", False)],
#     16: [("Dezoksiribonuklein kislota", True), ("Protein", False), ("Lipid", False), ("Karbonhidrat", False)],
#     17: [("206", True), ("205", False), ("201", False), ("208", False)],
#     18: [("O‘pka", True), ("Jigar", False), ("Yurak", False), ("Buyrak", False)],
#     19: [("Uilyam Garvey", True), ("Isaak Nyuton", False), ("Albert Eynshtein", False), ("Nikola Tesla", False)],
#     20: [("4", True), ("3", False), ("2", False), ("5", False)],
#     21: [("Leonardo da Vinci", True), ("Pablo Picasso", False), ("Vincent van Gogh", False), ("Claude Monet", False)],
#     22: [("Qizil, Yashil, Ko‘k", True), ("Qora, Oq, Kulrang", False), ("Sariq, Qora, Oq", False), ("To‘q yashil, och ko‘k, qizil", False)],
#     23: [("Shaxsiy portret", True), ("Tabiat manzarasi", False), ("Hayvon rasmi", False), ("Abstrakt rassomlik", False)],
#     24: [("Suv bilan aralashtirilgan bo‘yoq", True), ("Yog‘li bo‘yoq", False), ("Karbongrafit", False), ("Akril bo‘yoq", False)],
#     25: [("Kichik mozaika elementlari bilan ishlangan san’at", True), ("Yirik yog‘li rasm", False), ("Qog‘oz rassomligi", False), ("Kaktus rasmi", False)],
#     26: [("Musiqiy yozuv belgisi", True), ("O‘yinchoq", False), ("Kitob sahifasi", False), ("Rasm", False)],
#     27: [("Piano", True), ("Gitara", False), ("Skripka", False), ("Fleyta", False)],
#     28: [("Qariyb 70 ta cholg‘u", True), ("30 ta", False), ("100 ta", False), ("50 ta", False)],
#     29: [("Musiqiy tovushlar nomi", True), ("Raqamlar", False), ("Hayvon nomlari", False), ("Yulduzlar nomi", False)],
#     30: [("Kompozitor", True), ("Rassom", False), ("Shifokor", False), ("O‘qituvchi", False)],
#     31: [("San’at asari sifatida haykal", True), ("Mitoxondriya", False), ("Ribosoma", False), ("Golji apparati", False)],
#     32: [("Materiallar va ijod", True), ("Fermentatsiya", False), ("Nafas olish", False), ("Chirishi", False)],
#     33: [("Davud haykali", True), ("RNK", False), ("ATP", False), ("Enzim", False)],
#     34: [("Metall qotishmasi", True), ("Vakuola", False), ("Yadro", False), ("Lizosoma", False)],
#     35: [("Haykal yasovchi rassom", True), ("Organizm", False), ("Hujayra", False), ("Organ", False)],
#     36: [("Spektakl ko‘rsatish joyi", True), ("Yog‘", False), ("Suv", False), ("Vitamin", False)],
#     37: [("Rol ijro etadi", True), ("Teri", False), ("Qon", False), ("Asab", False)],
#     38: [("Teatrdagi sahna", True), ("Aorta", False), ("Venalar", False), ("Arteriyalar", False)],
#     39: [("Pyesa muallifi", True), ("Nafas tizimi", False), ("Ovqat hazm qilish tizimi", False), ("Qon aylanish tizimi", False)],
#     40: [("Spektaklni boshqaradi", True), ("Yurak", False), ("Jigar", False), ("O‘pka", False)],
#     41: [("11", True), ("2", False), ("4", False), ("5", False)],
#     42: [("90 daqiqa", True), ("Yog‘", False), ("Metall", False), ("Shisha", False)],
#     43: [("O‘yindagi qoida buzilishi", True), ("Kimyoviy reaksiya", False), ("Nur yutilishi", False), ("Suv aylanishi", False)],
#     44: [("Video hakam tizimi", True), ("Yig‘ilish", False), ("Parlanish", False), ("Qaynash", False)],
#     45: [("Inter Miami", True), ("0°C", False), ("25°C", False), ("50°C", False)],
#     46: [("2 yoki 3 ochko", True), ("Yashil", False), ("Ko‘k", False), ("Oq", False)],
#     47: [("Basketbol ligasi", True), ("Elektron", False), ("Neutron", False), ("Kvark", False)],
#     48: [("28x15 metr", True), ("Proton", False), ("Kvark", False), ("Atom", False)],
#     49: [("Qo‘l va oyoq bilan", True), ("Molekula", False), ("Yadro", False), ("Proton", False)],
#     50: [("Basketbolchi", True), ("Biologiya", False), ("Matematika", False), ("Geografiya", False)],
#     51: [("3 yoki 5", True), ("Nur", False), ("Tovush", False), ("Sovuq", False)],
#     52: [("Tennisda to‘p urish asbobi", True), ("Kislorod", False), ("Uglerod", False), ("Azot", False)],
#     53: [("Tennis turniri", True), ("Kislorod", False), ("Vodorod", False), ("Azot", False)],
#     54: [("O‘yinni boshlash usuli", True), ("Neytral", False), ("Yarim metall", False), ("Gaz", False)],
#     55: [("Novak Djokovic", True), ("Atom", False), ("Molekula", False), ("Proton", False)],
#     56: [("Kraul, brass, batterflyay", True), ("Suyuqliklar", False), ("Gazlar", False), ("Yog‘lar", False)],
#     57: [("50 metr", True), ("Kovalent bog‘lanish", False), ("Metall bog‘lanish", False), ("Vodorod bog‘lanishi", False)],
#     58: [("Burun orqali", True), ("Temperatura", False), ("Bosim", False), ("Sifat", False)],
#     59: [("Suzish uslubi", True), ("Qattiq", False), ("Gaz", False), ("Plazma", False)],
#     60: [("Olimpiya chempioni suzuvchi", True), ("Kislorod", False), ("Azot", False), ("Metan", False)],
#     61: [("Hisoblash qurilmasi", True), ("Oy", False), ("Mars", False), ("Quyosh", False)],
#     62: [("Markaziy protsessor", True), ("Quyosh", False), ("Yupiter", False), ("Saturn", False)],
#     63: [("Tezkor xotira", True), ("Mars", False), ("Yer", False), ("Merkuriy", False)],
#     64: [("Tezlik va sig‘im farqi", True), ("Venera", False), ("Neptun", False), ("Saturn", False)],
#     65: [("Dasturiy ta’minot", True), ("Oy", False), ("Yulduz", False), ("Meteor", False)],
#     66: [("Telefon dasturi", True), ("Litosfera", False), ("Gidrosfera", False), ("Ionosfera", False)],
#     67: [("Operatsion tizim", True), ("Magnit", False), ("Issiqlik", False), ("Yorug‘lik", False)],
#     68: [("Apple operatsion tizimi", True), ("360 kun", False), ("400 kun", False), ("300 kun", False)],
#     69: [("Ilovalar do‘koni", True), ("12 soat", False), ("48 soat", False), ("72 soat", False)],
#     70: [("Dasturlash tillari bilan", True), ("Kometa", False), ("Planet", False), ("Yulduz", False)],
#     71: [("Aqlli mashina", True), ("Sovuq siqilishi", False), ("Qayt qilish", False), ("Bug‘lanish", False)],
#     72: [("Turli sohalarda", True), ("Oksidlanish", False), ("Erish", False), ("Qaynatish", False)],
#     73: [("Sun’iy intellekt chatboti", True), ("Asab to‘qimasi", False), ("Muskul to‘qima", False), ("Epiteliya", False)],
#     74: [("Ma’lumotlardan o‘rganish", True), ("Azot", False), ("Uglerod", False), ("Vodorod", False)],
#     75: [("Nazorat ostida xavfsiz", True), ("Atmosfera", False), ("Litosfera", False), ("Biosfera", False)],
#     76: [("Global tarmoq", True), ("O‘simlik o‘sishi", False), ("Fotosintez", False), ("Erish", False)],
#     77: [("Qurilma identifikatori", True), ("O‘tin", False), ("Gaz", False), ("Quruq barglar", False)],
#     78: [("Internetga kirish dasturi", True), ("Yorug‘lik chiqarish", False), ("Issiqlik tarqatish", False), ("Suvni bug‘latish", False)],
#     79: [("Veb protokoli", True), ("Fizika", False), ("Kimyo", False), ("Geometriya", False)],
#     80: [("Server va brauzer orqali", True), ("Yong‘in", False), ("Plastik", False), ("Ko‘mir", False)]
# }
#
# for quiz_id, options in options_by_id.items():
#     for text, is_correct in options:
#         db.create_options(quiz_id, text, is_correct)

# print(db.fetchall())

if __name__ == "__main__":
    db = PostgresSQL()

