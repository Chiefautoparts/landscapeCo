from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from models import Appointment

class AppointmentCalendar(HTMLCalendar):
	def __init__(self, appointments=None):
		super(AppointmentCalendar, self).__init__()
		self.appointments = appointments

	def formatday(self, day, weekday, appointments):
		appointments_from_day = appointments.filter(day__day=day)
		appointments_html = "<ul>"
		for appointment in appointments_from_day:
			appointments_html += appointment.get_absolute_url() + "<br>"
		appointments_html += "</ul>"
		if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, appointments_html)
 
    def formatweek(self, theweek, appointments):
        s = ''.join(self.formatday(d, wd, appointments) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
 
    def formatmonth(self, theyear, themonth, withyear=True):
        appointments = Appointment.objects.filter(day__month=themonth)
 
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, appointments))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)