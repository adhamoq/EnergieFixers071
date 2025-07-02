"""
Calendly API service for fetching appointment data.
"""
import requests
from datetime import datetime, timedelta
from config import Config
from core.models import Appointment
import logging

logger = logging.getLogger(__name__)

class CalendlyService:
    """Service for interacting with Calendly API"""
    
    def __init__(self):
        self.api_token = Config.CALENDLY_API_TOKEN
        self.user_uri = Config.CALENDLY_USER_URI
        self.base_url = "https://api.calendly.com"
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self):
        """Test API connection"""
        try:
            url = f"{self.base_url}/users/me"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Calendly connection test failed: {e}")
            return False
    
    def get_scheduled_events(self, days_ahead=30):
        """Fetch scheduled events from Calendly"""
        try:
            min_start_time = datetime.now().isoformat()
            max_start_time = (datetime.now() + timedelta(days=days_ahead)).isoformat()
            
            url = f"{self.base_url}/scheduled_events"
            params = {
                'user': self.user_uri,
                'min_start_time': min_start_time,
                'max_start_time': max_start_time,
                'count': 100
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get('collection', [])
            
        except Exception as e:
            logger.error(f"Failed to fetch Calendly events: {e}")
            return []
    
    def get_event_invitees(self, event_uuid):
        """Get invitees for a specific event"""
        try:
            url = f"{self.base_url}/scheduled_events/{event_uuid}/invitees"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('collection', [])
            
        except Exception as e:
            logger.error(f"Failed to fetch event invitees: {e}")
            return []
    
    def sync_appointments(self):
        """Sync appointments from Calendly to local database"""
        try:
            events = self.get_scheduled_events()
            synced_count = 0
            
            for event in events:
                appointment_data = self._parse_event(event)
                if appointment_data:
                    appointment, created = Appointment.get_or_create(
                        calendly_event_uuid=event.get('uuid'),
                        defaults=appointment_data
                    )
                    if created:
                        synced_count += 1
                        # Get invitee information
                        self._update_appointment_invitees(appointment, event.get('uuid'))
            
            logger.info(f"Synced {synced_count} appointments from Calendly")
            return synced_count
            
        except Exception as e:
            logger.error(f"Appointment sync failed: {e}")
            return 0
    
    def _parse_event(self, event):
        """Parse Calendly event into appointment data"""
        try:
            appointment_data = {
                'calendly_uri': event.get('uri'),
                'event_name': event.get('name', 'Appointment'),
                'start_time': self._parse_datetime(event.get('start_time')),
                'end_time': self._parse_datetime(event.get('end_time')),
                'status': event.get('status', 'scheduled').lower(),
                'location': event.get('location', {}).get('location'),
                'meeting_url': event.get('location', {}).get('join_url'),
                'calendly_data': event
            }
            
            # Determine meeting type
            location_type = event.get('location', {}).get('type', '')
            if 'phone' in location_type.lower():
                appointment_data['meeting_type'] = 'phone'
            elif 'zoom' in location_type.lower() or 'meet' in location_type.lower():
                appointment_data['meeting_type'] = 'online'
            else:
                appointment_data['meeting_type'] = 'in_person'
            
            return appointment_data
            
        except Exception as e:
            logger.error(f"Failed to parse Calendly event: {e}")
            return None
    
    def _parse_datetime(self, datetime_string):
        """Parse datetime string from Calendly"""
        if not datetime_string:
            return None
        
        try:
            # Calendly uses ISO format
            return datetime.fromisoformat(datetime_string.replace('Z', '+00:00'))
        except Exception as e:
            logger.error(f"Failed to parse datetime: {datetime_string}, {e}")
            return None
    
    def _update_appointment_invitees(self, appointment, event_uuid):
        """Update appointment with invitee information"""
        try:
            invitees = self.get_event_invitees(event_uuid)
            if invitees:
                invitee = invitees[0]  # Take first invitee
                appointment.invitee_name = invitee.get('name')
                appointment.invitee_email = invitee.get('email')
                appointment.save()
        except Exception as e:
            logger.error(f"Failed to update appointment invitees: {e}")
