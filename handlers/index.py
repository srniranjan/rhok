import webapp2
import json
import os

from model.patron import Patron
from model.reminder import Reminder
from google.appengine.ext.webapp import template

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

app = webapp2.WSGIApplication([('/', HomepageHandler),
                               ('/new_patron', NewPatronHandler),
                               ('/save_patron',SavePatronHandler)])
