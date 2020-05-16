import re
import json
from datetime import datetime, timedelta


def get_user_role(user):
	try:
		client = user.client
		return 'client'
	except:
		return 'doctor'


def parse_schedule(schedule):
	DAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',)
	schedule = re.sub(r' ', '', schedule)
	days, time = re.split(r',', schedule)

	start_day, end_day = re.split(r'-', days)
	days = list(set([0, 1, 2, 3, 4, 5, 6])- set([day for day in range(DAYS.index(start_day), DAYS.index(end_day) + 1)]))
	days = [(day + 1) % 7 for day in days]

	start_time, end_time = re.split(r'-', time)
	start_hour = datetime.strptime(start_time, '%H:%M').hour
	end_hour = datetime.strptime(end_time, '%H:%M').hour

	time_intervals = list()
	time = start_time
	for hour in range((end_hour - start_hour)*2 + 1):
		time_intervals.append(time)
		time = datetime.strptime(time, '%H:%M')
		time = time + timedelta(minutes=30)
		time = time.strftime('%H:%M')

	time_intervals = json.dumps(time_intervals)

	return days, time_intervals


def get_disabled_tickets(tickets):
	disabled_tickets = {}
	for ticket in tickets:
		date = ticket.date.strftime('%Y-%m-%d')
		time = ticket.time.strftime('%H:%M')
		try:
			disabled_tickets[date].append(time)
		except:
			disabled_tickets[date] = list()
			disabled_tickets[date].append(time)

	disabled_tickets = json.dumps(disabled_tickets)
	
	return disabled_tickets