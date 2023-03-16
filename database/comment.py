from pymongo import MongoClient
from .book import Book
from .user import User
import os, time
from dotenv import load_dotenv

load_dotenv()
DATABASE_URI = os.getenv('DATABASE_URI')
client = MongoClient(DATABASE_URI)
db = client['prak1']
comments = db['comments']


class Comment:
    author = ''
    book = ''
    content = ''
    timestamp = ''

    def __init__(self, id):
        comment = comments.find_one({'_id': id})
        self.id = id
        self.author_id = comment.get('author_id')
        self.book_id = comment.get('book_id')
        self.content = comment.get('content')
        self.timestamp = comment.get('timestamp')
    
    def __str__(self):
        return self.id
    
    @classmethod
    def _create(cls, author_id, book_id, content):
        if User.filter(_id=author_id) == [] or Book.filter(_id=book_id) == []:
            raise Exception
        id = comments.insert_one({
                'author_id': author_id, 
                'book_id': book_id,
                'content': content,
                'timestamp': time.time(),
            }).inserted_id

        comment = cls(id)
        return comment
    
    def is_existed(self):
        return Book.filter(id=self.id) != []
    
    @classmethod
    def filter(cls,  *args, **kwargs):
        query = []
        for book in comments.find(kwargs):
            query.append(Book(book['_id']))
        return query
    
    def delete(self):
        return comments.delete_one({'_id': self._id})
    
    def save(self):
        comments.update_one(
            {'_id':self._id}, 
            {
                '$set' : {
                    'author': self.author_id, 
                    'book': self.book_id,
                    'content': self.content,
                    'timestamp': self.timestamp,
                }
            },
            upsert=True
        )