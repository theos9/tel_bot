from pyrogram import filters , Client
from pyrogram.types import *
from collections import defaultdict
import sqlite3
from pyromod.listen import Client, Message
# ====================================================




class connect_db:
    def __init__(self):
        self.connect()
        self.product()
    def connect(self):
        connection = sqlite3.connect("./users.db")
        cursor = connection.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS users(
            ID INTEGER PRIMARY KEY AUTOINCREMENT ,
            USER_ID VARCHAR(300),
            NAME VARCHAR(100),
            LAST_NAME VARCHAR(100),
            USER_NAME VARCHAR(150),
            PHONE_NUMBER VARCHAR(30)
            );
        """
        cursor.execute(sql)
        connection.commit()
        connection.close()
    def product(self):
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = """
                    CREATE TABLE IF NOT EXISTS prod(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                    NAME VARCHAR(50),
                    CAPTION VARCHAR(150),
                    CATEGORY VARCHAR(20),
                    GENDER VARCHAR(10),
                    PRICE INTEGER,
                    PHOTO BLOB
                    );
                """
        cursor.execute(sql)
        connection.commit()
        connection.close()
class import_prod:
    def __init__(self,name,caption,category,gender,price,photo):
        self.name=name
        self.caption=caption
        self.category=category
        self.gender=gender
        self.price=price
        self.photo=photo
    def import_(self):
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
        insert into prod (NAME,CAPTION,CATEGORY,GENDER,PRICE,PHOTO) values ('{self.name}','{self.caption}','{self.category}','{self.gender}','{self.price}','{self.photo}')
        """
        cursor.execute(sql)
        connection.commit()
        connection.close()
class import_db:
    def __init__(self, user_id: str, name: str, last_name: str, user_name: str, phone_number: str):
        self.user_id = user_id
        self.name = name
        self.last_name = last_name
        self.user_name = user_name
        self.phone_number = phone_number

    def import_(self):
        try:
            connection = sqlite3.connect("./users.db")
            cursor = connection.cursor()
            sql = """
                    select USER_ID from users
                    """
            sql2 = f"""
                    insert into users (USER_ID,NAME,LAST_NAME,USER_NAME,PHONE_NUMBER)values ('{self.user_id}','{self.name}','{self.last_name}','{self.user_name}','{self.phone_number}')
    
            """
            cursor.execute(sql)
            list_of_userid = []

            for i in cursor:
                for j in i:
                    list_of_userid.append(j)

            if self.user_id not in list_of_userid:
                cursor.execute(sql2)
            connection.commit()
            connection.close()
        except Exception as ex:
            Message.reply_text(f"somthing went wrong: {ex}")




# ================================================================================================
admin=50872892

def Tree():
    return defaultdict(Tree)


user_pocket = Tree()
@Client.on_message(filters.private &filters.user(admin)& filters.command("start")|filters.private &filters.user(admin)&filters.regex("🏠"))
async def admin_page(client: Client, message: Message):
    connect_db()
    info=import_db(str(message.from_user.id),str(message.from_user.first_name),str(message.from_user.last_name),str(message.from_user.username),
              str(message.from_user.phone_number))
    info.import_()
    await message.reply_text("hello admin!\nwhat do you want?",reply_markup=ReplyKeyboardMarkup([["/import"],["/delete"],["product"]],resize_keyboard=True,one_time_keyboard=True))
@Client.on_message(filters.private & filters.command("start")|filters.regex("🏠"))
async def start_handler(client: Client, message: Message):
    connect_db()
    info=import_db(str(message.from_user.id),str(message.from_user.first_name),str(message.from_user.last_name),str(message.from_user.username),
              str(message.from_user.phone_number))
    info.import_()
    await message.reply_text(f"hello {message.from_user.first_name} wellcome to this store",reply_markup=ReplyKeyboardMarkup([["product"]],resize_keyboard=True))

@Client.on_message(filters.private & filters.user(admin)&filters.command("import"))
async def import_items(client:Client, message:Message):
    try:
        category_list=["hoodie","hat","shoes","jacket","tshirt"]
        gender_list=["men","women"]
        chat_id=message.chat.id
        name = await client.ask(chat_id=chat_id, text='what is name of product?',filters=filters.text)
        caption = await client.ask(chat_id=chat_id, text='what is caption of product?',filters=filters.text)
        gender = await client.ask(chat_id=chat_id, text='what is gender of product?\nmen or women', filters=filters.text)
        category = await client.ask(chat_id=chat_id, text='what is category of product?\nhoodie\nhat\nshoes\njacket\ntshirt', filters=filters.text)
        price = await client.ask(chat_id=chat_id, text='what is price of product?\njust number like:250000',filters=filters.text)
        photo = await client.ask(chat_id=chat_id, text='send photo of product',filters=filters.photo)
        gen=gender.text.lower()
        cat=category.text.lower()
        if gen not in gender_list or cat not in category_list:
            raise NameError("error:")
        items=import_prod(name.text,caption.text,cat,gen,int(price.text),photo.photo.file_id)
        items.import_()
        await message.reply_text("your product save in database!")
    except:
        await message.reply_text("we cant save this product\nsomthing went wrong")

@Client.on_message(filters.private & ~filters.user(admin)&filters.command("import"))
async def faild_import(client:Client, message:Message):
    await message.reply_text("sorry you are not admin\nyou cant import product")
@Client.on_message(filters.private& filters.user(admin)&filters.command("delete"))
async def delete_func(client:Client, message:Message):
    try:
        id_prod = await client.ask(chat_id=admin, text="enter id of product\npress 0 to cancel this proces...",
                                   filters=filters.text, reply_markup=ReplyKeyboardMarkup([["🏠"]],resize_keyboard=True))
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
            DELETE FROM prod WHERE ID='{int(id_prod.text)}'
        """
        cursor.execute(sql)
        connection.commit()
        connection.close()
        if id_prod.text=="0":
            await message.reply_text("ok you cancel that...\nenter 🏠")
        else:
            await message.reply_text(f"id:{id_prod.text} has deleted from db")
    except:
        await message.reply_text("i cant delete this id\nenter 🏠")
@Client.on_message(filters.private &filters.regex("product"))
async def show(client:Client, message:Message):
    await message.reply_text("select, men or women",reply_markup=ReplyKeyboardMarkup([["/men","/women"],["🏠"]],resize_keyboard=True))
@Client.on_message(filters.private &filters.command("men"))
async def men_list(client:Client, message:Message):
    await message.reply_text("ok! choose your category",reply_markup=ReplyKeyboardMarkup([["hoodie","hat"],["shoes"],["jacket","tshirt"],["🏠"]],resize_keyboard=True,one_time_keyboard=True))
    user_pocket[message.from_user.id]['step'] = "men"
@Client.on_message(filters.private & filters.command("women"))
async def women_list(client: Client, message: Message):
    await message.reply_text("ok! choose your category",reply_markup=ReplyKeyboardMarkup([["hoodie","hat"],["shoes"],["jacket","tshirt"],["🏠"]],resize_keyboard=True,one_time_keyboard=True))
    user_pocket[message.from_user.id]['step'] = "women"
@Client.on_message(filters.private & filters.regex("hoodie"))
async def hoodie(client: Client, message: Message):
    if user_pocket[message.from_user.id]['step'] == "men":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='men' AND CATEGORY='hoodie';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
    elif user_pocket[message.from_user.id]['step'] == "women":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='women' AND CATEGORY='hoodie';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
@Client.on_message(filters.private & filters.regex("hat"))
async def hat(client: Client, message: Message):
    if user_pocket[message.from_user.id]['step'] == "men":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='men' AND CATEGORY='hat';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
    elif user_pocket[message.from_user.id]['step'] == "women":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='women' AND CATEGORY='hat';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
@Client.on_message(filters.private & filters.regex("shoes"))
async def shoes(client: Client, message: Message):
    if user_pocket[message.from_user.id]['step'] == "men":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='men' AND CATEGORY='shoes';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
    elif user_pocket[message.from_user.id]['step'] == "women":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='women' AND CATEGORY='shoes';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
@Client.on_message(filters.private & filters.regex("jacket"))
async def jacket(client: Client, message: Message):
    if user_pocket[message.from_user.id]['step'] == "men":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='men' AND CATEGORY='jacket';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
    elif user_pocket[message.from_user.id]['step'] == "women":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='women' AND CATEGORY='jacket';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
@Client.on_message(filters.private & filters.regex("tshirt"))
async def tshirt(client: Client, message: Message):
    if user_pocket[message.from_user.id]['step'] == "men":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='men' AND CATEGORY='tshirt';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
    elif user_pocket[message.from_user.id]['step'] == "women":
        connection = sqlite3.connect("./product.db")
        cursor = connection.cursor()
        sql = f"""
                SELECT * FROM prod WHERE GENDER='women' AND CATEGORY='tshirt';
                """
        cursor.execute(sql)
        for x in cursor.fetchall():
            item_list = x
            await message.reply_photo(photo=item_list[6],caption=f"id:  {item_list[0]}\n\nname:   {item_list[1]}\ncaption:    {item_list[2]}\ncategory:    {item_list[3]}\ngender:    {item_list[4]}\nprice:    {item_list[5]}")
        connection.commit()
        connection.close()
