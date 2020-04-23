from bookFlask import db
from datetime import datetime

# SQLAlchemy database class/methods

# Tables are creating by making a new class of type db.Model


# A db.Model object is a new Table
class Publication(db.Model):

    __tablename__ = 'publication'

    # One of the benefits of SQLAlchemy is we can create tables here in Python, rather than writing SQL in the database platform
    # The ORM (Object Relational Mapper) converts the class definitions to the SQL statements

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    # in-built python methods
    # __init__() is called when new instances of a class are created, it initializes reference variables and attributes
    # __repr__() takes only 1 parameter, self, and returns a string representation of an instance,
    #                this helps in formatting and producing a readble output of the data

    def __init__(self, name):

        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format(self.name)




# A db.Model object is a new Table
class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    # The index=True attribute will speed up retrieving records from the database
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    # String it not the image itself, but the filepath to the image
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    # this datetime is from the Python library (and not SQLAlchemy) and needs to be imported above
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())


    # Relationship - this establishes the relationship from this 'book' table to the 'publication' table above
    # It sets the book's 'pub_id' value as a Foreign Key to the publication table's 'id' values
    # Each Publisher in the publication table contains unique books from that publisher alone

    # This is a 1-to-Many relationship between the publication.id and the book.pub_id
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        # book_id and pub_date have been left out because they are automatically generated and can't be changed
        # they will render on their own in the table
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return 'The title is {} by author {}'.format(self.title, self.author)
