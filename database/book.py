from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URI = os.getenv('DATABASE_URI')
client = MongoClient(DATABASE_URI)
db = client['prak1']
books = db['books']


class Book:
    author = ''
    title = ''
    price = ''
    description = ''
    image = ''

    def __init__(self, id):
        book = books.find_one({'_id': id})
        self.id = id
        self.title = book.get('title')
        self.price = book.get('price')
        self.description = book.get('description')
        self.image = book.get('image')
        self.author = book.get('author ')

    def __str__(self):
        return self.title
    
    @classmethod
    def create(cls, title, price, description, image, author):
        id = books.insert_one({
                'title': title, 
                'price': price,
                'description': description,
                'image': image,
                'author': author
            }).inserted_id
        book = cls(id)
        return book
    
    def is_existed(self):
        return Book.filter(id=self.id) != []
    
    @classmethod
    def filter(cls,  *args, **kwargs):
        query = []
        for book in books.find(kwargs):
            query.append(Book(book['_id']))
        return query
    
    def delete(self):
        return books.delete_one({'_id': self._id})
    
    def save(self):
        books.update_one(
            {'_id':self._id}, 
            {
                '$set' : {
                    'title': self.title, 
                    'price': self.price,
                    'description': self.description,
                    'image': self.image,
                    'author': self.author
                }
            },
            upsert=True
        )