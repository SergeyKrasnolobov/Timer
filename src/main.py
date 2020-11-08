# -*- coding: utf-8 -*-
import sys
from os import system
import json
import datetime
import time
from serializer import Activity, ActivityList, TimeEntry
from singletonmeta import singletonMeta
import logging

_win_platform = ['win32', 'windows', 'cygwin']
_mac_platform = ['Mac', 'darwin', 'os2']
_linux_platform = ['linux', 'linux2']

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

if sys.platform in _win_platform:
    import win32.win32gui as gui
    import uiautomation as auto
elif sys.platform in _mac_platform:
    try:
        from AppKit import NSWorkspace
        from Foundation import *
    except ImportError:
        logging.info('You can import all (*) only at module level')
elif sys.platform in _linux_platform:
    try:
        import linux as linux
    except ImportError:
        logging.info('You can import all (*) only at module level')
    

@singletonMeta
class MainApp:
    'Основной класс приложения'  
    def __init__(self): 
        self.active_window_name = None
        self.activity_name = None
        self.visited_url = None
        self.spend_time = None
        self.activity_list = ActivityList([])
        self.first_launch = True
        self.start_time = datetime.datetime.now()
        self.end_time = None
        
    
    def get_active_window_name(self):
        window = gui.GetForegroundWindow()
        active_window_name = gui.GetWindowText(window)
        return active_window_name  
        
            
    def get_browser_tab_url(self):
        window = gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        return edit.GetValuePattern().Value
        
      
    def run(self):
        current_window = self.get_active_window_name()
        current_url = self.get_browser_tab_url()
        try:
            while True:       
                if self.active_window_name != current_window:
                    print(current_window.split()[0])
                    self.active_window_name = current_window
                    if not self.first_launch:
                        self.end_time = datetime.datetime.now() 
                        time_entry = TimeEntry(self.start_time, self.end_time, days=0, hours=0, minutes=0, seconds=0)
                        time_entry.get_specified_times()
                        exists = False
                        for activity in self.activity_list.activities:
                            if activity.name == self.active_window_name:
                                exists = True
                                activity.time_entries.append(time_entry)
                        if not exists:
                            activity = Activity(self.active_window_name, [time_entry])
                            self.activity_list.activities.append(activity)
                        with open('activities.json', 'w') as json_file:
                            json.dump(self.activity_list.serialize(), json_file,indent=4, sort_keys=True)       
                            self.start_time = datetime.datetime.now()
                    self.first_launch = False
                current_window = self.get_active_window_name()

                if self.visited_url != current_url:
                    print(current_url)
                    self.visited_url = current_url
                current_url = self.get_browser_tab_url()


        except KeyboardInterrupt:
            with open('activities.json', 'w') as json_file:
                json.dump(self.activity_list.serialize(), json_file, indent=4, sort_keys=True)


def main(application_object):
    'Функция запуска приложения'
    application_object.run()
    
if __name__ == '__main__':
    app = MainApp()  
    main(app)


