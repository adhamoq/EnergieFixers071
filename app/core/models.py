"""
Database models for EnergieFixers071 application.
"""
import logging
from datetime import datetime, date
from peewee import (
    Model, CharField, TextField, DateField, DateTimeField, 
    BooleanField, IntegerField, FloatField, ForeignKeyField
)

logger = logging.getLogger(__name__)

# Import database proxy
from core.database import db

class BaseModel(Model):
    """Base model class"""
    class Meta:
        database = db

class Volunteer(BaseModel):
    """Volunteer model"""
    name = CharField(max_length=100)
    phone = CharField(max_length=20, null=True)
    email = CharField(max_length=100, null=True)
    address = TextField(null=True)
    skills = TextField(null=True)
    notes = TextField(null=True)
    is_active = BooleanField(default=True)
    date_joined = DateField(default=date.today)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    @property
    def visit_count(self):
        """Get number of visits for this volunteer"""
        try:
            return self.visits.count()
        except:
            return 0
    
    @property
    def last_visit_date(self):
        """Get date of last visit"""
        try:
            last_visit = self.visits.order_by(Visit.visit_date.desc()).first()
            return last_visit.visit_date if last_visit else None
        except:
            return None

class Visit(BaseModel):
    """Visit model based on KoboToolbox form"""
    # Basic Information
    volunteer = ForeignKeyField(Volunteer, backref='visits', null=True)
    address = CharField(max_length=200)
    visit_date = DateField(default=date.today)
    appointment_time = CharField(max_length=20, null=True)
    executed_by = CharField(max_length=200, null=True)
    
    # Resident Information
    residents_count = IntegerField(default=1)
    energy_measures_taken = BooleanField(default=False)
    which_measures = TextField(null=True)
    ventilation = BooleanField(default=False)
    
    # Energy Contract Information
    contract_duration = CharField(max_length=50, null=True)
    electricity_consumption = FloatField(null=True)
    gas_consumption = FloatField(null=True)
    monthly_amount = FloatField(null=True)
    energy_bill_concerns = BooleanField(default=False)
    
    # Materials and Interventions
    radiator_foil_meters = FloatField(default=0)
    radiator_fan_needed = BooleanField(default=False)
    small_power_strip_needed = BooleanField(default=False)
    led_lamps_needed = BooleanField(default=False)
    e14_leds_count = IntegerField(default=0)
    e27_leds_count = IntegerField(default=0)
    draft_strip_meters = FloatField(default=0)
    door_draft_band = BooleanField(default=False)
    door_closers = BooleanField(default=False)
    door_closer_spring = BooleanField(default=False)
    
    # Door Assessment
    all_interior_doors_present = BooleanField(default=True)
    missing_doors_description = TextField(null=True)
    
    # Bathroom
    shower_timer = BooleanField(default=False)
    shower_head = BooleanField(default=False)
    
    # Heating System
    current_cv_temperature = IntegerField(null=True)
    cv_temperature_lowered_to = IntegerField(null=True)
    cv_water_pressure_under_1_bar = BooleanField(default=False)
    tap_comfort_off = BooleanField(default=False)
    large_power_strip_needed = BooleanField(default=False)
    
    # Problems
    problems_with = TextField(null=True)
    mold_issues = BooleanField(default=False)
    moisture_issues = BooleanField(default=False)
    draft_issues = BooleanField(default=False)
    problem_rooms_description = TextField(null=True)
    hygrometer_needed = BooleanField(default=False)
    
    # Community Building
    knows_potential_fixers = BooleanField(default=False)
    wants_to_help = BooleanField(default=False)
    tell_neighbors = BooleanField(default=False)
    
    # Additional Information
    old_refrigerator = BooleanField(default=False)
    share_info_with_housing_corp = BooleanField(default=False)
    keep_updated_on_results = BooleanField(default=False)
    other_remarks = TextField(null=True)
    
    # KoboToolbox Integration
    kobo_submission_id = CharField(max_length=50, null=True, unique=True)
    visit_data = TextField(null=True)  # JSON storage for full form data
    
    # Metadata
    status = CharField(max_length=20, default='completed')
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

class Appointment(BaseModel):
    """Appointment model for Calendly integration"""
    calendly_event_uuid = CharField(max_length=100, unique=True)
    calendly_uri = CharField(max_length=200, null=True)
    event_name = CharField(max_length=200)
    start_time = DateTimeField()
    end_time = DateTimeField()
    status = CharField(max_length=20, default='scheduled')
    location = CharField(max_length=200, null=True)
    meeting_url = CharField(max_length=500, null=True)
    meeting_type = CharField(max_length=20, default='in_person')
    
    # Invitee Information
    invitee_name = CharField(max_length=100, null=True)
    invitee_email = CharField(max_length=100, null=True)
    
    # Integration Data
    calendly_data = TextField(null=True)  # JSON storage
    
    # Metadata
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

def create_tables():
    """Create all database tables"""
    try:
        tables = [Volunteer, Visit, Appointment]
        db.create_tables(tables, safe=True)
        logger.info(f"Created {len(tables)} database tables")
        
        # Create dummy data if tables are empty
        create_dummy_data()
        
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise

def create_dummy_data():
    """Create dummy data for testing if database is empty"""
    try:
        # Only create dummy data if no volunteers exist
        if Volunteer.select().count() == 0:
            logger.info("Creating dummy data...")
            
            # Create dummy volunteers
            volunteers_data = [
                {"name": "Jan van der Berg", "phone": "06-12345678", "email": "jan@email.nl", "is_active": True},
                {"name": "Maria Santos", "phone": "06-87654321", "email": "maria@email.nl", "is_active": True},
                {"name": "Ahmed Hassan", "phone": "06-11223344", "email": "ahmed@email.nl", "is_active": True},
                {"name": "Sophie Jansen", "phone": "06-55667788", "email": "sophie@email.nl", "is_active": True},
                {"name": "David Okafor", "phone": "06-99887766", "email": "david@email.nl", "is_active": True},
                {"name": "Emma de Vries", "phone": "06-44556677", "email": "emma@email.nl", "is_active": True},
                {"name": "Carlos Rodriguez", "phone": "06-33445566", "email": "carlos@email.nl", "is_active": False}
            ]
            
            created_volunteers = []
            for volunteer_data in volunteers_data:
                volunteer = Volunteer.create(**volunteer_data)
                created_volunteers.append(volunteer)
            
            # Create dummy visits
            visits_data = [
                {
                    "volunteer": created_volunteers[0],
                    "address": "Cornelis Schuytlaan 25",
                    "residents_count": 4,
                    "energy_measures_taken": False,
                    "contract_duration": "doorlopend",
                    "electricity_consumption": 1428,
                    "gas_consumption": 669,
                    "monthly_amount": 180,
                    "radiator_foil_meters": 3.0,
                    "led_lamps_needed": True,
                    "mold_issues": True,
                    "moisture_issues": True
                },
                {
                    "volunteer": created_volunteers[1], 
                    "address": "Weidehof 15",
                    "residents_count": 4,
                    "energy_measures_taken": True,
                    "which_measures": "Spaar lampen",
                    "contract_duration": "doorlopend",
                    "monthly_amount": 200,
                    "e14_leds_count": 8,
                    "shower_head": True
                },
                {
                    "volunteer": created_volunteers[2],
                    "address": "Sperwerhorst 73", 
                    "residents_count": 6,
                    "energy_measures_taken": True,
                    "which_measures": "Led lampen",
                    "electricity_consumption": 1328,
                    "gas_consumption": 1328,
                    "monthly_amount": 500,
                    "radiator_foil_meters": 3.6,
                    "draft_strip_meters": 6.0,
                    "draft_issues": True
                }
            ]
            
            for visit_data in visits_data:
                Visit.create(**visit_data)
            
            logger.info(f"Created {len(created_volunteers)} volunteers and {len(visits_data)} visits")
            
    except Exception as e:
        logger.error(f"Failed to create dummy data: {e}")

# Statistics functions
def get_volunteer_stats():
    """Get volunteer statistics with safe error handling"""
    try:
        total_volunteers = Volunteer.select().count()
        active_volunteers = Volunteer.select().where(Volunteer.is_active == True).count()
        total_visits = Visit.select().count()
        
        # Get visits this month
        from datetime import datetime
        current_month = datetime.now().month
        current_year = datetime.now().year
        visits_this_month = Visit.select().where(
            (Visit.visit_date.month == current_month) & 
            (Visit.visit_date.year == current_year)
        ).count()
        
        return {
            "total_volunteers": total_volunteers,
            "active_volunteers": active_volunteers, 
            "total_visits": total_visits,
            "visits_this_month": visits_this_month
        }
        
    except Exception as e:
        logger.error(f"Failed to get volunteer stats: {e}")
        return {
            "total_volunteers": 0,
            "active_volunteers": 0,
            "total_visits": 0,
            "visits_this_month": 0
        }

def get_recent_visits(limit=10):
    """Get recent visits with safe error handling"""
    try:
        return list(Visit.select().order_by(Visit.visit_date.desc()).limit(limit))
    except Exception as e:
        logger.error(f"Failed to get recent visits: {e}")
        return []

def get_upcoming_appointments(limit=10):
    """Get upcoming appointments with safe error handling"""
    try:
        from datetime import datetime
        return list(Appointment.select().where(
            Appointment.start_time > datetime.now()
        ).order_by(Appointment.start_time).limit(limit))
    except Exception as e:
        logger.error(f"Failed to get upcoming appointments: {e}")
        return []

def search_volunteers(query):
    """Search volunteers by name or email"""
    try:
        return list(Volunteer.select().where(
            (Volunteer.name.contains(query)) | 
            (Volunteer.email.contains(query))
        ).order_by(Volunteer.name))
    except Exception as e:
        logger.error(f"Failed to search volunteers: {e}")
        return []
