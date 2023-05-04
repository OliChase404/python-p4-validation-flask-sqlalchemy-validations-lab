import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Phone_REGEX_basic = re.compile(r'^\d{10}$')
# Phone_REGEX_adv = re.compile(
#     r'^(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*(\d{3})\s*\)|(\d{3}))(?:\s*[.-]?\s*)(\d{3})(?:\s*[.-]?\s*)(\d{4}))(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$')


class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError('Phone number must not be empty')
        elif not re.match(r'^\d{10}$', phone_number):
            raise ValueError('Phone number must be exactly 10 digits')
        else:
            return phone_number
    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 1 or name == None:
            raise ValueError('Name must not be empty')
        else:
            return name
        
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1, 80), nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('title')
    def validate_title(self, key, title):
        if len(title) < 1 or title == None:
            raise ValueError('Title must not be empty')
        elif title == 'Why I love programming.':
            raise ValueError('Title must not be Why I love programming.')
        else:
            return title
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 1 or content == None:
            raise ValueError('Content must not be empty')
        elif len(content) < 250:
            raise ValueError('Content must be at least 250 characters')
        else:
            return content
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) < 1 or summary == None:
            raise ValueError('Summary must not be empty')
        elif len(summary) >= 250:
            raise ValueError('Summary must be less than 250 characters')
        else:
            return summary
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Category must be Fiction or Non-Fiction')
        else:
            return category
        

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
