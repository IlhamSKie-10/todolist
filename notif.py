import sys
from plyer import notification
    

class notifi:
    def showNotification(self, title, message):
            notification.notify(
            title='Task Done!',
            message='You have completed a task.',
            app_name='To Do List'
        )
        
