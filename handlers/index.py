import webapp2
import logging
import os
from pytz import timezone
from datetime import datetime

from model.patron import Patron
from model.reminder import Reminder
from google.appengine.ext.webapp import template
from twilio import send_sms

class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        index_path = os.path.join(os.path.dirname(__file__), '../templates/index.html')
        self.response.out.write(template.render(index_path, None))

class NewPatronHandler(webapp2.RequestHandler):
    def get(self):
        index_path = os.path.join(os.path.dirname(__file__), '../templates/new_patron.html')
        self.response.out.write(template.render(index_path, None))

class SavePatronHandler(webapp2.RequestHandler):
    def add_tasks(self, tasks_str, patron):
        task_strs = tasks_str.split("####")[1:]
        for task_str in task_strs:
            task_name, times = task_str.split('~~~~')
            for time in times.split(';'):
                reminder = Reminder()
                reminder.name = task_name
                reminder.time = time
                reminder.patron = patron
                reminder.put()

    def post(self):
        tasks = self.request.get('tasks')
        patron = Patron()
        patron.name = self.request.get('name')
        patron.phone = self.request.get('phone')
        patron.address = self.request.get('address')
        patron.tasks = tasks
        patron.put()
        self.add_tasks(tasks, patron)

class SendRemindersHandler(webapp2.RequestHandler):
    def get(self):
        india_tz = timezone('Asia/Calcutta')
        india_time = datetime.now(india_tz)
        reminders = Reminder.all()
        for reminder in reminders.run(limit=1000):
            if india_time.hour == int(reminder.time):
                send_sms(reminder.patron.phone, reminder.name)
                logging.info('+++++++++++++++')
                logging.info('Running ' + reminder.name + ' at ' + reminder.patron.phone)
                logging.info('+++++++++++++++')

class PatronValObj():
    def __init__(self, patron):
        self.name = patron.name
        self.phone = patron.phone
        self.address = patron.address
        self.tasks = ''
        for task_str in patron.tasks.split('####')[1:]:
            task_name, times = task_str.split('~~~~')
            self.tasks += task_name + ' at ' + times + ', '
        self.patron_id = patron.key().id()

class ListPatronsHandler(webapp2.RequestHandler):
    def get(self):
        patrons = Patron.all()
        val_objs = []
        for patron in patrons.run(limit=1000):
            val_objs.append(PatronValObj(patron))
        index_path = os.path.join(os.path.dirname(__file__), '../templates/list_patrons.html')
        self.response.out.write(template.render(index_path, {'patrons':val_objs}))

class DelPatronHandler(webapp2.RequestHandler):
    def post(self):
        patron = Patron.get_by_id(long(self.request.get('patron_id')))
        reminders = Reminder.all()
        reminders.filter("patron =", patron)
        for reminder in reminders.run(limit=1000):
            reminder.delete()
        patron.delete()

app = webapp2.WSGIApplication([('/', HomepageHandler),
                               ('/new_patron', NewPatronHandler),
                               ('/save_patron',SavePatronHandler),
                               ('/send_reminders',SendRemindersHandler),
                               ('/list_patrons',ListPatronsHandler),
                               ('/del_patron',DelPatronHandler)])
