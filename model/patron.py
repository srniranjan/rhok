from google.appengine.ext import db

class Patron(db.Model):
    name = db.StringProperty(indexed=False)
    phone = db.StringProperty(indexed=False)
    address = db.TextProperty(indexed=False)
    tasks = db.TextProperty(indexed=False)