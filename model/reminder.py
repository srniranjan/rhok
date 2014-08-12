from google.appengine.ext import db

class Reminder(db.Model):
    patron = db.ReferenceProperty()
    name = db.StringProperty(indexed=False)
    time = db.StringProperty(indexed=False)