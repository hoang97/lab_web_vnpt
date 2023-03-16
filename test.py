from database.book import Book

book = Book.filter(title='hello world')[0]
print(book.id)

from database.user import User

# admin = User.create_user('admin', 'admin')

# print(admin.id)

admin = User.filter(username='admin')[0]
# auth = admin.authenticate('vcl')

# print(auth)

from database.comment import Comment

comment1 = Comment._create(admin.id, book.id, "sachnhuloz")

print(comment1.content)