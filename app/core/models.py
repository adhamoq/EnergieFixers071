"""
Data models for the EnergieFixers071 application using Peewee ORM.
"""
from datetime import datetime, date
from peewee import *
from playhouse.sqlite_ext import JSONField
from core.database import BaseModel
import json

class Volunteer(BaseModel):
    """Model representing a volunteer"""

    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=False)
    phone = CharField(max_length=20, null=True)
    email = CharField(max_length=100, null=True)
    address = TextField(null=True)
    date_joined = DateField(default=date.today)
    is_active = BooleanField(default=True)
    notes = TextField(null=True)
    skills = TextField(null=True)  # Comma-separated skills
    availability = TextField(null=True)  # JSON string for availability schedule

    # Timestamps
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'volunteers'
        indexes = (
            (('name',), False),
            (('email',), True),  # Unique email
        )

    def __str__(self):
        return f"Volunteer: {self.name}"

    def save(self, *args, **kwargs):
        """Override save to update timestamp"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    @property
    def visit_count(self):
        """Get the number of visits for this volunteer"""
        return Visit.select().where(Visit.volunteer == self).count()

    @property
    def last_visit_date(self):
        """Get the date of the last visit"""
        last_visit = (Visit.select()
                     .where(Visit.volunteer == self)
                     .order_by(Visit.visit_date.desc())
                     .first())
        return last_visit.visit_date if last_visit else None

    @property
    def skills_list(self):
        """Get skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []

    @skills_list.setter
    def skills_list(self, skills):
        """Set skills from a list"""
        if isinstance(skills, list):
            self.skills = ', '.join(skills)
        else:
            self.skills = skills

class Visit(BaseModel):
    """Model representing a home visit"""

    id = AutoField(primary_key=True)
    volunteer = ForeignKeyField(Volunteer, backref='visits', null=True)
    kobo_submission_id = CharField(max_length=100, unique=True, null=True)

    # Visit details
    visit_date = DateField(null=False)
    visit_time = TimeField(null=True)
    address = TextField(null=False)

    # Visit data (flexible JSON storage for KoboToolbox data)
    visit_data = JSONField(default=dict)

    # Status tracking
    status = CharField(max_length=20, default='planned')  # planned, completed, cancelled
    notes = TextField(null=True)

    # Energy saving metrics
    energy_saved_kwh = FloatField(null=True)
    cost_savings_euro = FloatField(null=True)
    measures_implemented = TextField(null=True)  # JSON string

    # Timestamps
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'visits'
        indexes = (
            (('visit_date',), False),
            (('volunteer', 'visit_date'), False),
            (('kobo_submission_id',), True),
        )

    def __str__(self):
        return f"Visit to {self.address} on {self.visit_date}"

    def save(self, *args, **kwargs):
        """Override save to update timestamp"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    @property
    def measures_list(self):
        """Get implemented measures as a list"""
        if self.measures_implemented:
            try:
                return json.loads(self.measures_implemented)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @measures_list.setter
    def measures_list(self, measures):
        """Set measures from a list"""
        if isinstance(measures, list):
            self.measures_implemented = json.dumps(measures)
        else:
            self.measures_implemented = measures

class Appointment(BaseModel):
    """Model representing a Calendly appointment"""

    id = AutoField(primary_key=True)
    calendly_event_uuid = CharField(max_length=100, unique=True, null=False)
    calendly_uri = CharField(max_length=255, null=True)

    # Appointment details
    event_name = CharField(max_length=200, null=False)
    start_time = DateTimeField(null=False)
    end_time = DateTimeField(null=False)
    timezone = CharField(max_length=50, null=True)

    # Invitee information
    invitee_name = CharField(max_length=100, null=True)
    invitee_email = CharField(max_length=100, null=True)
    invitee_phone = CharField(max_length=20, null=True)

    # Location/meeting details
    location = TextField(null=True)
    meeting_type = CharField(max_length=50, null=True)  # in_person, phone, online
    meeting_url = CharField(max_length=255, null=True)

    # Status
    status = CharField(max_length=20, default='scheduled')  # scheduled, completed, cancelled, rescheduled

    # Additional data from Calendly
    calendly_data = JSONField(default=dict)

    # Timestamps
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'appointments'
        indexes = (
            (('start_time',), False),
            (('invitee_email',), False),
            (('calendly_event_uuid',), True),
        )

    def __str__(self):
        return f"Appointment: {self.event_name} on {self.start_time.date()}"

    def save(self, *args, **kwargs):
        """Override save to update timestamp"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        """Check if appointment is in the future"""
        return self.start_time > datetime.now()

    @property
    def duration_minutes(self):
        """Get appointment duration in minutes"""
        if self.end_time and self.start_time:
            return int((self.end_time - self.start_time).total_seconds() / 60)
        return 0

class Setting(BaseModel):
    """Model for storing application settings"""

    id = AutoField(primary_key=True)
    key = CharField(max_length=50, unique=True, null=False)
    value = TextField(null=True)
    description = TextField(null=True)

    # Timestamps
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'settings'

    def __str__(self):
        return f"Setting: {self.key} = {self.value}"

    def save(self, *args, **kwargs):
        """Override save to update timestamp"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def get_value(cls, key, default=None):
        """Get a setting value by key"""
        try:
            setting = cls.get(cls.key == key)
            return setting.value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_value(cls, key, value, description=None):
        """Set a setting value by key"""
        setting, created = cls.get_or_create(
            key=key,
            defaults={'value': value, 'description': description}
        )
        if not created:
            setting.value = value
            if description:
                setting.description = description
            setting.save()
        return setting

# Utility functions for database operations

def get_volunteer_stats():
    """Get volunteer statistics"""
    return {
        'total_volunteers': Volunteer.select().count(),
        'active_volunteers': Volunteer.select().where(Volunteer.is_active == True).count(),
        'total_visits': Visit.select().count(),
        'visits_this_month': Visit.select().where(
            Visit.visit_date >= date.today().replace(day=1)
        ).count(),
    }

def get_recent_visits(limit=10):
    """Get recent visits"""
    return (Visit.select()
            .join(Volunteer, JOIN.LEFT_OUTER)
            .order_by(Visit.visit_date.desc())
            .limit(limit))

def get_upcoming_appointments(limit=10):
    """Get upcoming appointments"""
    return (Appointment.select()
            .where(Appointment.start_time > datetime.now())
            .order_by(Appointment.start_time)
            .limit(limit))

def search_volunteers(query):
    """Search volunteers by name or email"""
    return (Volunteer.select()
            .where(
                (Volunteer.name.contains(query)) |
                (Volunteer.email.contains(query))
            )
            .order_by(Volunteer.name))
