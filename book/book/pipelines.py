# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import openpyxl, json
import pymysql
from pymysql.converters import escape_string
import datetime


class BookPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.append(["分类", "分类链接", "书本链接", "书名", "简述", "作者", "出版社", "出版时间", "评论数", "价格"])

    def process_item(self, item, spider):
        line = [item["分类"], item["分类链接"], item["book_url"], item["name"], item["desc"], item["author"], item["pub"],
                item["date_time"], item["comm_num"], item["price"]]
        self.ws.append(line)
        self.wb.save("dangdang.xlsx")
        return item


class TiebaPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.append(["name", "content", "url"])

    def process_item(self, item, spider):
        print(item)
        line = [item["name"], item["content"], item["url"]]
        self.ws.append(line)
        self.wb.save("tieba.xlsx")
        return item


class TravelPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='whb1107',
            db='travel',
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item["name"] == "广州线路":
            item["lid_id"] = 1
        if item["name"] == "韶关线路":
            item["lid_id"] = 1
        if item["name"] == "深圳线路":
            item["lid_id"] = 1
        if item["name"] == "珠海线路":
            item["lid_id"] = 1
        if item["name"] == "清远线路":
            item["lid_id"] = 1
        if item["name"] == "肇庆线路":
            item["lid_id"] = 1
        if item["name"] == "茂名线路":
            item["lid_id"] = 1
        if item["name"] == "广州线路":
            item["lid_id"] = 1
        if item["name"] == "惠州线路":
            item["lid_id"] = 1
        if item["name"] == "梅州线路":
            item["lid_id"] = 1
        if item["name"] == "汕尾线路":
            item["lid_id"] = 1
        if item["name"] == "河源线路":
            item["lid_id"] = 1
        if item["name"] == "阳江线路":
            item["lid_id"] = 1
        if item["name"] == "东莞线路":
            item["lid_id"] = 1
        if item["name"] == "中山线路":
            item["lid_id"] = 1
        if item["name"] == "佛山线路":
            item["lid_id"] = 1
        if item["name"] == "潮州线路":
            item["lid_id"] = 1
        if item["name"] == "汕头线路":
            item["lid_id"] = 1
        if item["name"] == "江门线路":
            item["lid_id"] = 1
        if item["name"] == "湛江线路":
            item["lid_id"] = 1
        if item["name"] == "桂林线路":
            item["lid_id"] = 2
        if item["name"] == "福建线路":
            item["lid_id"] = 2
        if item["name"] == "湖南线路":
            item["lid_id"] = 2
        if item["name"] == "湖北线路":
            item["lid_id"] = 2
        if item["name"] == "海南线路":
            item["lid_id"] = 2
        if item["name"] == "江西线路":
            item["lid_id"] = 2
        if item["name"] == "北京线路":
            item["lid_id"] = 2
        if item["name"] == "华东线路":
            item["lid_id"] = 2
        if item["name"] == "东北线路":
            item["lid_id"] = 2
        if item["name"] == "内蒙古线":
            item["lid_id"] = 2
        if item["name"] == "新疆线路":
            item["lid_id"] = 2
        if item["name"] == "陕西线路":
            item["lid_id"] = 2
        if item["name"] == "山西线路":
            item["lid_id"] = 2
        if item["name"] == "山东线路":
            item["lid_id"] = 2
        if item["name"] == "甘肃线路":
            item["lid_id"] = 2
        if item["name"] == "安微线路":
            item["lid_id"] = 2
        if item["name"] == "贵州线路":
            item["lid_id"] = 2
        if item["name"] == "云南线路":
            item["lid_id"] = 2
        if item["name"] == "西藏线路":
            item["lid_id"] = 2
        if item["name"] == "四川线路":
            item["lid_id"] = 2
        if item["name"] == "西北线路":
            item["lid_id"] = 2
        if item["name"] == "香港线路":
            item["lid_id"] = 3
        if item["name"] == "澳门线路":
            item["lid_id"] = 3
        if item["name"] == "台湾游":
            item["lid_id"] = 3
        if item["name"] == "港澳联游":
            item["lid_id"] = 3
        if item["name"] == "亚洲线路":
            item["lid_id"] = 4
        if item["name"] == "欧洲线路":
            item["lid_id"] = 4
        if item["name"] == "美洲线路":
            item["lid_id"] = 4
        if item["name"] == "非洲线路":
            item["lid_id"] = 4
        if item["name"] == "澳洲线路":
            item["lid_id"] = 4
        if item["name"] == "海岛游轮":
            item["lid_id"] = 5

        insert_sql = "INSERT INTO line(city, lname, img, sec, price, to_time, detail,lid_id) VALUES ('%s','%s', '%s', '%s', '%d', '%d', '%s', '%d')" % (
            item['name'], escape_string(item['lname']), item['img'], item['sec'], item['price'], item['to_time'],
            escape_string(item['detail']), item['lid_id'])
        self.cursor.execute(insert_sql)

        self.connect.commit()
        print("\033[36m------------->保存数据到mysql成功<------------------------")
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


class XiaoshuoPipeline:
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='whb1107',
            db='xiaoshuo',
            charset='utf8'
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        #  分类表
        self.cursor.execute('select id from fenlei where `name` = "{}"'.format(item['fenlei']))
        fenlei_id = self.cursor.fetchone()
        if not fenlei_id:
            creat_time = datetime.datetime.now()
            self.cursor.execute(
                'insert into fenlei (`name`, creat_time, update_time) values("%s", "%s", "%s")' % (
                    item['fenlei'], creat_time,
                    creat_time))
            self.db.commit()
            self.cursor.execute('select id from fenlei where `name` = "{}"'.format(item['fenlei']))
            fenlei_id = self.cursor.fetchone()
        fenlei_id = fenlei_id[0]

        #  小说表
        self.cursor.execute('select id from book where `name` = "{}"'.format(item['book_name']))
        book_id = self.cursor.fetchone()
        if not book_id:
            creat_time = datetime.datetime.now()
            print(creat_time)
            self.cursor.execute(
                'insert into book (`name`, author, `describe`, creat_time, update_time, fenlei_id, `click`) values("{}","{}","{}","{}","{}","{}","{}")'.format(
                    item['book_name'], item['author'], item['desc'], creat_time, creat_time, fenlei_id, 0
                ))
            self.db.commit()
            self.cursor.execute('select id from book where name = "{}"'.format(item['book_name']))
            book_id = self.cursor.fetchone()
        book_id = book_id[0]

        #  章节表
        # self.cursor.execute('select id from chapter where `name` = "{}"'.format(item['chapter_name']))
        # chapter_id = self.cursor.fetchone()
        # if not chapter_id:
        creat_time = datetime.datetime.now()
        self.cursor.execute(
            'insert into chapter(`name`, content, creat_time, update_time, book_id, `number`) values ("%s","%s","%s","%s","%s","%s")' % (
                item['chapter_name'], escape_string(item['content']), creat_time, creat_time, book_id, item["number"]))

        self.db.commit()
        print("\033[36m------------->保存数据到mysql成功<------------------------")
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()


class NovelSpiderPipeline:
    def __init__(self):
        self.db = pymysql.connect(
            host='192.168.0.222',
            port=3306,
            user='root',
            passwd='whb1107',
            db='mysite',
            charset='utf8'
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        self.cursor.execute('select id from category where category_name = "{}"'.format(item['category_name']))
        category_id = self.cursor.fetchone()
        if not category_id:
            self.cursor.execute('insert into category (category_name) values("{}")'.format(item['category_name']))
            self.db.commit()
            self.cursor.execute('select id from category where category_name = "{}"'.format(item['category_name']))
            category_id = self.cursor.fetchone()
        category_id = category_id[0]

        self.cursor.execute('select id from author where author_name = "{}"'.format(item['author']))
        author_id = self.cursor.fetchone()
        if not author_id:
            self.cursor.execute('insert into author (author_name) values("%s")' % (item['author']))
            self.db.commit()
            self.cursor.execute('select id from author where author_name = "{}"'.format(item['author']))
            author_id = self.cursor.fetchone()
        author_id = author_id[0]
        self.cursor.execute("SELECT id FROM book WHERE book_name = '%s'" % (item['book_name'],))
        book_id = self.cursor.fetchone()
        if not book_id:
            self.cursor.execute(
                "INSERT INTO book (book_name, image, intro, author_id, category_id, `number`) VALUES ('%s','%s','%s','%s','%s','%s')" %
                (item['book_name'], item['image'], item['intro'], author_id, category_id, 0))
            self.db.commit()
            print("\033[35m------------->保存小说《%s》到mysql成功<------------------------" % item['book_name'])
            self.cursor.execute("SELECT id FROM book WHERE book_name = '%s'" % (item['book_name'],))
            book_id = self.cursor.fetchone()
        book_id = book_id[0]

        self.cursor.execute(
            "INSERT INTO chapter (`number`, chapter_name, content, book_id) VALUES ('%s','%s','%s','%s')" % (
                item['number'], item['chapter_name'], escape_string(item['content']), book_id))
        self.db.commit()
        print("\033[36m------------->保存章节-->%s<--到mysql成功<------------------------" % item['chapter_name'])
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
