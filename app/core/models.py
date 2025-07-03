"""
Enhanced database models for EnergieFixers071 application with comprehensive visit data.
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
    """Enhanced volunteer model"""
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
    """Comprehensive visit model based on KoboToolbox form structure"""
    
    # Basic Information
    volunteer = ForeignKeyField(Volunteer, backref='visits', null=True)
    volunteer_2 = ForeignKeyField(Volunteer, backref='secondary_visits', null=True)  # Second volunteer
    address = CharField(max_length=200)
    visit_date = DateField(default=date.today)
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)
    appointment_time = CharField(max_length=20, null=True)
    
    # Resident Information
    residents_count = IntegerField(default=1, help_text="Number of people living at address")
    energy_measures_taken = BooleanField(default=False, help_text="Energy saving measures already taken")
    which_measures = TextField(null=True, help_text="Which measures were taken")
    ventilation_checked = BooleanField(default=False, help_text="Ventilation checked")
    
    # Energy Contract Information
    energy_usage_checked = BooleanField(default=False, help_text="Energy usage checked via website/app")
    contract_duration = CharField(max_length=50, null=True, help_text="Duration of energy contract")
    electricity_consumption = FloatField(null=True, help_text="Annual electricity consumption (kWh)")
    gas_consumption = FloatField(null=True, help_text="Annual gas consumption (m³)")
    monthly_amount = FloatField(null=True, help_text="Monthly payment amount (€)")
    energy_bill_concerns = BooleanField(default=False, help_text="Major concerns about energy bill")
    
    # Materials and Interventions
    radiator_foil_meters = FloatField(default=0, help_text="Radiator foil in meters")
    radiator_fan_needed = BooleanField(default=False, help_text="Radiator fan needed")
    small_power_strip_needed = BooleanField(default=False, help_text="Small power strip needed")
    led_lamps_needed = BooleanField(default=False, help_text="LED lamps needed")
    e14_leds_count = IntegerField(default=0, help_text="Number of E14 LEDs needed")
    e27_leds_count = IntegerField(default=0, help_text="Number of E27 LEDs needed")
    draft_strip_meters = FloatField(default=0, help_text="Draft strip in meters")
    door_draft_band = BooleanField(default=False, help_text="Door draft band needed")
    door_closers = BooleanField(default=False, help_text="Door closers needed")
    door_closer_spring = BooleanField(default=False, help_text="Door closer spring needed")
    
    # Door Assessment
    all_interior_doors_present = BooleanField(default=True, help_text="All interior doors present")
    missing_doors = TextField(null=True, help_text="Which doors are missing")
    missing_doors_living_room = CharField(max_length=100, null=True)
    missing_doors_kitchen = CharField(max_length=100, null=True)
    missing_doors_bedroom = CharField(max_length=100, null=True)
    missing_doors_hallway = CharField(max_length=100, null=True)
    
    # Bathroom Equipment
    shower_timer = BooleanField(default=False, help_text="Shower timer installed/needed")
    shower_head = BooleanField(default=False, help_text="Shower head replaced/needed")
    
    # Heating System (CV)
    cv_website_mentioned = BooleanField(default=False, help_text="CV website (zetmop60.nl) mentioned")
    current_cv_temperature = IntegerField(null=True, help_text="Current CV temperature")
    cv_temperature_lowered_to = IntegerField(null=True, help_text="CV temperature lowered to")
    cv_water_pressure_under_1_bar = BooleanField(default=False, help_text="CV water pressure under 1 bar")
    tap_comfort_off = BooleanField(default=False, help_text="Tap comfort turned off")
    large_power_strip_needed = BooleanField(default=False, help_text="Large power strip needed")
    
    # Problems and Issues
    problems_with = TextField(null=True, help_text="General problems mentioned")
    mold_issues = BooleanField(default=False, help_text="Mold issues present")
    moisture_issues = BooleanField(default=False, help_text="Moisture issues present")
    draft_issues = BooleanField(default=False, help_text="Draft issues present")
    problem_rooms_description = TextField(null=True, help_text="Which rooms have problems")
    hygrometer_needed = BooleanField(default=False, help_text="Hygrometer needed")
    
    # Community Building
    community_building = TextField(null=True, help_text="Community building responses")
    knows_potential_fixers = BooleanField(default=False, help_text="Knows people who could become fixers")
    wants_to_help = BooleanField(default=False, help_text="Wants to help as volunteer")
    tell_neighbors = BooleanField(default=False, help_text="Will tell neighbors about project")
    
    # Additional Information
    old_refrigerator = BooleanField(default=False, help_text="Has old refrigerator")
    share_info_with_housing_corp = BooleanField(default=False, help_text="Can share info with housing corporation")
    keep_updated_on_results = BooleanField(default=False, help_text="Wants to be kept updated on results")
    other_remarks = TextField(null=True, help_text="Other remarks")
    
    # Contact and Photos
    resident_email = CharField(max_length=100, null=True, help_text="Resident email address")
    photos = TextField(null=True, help_text="Photo filenames")
    photos_url = TextField(null=True, help_text="Photo URLs")
    
    # Complaint flags (derived from problems)
    mold_complaint = BooleanField(default=False)
    draft_complaint = BooleanField(default=False)
    
    # KoboToolbox Integration
    kobo_submission_id = CharField(max_length=50, null=True, unique=True)
    kobo_uuid = CharField(max_length=100, null=True)
    submission_time = DateTimeField(null=True)
    visit_data = TextField(null=True)  # JSON storage for full form data
    
    # Metadata
    status = CharField(max_length=20, default='completed')
    notes = TextField(null=True, help_text="Internal notes about the visit")
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
    """Create comprehensive dummy data including visits based on CSV data"""
    try:
        # Only create dummy data if no volunteers exist
        if Volunteer.select().count() == 0:
            logger.info("Creating comprehensive dummy data...")
            
            # Create volunteers based on the CSV data
            volunteers_data = [
                {"name": "Sarah van der Berg", "phone": "06-12345678", "email": "sarah@energiefixers.nl", "is_active": True, "skills": "Insulation, General repairs"},
                {"name": "Adham Al Moqdad", "phone": "06-87654321", "email": "adham@energiefixers.nl", "is_active": True, "skills": "Electronics, LED installation"},
                {"name": "Patricia Santos", "phone": "06-11223344", "email": "patricia@energiefixers.nl", "is_active": True, "skills": "Ventilation, Energy advice"},
                {"name": "Mounsif Hassan", "phone": "06-55667788", "email": "mounsif@energiefixers.nl", "is_active": True, "skills": "Plumbing, Heating systems"},
                {"name": "Hussein Ahmed", "phone": "06-99887766", "email": "hussein@energiefixers.nl", "is_active": True, "skills": "Electrical work, Insulation"},
                {"name": "Willem de Jong", "phone": "06-44556677", "email": "willem@energiefixers.nl", "is_active": True, "skills": "Door installation, Draft sealing"},
                {"name": "Ronald Jansen", "phone": "06-33445566", "email": "ronald@energiefixers.nl", "is_active": True, "skills": "HVAC, Energy audits"},
                {"name": "Maarten Visser", "phone": "06-22334455", "email": "maarten@energiefixers.nl", "is_active": True, "skills": "Insulation, General maintenance"},
                {"name": "Edidia Okafor", "phone": "06-77889900", "email": "edidia@energiefixers.nl", "is_active": True, "skills": "Energy consultation, Electronics"},
                {"name": "Hans Mueller", "phone": "06-66778899", "email": "hans@energiefixers.nl", "is_active": False, "skills": "Electrical, Heating"},
                {"name": "Haben Tesfaye", "phone": "06-55667788", "email": "haben@energiefixers.nl", "is_active": True, "skills": "Plumbing, Energy systems"},
                {"name": "Maurits van Dam", "phone": "06-88990011", "email": "maurits@energiefixers.nl", "is_active": True, "skills": "Insulation, Home improvement"},
                {"name": "Igor Petrov", "phone": "06-99001122", "email": "igor@energiefixers.nl", "is_active": True, "skills": "Electronics, Smart home"},
                {"name": "Franz Weber", "phone": "06-11223344", "email": "franz@energiefixers.nl", "is_active": True, "skills": "Energy audits, Consulting"},
                {"name": "Ram Sharma", "phone": "06-22334455", "email": "ram@energiefixers.nl", "is_active": True, "skills": "Electrical, Solar systems"},
                {"name": "Harold Johnson", "phone": "06-33445566", "email": "harold@energiefixers.nl", "is_active": True, "skills": "General repairs, Energy advice"},
                {"name": "Willem S. de Boer", "phone": "06-44556677", "email": "willems@energiefixers.nl", "is_active": True, "skills": "Heating, Insulation"},
                {"name": "Wael Al-Ahmad", "phone": "06-55667788", "email": "wael@energiefixers.nl", "is_active": True, "skills": "Energy systems, Consulting"}
            ]
            
            created_volunteers = []
            for volunteer_data in volunteers_data:
                volunteer = Volunteer.create(**volunteer_data)
                created_volunteers.append(volunteer)
            
            # Create comprehensive visits based on the CSV data
            visit_data_samples = [
                {
                    "volunteer": next(v for v in created_volunteers if "Sarah" in v.name),
                    "volunteer_2": next(v for v in created_volunteers if "Adham" in v.name),
                    "address": "Cornelis Schuytlaan 25, Amsterdam",
                    "visit_date": date(2025, 4, 5),
                    "appointment_time": "10:00",
                    "residents_count": 4,
                    "energy_measures_taken": False,
                    "ventilation_checked": False,
                    "contract_duration": "doorlopend",
                    "electricity_consumption": 1428,
                    "gas_consumption": 669,
                    "monthly_amount": 180,
                    "energy_bill_concerns": False,
                    "radiator_foil_meters": 3.0,
                    "radiator_fan_needed": True,
                    "small_power_strip_needed": True,
                    "led_lamps_needed": False,
                    "draft_strip_meters": 6.0,
                    "all_interior_doors_present": True,
                    "shower_timer": True,
                    "shower_head": True,
                    "current_cv_temperature": 80,
                    "cv_temperature_lowered_to": 60,
                    "cv_water_pressure_under_1_bar": True,
                    "tap_comfort_off": True,
                    "large_power_strip_needed": True,
                    "problems_with": "schimmel vocht",
                    "mold_issues": True,
                    "moisture_issues": True,
                    "draft_issues": False,
                    "problem_rooms_description": "Woonkamer",
                    "hygrometer_needed": True,
                    "tell_neighbors": True,
                    "share_info_with_housing_corp": True,
                    "resident_email": "roma87flex@gmail.com",
                    "other_remarks": "Wonen al 8 jaar, schimmel begon 2 jaar geleden",
                    "mold_complaint": True,
                    "draft_complaint": True
                },
                {
                    "volunteer": next(v for v in created_volunteers if "Patricia" in v.name),
                    "volunteer_2": next(v for v in created_volunteers if "Mounsif" in v.name),
                    "address": "Weidehof 15, Utrecht",
                    "visit_date": date(2025, 4, 5),
                    "appointment_time": "10:00",
                    "residents_count": 4,
                    "energy_measures_taken": True,
                    "which_measures": "Spaar lampen",
                    "ventilation_checked": True,
                    "contract_duration": "doorlopend",
                    "electricity_consumption": 0,
                    "gas_consumption": 0,
                    "monthly_amount": 200,
                    "energy_bill_concerns": True,
                    "radiator_foil_meters": 0,
                    "led_lamps_needed": True,
                    "e14_leds_count": 8,
                    "current_cv_temperature": 70,
                    "cv_temperature_lowered_to": 60,
                    "cv_water_pressure_under_1_bar": True,
                    "tap_comfort_off": True,
                    "large_power_strip_needed": True,
                    "tell_neighbors": True,
                    "share_info_with_housing_corp": True,
                    "resident_email": "zorg.sriri@outlook.com",
                    "other_remarks": "Maakt badkamer schoon af en toe door schimmel opbouw. Badkamer ventilator wrkt niet. Huurt via portaal."
                },
                {
                    "volunteer": next(v for v in created_volunteers if "Willem" in v.name and "de Jong" in v.name),
                    "volunteer_2": next(v for v in created_volunteers if "Hussein" in v.name),
                    "address": "Sperwerhorst 73, Den Haag",
                    "visit_date": date(2025, 4, 5),
                    "appointment_time": "12:45",
                    "residents_count": 6,
                    "energy_measures_taken": True,
                    "which_measures": "Led lampen",
                    "ventilation_checked": True,
                    "contract_duration": "doorlopend",
                    "electricity_consumption": 1328,
                    "gas_consumption": 1328,
                    "monthly_amount": 500,
                    "energy_bill_concerns": True,
                    "radiator_foil_meters": 3.6,
                    "radiator_fan_needed": True,
                    "led_lamps_needed": True,
                    "draft_strip_meters": 6.0,
                    "all_interior_doors_present": True,
                    "shower_timer": True,
                    "shower_head": True,
                    "current_cv_temperature": 80,
                    "cv_temperature_lowered_to": 60,
                    "tap_comfort_off": True,
                    "large_power_strip_needed": True,
                    "problems_with": "tocht",
                    "draft_issues": True,
                    "problem_rooms_description": "Woon kamer. Slaapkamer",
                    "share_info_with_housing_corp": True,
                    "resident_email": "meshalalaskar97@gmail.com",
                    "other_remarks": "Kamers van buiten hebben veel lekaage waardoor tocht komt.",
                    "draft_complaint": True
                },
                {
                    "volunteer": next(v for v in created_volunteers if "Hussein" in v.name),
                    "volunteer_2": next(v for v in created_volunteers if "Edidia" in v.name),
                    "address": "Gerrit Kasteinstraat 45, Rotterdam",
                    "visit_date": date(2025, 4, 12),
                    "appointment_time": "10:00",
                    "residents_count": 1,
                    "energy_measures_taken": False,
                    "ventilation_checked": True,
                    "contract_duration": "1 jaar",
                    "electricity_consumption": 1596,
                    "gas_consumption": 746,
                    "monthly_amount": 109,
                    "energy_bill_concerns": False,
                    "radiator_foil_meters": 3.4,
                    "radiator_fan_needed": True,
                    "led_lamps_needed": True,
                    "e14_leds_count": 1,
                    "e27_leds_count": 3,
                    "all_interior_doors_present": True,
                    "shower_head": True,
                    "current_cv_temperature": 70,
                    "cv_temperature_lowered_to": 60,
                    "tap_comfort_off": True,
                    "share_info_with_housing_corp": True
                },
                {
                    "volunteer": next(v for v in created_volunteers if "Ronald" in v.name),
                    "volunteer_2": next(v for v in created_volunteers if "Maarten" in v.name),
                    "address": "Gerrit Kasteinstraat 4, Rotterdam",
                    "visit_date": date(2025, 4, 12),
                    "appointment_time": "10:00",
                    "residents_count": 5,
                    "energy_measures_taken": True,
                    "which_measures": "Mech. ventilatie. Led lampen",
                    "ventilation_checked": True,
                    "contract_duration": "doorlopend contract",
                    "electricity_consumption": 2500,
                    "gas_consumption": 1950,
                    "monthly_amount": 310,
                    "energy_bill_concerns": False,
                    "radiator_foil_meters": 4.8,
                    "radiator_fan_needed": True,
                    "all_interior_doors_present": True,
                    "shower_timer": True,
                    "shower_head": True,
                    "current_cv_temperature": 80,
                    "cv_temperature_lowered_to": 60,
                    "tap_comfort_off": True,
                    "large_power_strip_needed": True,
                    "problems_with": "Schimmel",
                    "mold_issues": True,
                    "problem_rooms_description": "Keuken, woonkamer",
                    "hygrometer_needed": True,
                    "share_info_with_housing_corp": True,
                    "mold_complaint": True
                }
            ]
            
            for visit_data in visit_data_samples:
                Visit.create(**visit_data)
            
            # Create additional random visits for other volunteers
            import random
            addresses = [
                "Beethovenlaan 167, Almere", "Beethovenlaan 95, Almere", "Mulderstraat 19, Tilburg",
                "Hoflaan 100, Eindhoven", "Gerrit Kasteinstraat 8, Rotterdam", "Gerrit Kasteinstraat 20, Rotterdam",
                "Gerrit Kasteinstraat 28, Rotterdam", "Gerrit Kasteinstraat 72, Rotterdam", "Vijf Meilaan 115, Utrecht",
                "Brahmslaan 241, Den Haag", "Bartokstraat 46, Amsterdam"
            ]
            
            for i in range(15):  # Create 15 additional visits
                primary_vol = random.choice(created_volunteers[:12])  # Active volunteers only
                secondary_vol = random.choice([v for v in created_volunteers[:12] if v != primary_vol])
                
                Visit.create(
                    volunteer=primary_vol,
                    volunteer_2=secondary_vol,
                    address=random.choice(addresses),
                    visit_date=date(2025, random.randint(1, 6), random.randint(1, 28)),
                    residents_count=random.randint(1, 6),
                    energy_measures_taken=random.choice([True, False]),
                    electricity_consumption=random.randint(800, 3000),
                    gas_consumption=random.randint(300, 2000),
                    monthly_amount=random.randint(80, 400),
                    radiator_foil_meters=round(random.uniform(0, 10), 1),
                    led_lamps_needed=random.choice([True, False]),
                    e14_leds_count=random.randint(0, 10),
                    e27_leds_count=random.randint(0, 10),
                    current_cv_temperature=random.randint(65, 85),
                    cv_temperature_lowered_to=random.randint(55, 70),
                    mold_issues=random.choice([True, False]),
                    moisture_issues=random.choice([True, False]),
                    draft_issues=random.choice([True, False])
                )
            
            logger.info(f"Created {len(created_volunteers)} volunteers and {Visit.select().count()} visits with comprehensive data")
            
    except Exception as e:
        logger.error(f"Failed to create dummy data: {e}")

# Statistics functions with enhanced calculations
def get_volunteer_stats():
    """Get comprehensive volunteer statistics"""
    try:
        total_volunteers = Volunteer.select().count()
        active_volunteers = Volunteer.select().where(Volunteer.is_active == True).count()
        total_visits = Visit.select().count()
        
        # Get visits this month
        current_month = datetime.now().month
        current_year = datetime.now().year
        visits_this_month = Visit.select().where(
            (Visit.visit_date.month == current_month) & 
            (Visit.visit_date.year == current_year)
        ).count()
        
        # Calculate additional stats
        avg_visits_per_volunteer = round(total_visits / max(total_volunteers, 1), 1)
        volunteers_with_visits = Volunteer.select().where(
            Volunteer.id.in_(Visit.select(Visit.volunteer).distinct())
        ).count()
        
        return {
            "total_volunteers": total_volunteers,
            "active_volunteers": active_volunteers,
            "total_visits": total_visits,
            "visits_this_month": visits_this_month,
            "avg_visits_per_volunteer": avg_visits_per_volunteer,
            "volunteers_with_visits": volunteers_with_visits
        }
        
    except Exception as e:
        logger.error(f"Failed to get volunteer stats: {e}")
        return {
            "total_volunteers": 0,
            "active_volunteers": 0,
            "total_visits": 0,
            "visits_this_month": 0,
            "avg_visits_per_volunteer": 0,
            "volunteers_with_visits": 0
        }

def get_recent_visits(limit=10):
    """Get recent visits with enhanced data"""
    try:
        return list(Visit.select().order_by(Visit.visit_date.desc()).limit(limit))
    except Exception as e:
        logger.error(f"Failed to get recent visits: {e}")
        return []

def get_upcoming_appointments(limit=10):
    """Get upcoming appointments"""
    try:
        return list(Appointment.select().where(
            Appointment.start_time > datetime.now()
        ).order_by(Appointment.start_time).limit(limit))
    except Exception as e:
        logger.error(f"Failed to get upcoming appointments: {e}")
        return []

def search_volunteers(query):
    """Enhanced volunteer search"""
    try:
        return list(Volunteer.select().where(
            (Volunteer.name.contains(query)) | 
            (Volunteer.email.contains(query)) |
            (Volunteer.phone.contains(query)) |
            (Volunteer.skills.contains(query))
        ).order_by(Volunteer.name))
    except Exception as e:
        logger.error(f"Failed to search volunteers: {e}")
        return []
