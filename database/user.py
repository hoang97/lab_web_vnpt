from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URI = os.getenv('DATABASE_URI')
client = MongoClient(DATABASE_URI)
db = client['prak1']
users = db['users']

class User:
    username = ''
    password = ''
    fullname = ''
    email = ''
    avatar = ''


    def __init__(self, id) -> None:
        user = users.find_one({'_id': id})
        self.id = id
        self.username = user.get('username')
        self.password = user.get('password')
        self.fullname = user.get('fullname')
        self.email = user.get('email')
        self.avatar = user.get('avatar')

    def __str__(self):
        return self.username
    
    @classmethod
    def create_user(cls, username, password, fullname='', email='', avatar="upload/user-default-img.jpg"):
        id = users.insert_one({
                'username': username, 
                'password': generate_password_hash(password),
                'fullname': fullname,
                'email': email,
                'avatar': avatar
            }).inserted_id
        user = cls(id)
        return user
    
    @classmethod
    def filter(cls,  *args, **kwargs):
        query = []
        for user in users.find(kwargs):
            query.append(User(user['_id']))
        return query
    
    def is_existed(self):
        return User.filter(username=self.username) != []
    
    def delete(self):
        return users.delete_one({'_id': self._id})
    
    def save(self):
        users.update_one(
            {'_id':self._id}, 
            {
                '$set' : {
                    'username': self.username,
                    'password': self.password,
                    'fullname': self.fullname,
                    'email': self.email,
                    'avatar': self.avatar
                }
            },
            upsert=True
        )

    def authenticate(self, password):
        return check_password_hash(self.password, password)
    
    def edit_pwd(self, password):
        self.password = generate_password_hash(password)
        self.terminate_session()

