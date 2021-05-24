# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymysql
from pymysql.converters import escape_string


class NovelSpiderPipeline:
    def __init__(self):
        self.db = pymysql.connect(
            host='',
            port=3306,
            user='root',
            passwd='',
            db='',
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
