
from google.appengine.ext import ndb
from model import Account, Tables
import datetime

# I happened to contact a friend who owns a restaurant, to understand how they go about
# their booking process and how they make their customers wait. I applied that same logic
# with a couple of tweaks and coded an algorithm which does exactly that.
# This is that algorithm.



def rest_book(userid,no_people,booking_time,waiting_list =[]):
	avg_eating_time = 60  #minutes  Assumption
	no_of_2_tables = Tables.query().filter(Tables.max_occupancy == 2)
	no_of_4_tables = Tables.query().filter(Tables.max_occupancy == 4)
	no_of_8_tables = Tables.query().filter(Tables.max_occupancy == 8)

	predicted_first_2 = no_of_2_tables.order('time_of_booking').fetch(1) #This will fetch the row of table who entered first
	predicted_first_4 = no_of_4_tables.order('time_of_booking').fetch(1) #This will fetch the row of table who entered first
	predicted_first_8 = no_of_8_tables.order('time_of_booking').fetch(1) #This will fetch the row of table who entered first


	if no_people <=2:
		if len(no_of_2_tables.filter(Tables.booked == False).fetch()) > 0:
			return True,0
		elif (len(no_of_4_tables.filter(Tables.booked == False).fetch())//len(no_of_4_tables.fetch()) >= 0.8):
			return True,0
		else:
			waiting_time = diff_times_in_minutes(predicted_first_2[0].time_of_booking,booking_time) + avg_eating_time
			waiting_list.append([userid,waiting_time])
			return False,waiting_time

	if no_people > 2 and no_people <= 4:
		if len(no_of_4_tables.filter(Tables.booked == False).fetch()) > 0:
			return True,0
		elif (len(no_of_4_tables.filter(Tables.booked == False).fetch())//len(no_of_4_tables.fetch()) >= 0.8):
			return True,0
		else:
			waiting_time = diff_times_in_minutes(predicted_first_4[0].time_of_booking,booking_time) + avg_eating_time
			waiting_list.append([userid,waiting_time])
			return False,waiting_time

	if no_people >4 and no_people <=8:
		if len(no_of_8_tables.filter(Tables.booked == False).fetch()) > 0:
			return True,0
		else:
			waiting_time = diff_times_in_minutes(predicted_first_4[0].time_of_booking,booking_time) + avg_eating_time    
			waiting_list.append([userid,waiting_time])
			return  False,waiting_time





def diff_times_in_minutes(t1, t2):
    # assumes t1 & t2 are python times, on the same day and t2 is after t1
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60*h1)
    t2_secs = s2 + 60 * (m2 + 60*h2)
    return( (t2_secs - t1_secs)//60) # Convert it into minutes

