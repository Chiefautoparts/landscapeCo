# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Appointment(models.Model):
	day = models.DateField(u'Day of the appointment', help_text=u'Day of the appointment')
	start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
	end_time = models.TimeField(u'Ending time', help_text=u'Ending time')
	notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)

	class Meta:
		verbose_name = u'Scheduling'
		verbose_name_plural = u'Scheduling'

	def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
		overlap = False
		if new_start == fixed_end or new_end == fixed_start:
			overlap = False
		elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):
			overlap = True
		elif new_start <= fixed_start and new_end >= fixed_end:
			overlap = True

		return overlap

	def get_absolute_url(self):
		url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model.name), args=[self.id])
		return u'<a href="%s">%s</a>' % (url, str(self.start_time))

	def clean(self):
		if self.end_time <= self.start_time:
			raise ValidationError('Ending times must be after starting times')

		appointments = Appointment.objects.filter(day=self.day)
		if appointments.exists():
			for appointment in appointments:
				if self.check_overlap(appointment.start_time, appointment.end_time, self.start_time, self.end_time):
					raise ValidationError(
						'There is an overlap with another appointment: ' + str(appointment.day) + ', ' + str(appointment.start_time) + '-' + str(appointment.end_time))