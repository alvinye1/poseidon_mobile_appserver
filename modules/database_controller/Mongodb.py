#!-*- coding:utf-8-*-
import pymongo


class MongoDB(object):
    '''
    #    (>)  大于 - $gt
    #    (<)  小于 - $lt
    #    (>=)  大于等于 - $gte
    #    (<= )  小于等于 - $lte
    '''
    def __init__(self, host, port, db, site, user, passwd):
        self.host = host
        self.port = port
        self.db = db
        self.site = site
        self.user = user
        self.passwd = passwd
        self.con = self.connetion()

    def connetion(self):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.client.admin.authenticate(self.user, self.passwd)
        dba = self.client[self.db]
        col = dba[self.site]
        return col

    def search(self, sql, types):
        '''
        :param sql: all "", one_field  {"fieldname":"target"},some_field {"fieldname1":"1","fieldname2":"1"}
        :param types:
        :return:
        '''
        data = []
        if types == "all":
            find = self.con.find()
        elif types == "one_field":
            find = self.con.find(sql,{"_id": 0})
        elif types == "some_field":
            find = self.con.find({}, sql)
        for x in find:
            data.append(x)
        return data

    def remove(self, sql, types):
        '''
        many  sql={"fieldname": {"$regex": "^F"} }
        one sql = {"fieldname":"target"}
        '''
        if types == "one":
            self.con.delete_one(sql)
        elif types == "many":
            self.con.delete_many(sql)
        elif types == "all":
            self.con.delete_many({})
        elif types == "drop":
            self.con.drop()

    def insert(self, sql, types):
        '''
        type = one ,sql = {};
        type = many, sql = [{},{}];
        '''
        if types == "one":
            self.con.insert_one(sql)
        elif types == "many":
            self.con.insert_many(sql)

    def update(self, old, new, types):
        '''
        one old = { "alexa": "10000" } new = { "$set": { "alexa": "12345" } }
        many old = { "name": { "$regex": "^F" } } new = { "$set": { "alexa": "123" } }
        '''
        if types == "one":
            self.con.update_one(old, new)
        elif types == "many":
            self.con.update_many(old, new)

    def sorted(self, field, types):
        '''
        :param field: only one field
        :param types: up down
        :return:
        '''
        if types == "up":
            find = self.con.find().sort(field)
        elif types == "down":
            find = self.con.find().sort(field, -1)
        return find

    def __del__(self):
        self.client.close()

if __name__ == '__main__':
    # a = MongoDB('80.7.238.136', 8889, 'testposeidon', 'adi', 'root', 'qwert789')
    # b = a.search('aaa', 'all')
    db = MongoDB('80.7.238.136', 8889, 'testposeidon', 'adi', 'root', 'qwert789')

    data = db.search(({'$or':[{'CPU':{'$regex':'/2.0/'}}]}), 'one_field')
    print(data)
    search = db.search(({"IP Address": "10.252.1.10"}), 'one_field')
    print(search)
    # c = a.insert({'name':"itachi"},'one')
    # d = a.search('dsad','all')
    # print(d)