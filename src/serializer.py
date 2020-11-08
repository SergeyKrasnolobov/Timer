import datetime
import json
from dateutil import parser


class TimeEntry:
    'Класс для получения и систематизации времени проведенного в конкнретном приложении'
    def __init__(self, start, end, days, hours, minutes, seconds):
        self.start = start
        self.end = end
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.total_time = self.end - self.start #всего времени проведенного со старта работы в приложении

    def get_specified_times(self):
        'Нормализация времеи'
        self.days = self.total_time.days
        self.seconds = self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600 
        self.minutes = self.seconds % 3600 // 60 
        self.seconds = self.seconds % 60

    def serialize(self):
        'Сериализация данных в JSON формате'
        return {
            'start': self.start.strftime("%Y-%m-%d %H:%M:%S"),
            'end': self.end.strftime("%Y-%m-%d %H:%M:%S"),
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }


class Activity:
    'Класс для сериализации наименования приложения и времени проведенного в этом приложении'
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        return {
            'name': self.name,
            'time_entries': self.make_time_entires_to_json()
        }

    def make_time_entires_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())
        return time_list

class ActivityList:
    'Класс для создания объекта списка приложений где мы работали. Возвращает List'
    def __init__(self, activities: list) -> list:
        self.activities = activities
    
    def initialize(self):
        'Создает объект ActivityList'
        activity_list = []
        with open('activities.json', 'r') as activity_file:
            data = json.load(activity_file)
            activity_list = ActivityList(activities = self.get_activities_from_json(data))
        return activity_list
    
    def get_activities_from_json(self, data):
        return_list = []
        for activity in data['activities']:
            return_list.append(
                Activity(
                    name = activity['name'],
                    time_entries = self.get_time_entires_from_json(activity),
                )
            )
        self.activities = return_list
        return return_list
    
    def get_time_entires_from_json(self, data):
        return_list = []
        for entry in data['time_entries']:
            return_list.append(
                TimeEntry(
                    start = parser.parse(entry['start']),
                    end = parser.parse(entry['end']),
                    days = entry['days'],
                    hours = entry['hours'],
                    minutes = entry['minutes'],
                    seconds = entry['seconds'],
                )
            )
        self.time_entries = return_list
        return return_list
    
    def serialize(self):
        return {
            'activities' : self.activities_to_json()
        }
    
    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())
        return activities_
