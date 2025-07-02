"""
KoboToolbox API service for fetching visit data.
"""
import requests
import json
from datetime import datetime
from config import Config
from core.models import Visit, Volunteer
import logging

logger = logging.getLogger(__name__)

class KoboToolboxService:
    """Service for interacting with KoboToolbox API"""
    
    def __init__(self):
        self.base_url = Config.KOBO_BASE_URL
        self.api_token = Config.KOBO_API_TOKEN
        self.form_id = Config.KOBO_FORM_ID
        self.headers = {
            'Authorization': f'Token {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self):
        """Test API connection"""
        try:
            url = f"{self.base_url}/api/v2/assets/"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"KoboToolbox connection test failed: {e}")
            return False
    
    def get_form_data(self, limit=None, since_date=None):
        """Fetch form submissions from KoboToolbox"""
        try:
            url = f"{self.base_url}/api/v2/assets/{self.form_id}/data/"
            params = {}
            
            if limit:
                params['limit'] = limit
            if since_date:
                params['start'] = since_date.isoformat()
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get('results', [])
            
        except Exception as e:
            logger.error(f"Failed to fetch KoboToolbox data: {e}")
            return []
    
    def sync_visits(self):
        """Sync visits from KoboToolbox to local database"""
        try:
            submissions = self.get_form_data()
            synced_count = 0
            
            for submission in submissions:
                visit_data = self._parse_submission(submission)
                if visit_data:
                    visit, created = Visit.get_or_create(
                        kobo_submission_id=submission.get('_id'),
                        defaults=visit_data
                    )
                    if created:
                        synced_count += 1
                    elif self._should_update_visit(visit, submission):
                        self._update_visit(visit, visit_data)
                        synced_count += 1
            
            logger.info(f"Synced {synced_count} visits from KoboToolbox")
            return synced_count
            
        except Exception as e:
            logger.error(f"Visit sync failed: {e}")
            return 0
    
    def _parse_submission(self, submission):
        """Parse KoboToolbox submission into visit data"""
        try:
            # Extract data from introductie group (as per existing link generator)
            intro_data = submission.get('introductie', {})
            
            visit_data = {
                'address': intro_data.get('adres', ''),
                'visit_date': self._parse_date(intro_data.get('afspraakTijd')),
                'visit_data': submission,  # Store full submission as JSON
                'status': 'completed'
            }
            
            # Try to match volunteer by name
            volunteer_names = intro_data.get('uitvoerders', '').split(',')
            if volunteer_names and volunteer_names[0].strip():
                volunteer_name = volunteer_names[0].strip()
                volunteer = Volunteer.select().where(
                    Volunteer.name.contains(volunteer_name)
                ).first()
                if volunteer:
                    visit_data['volunteer'] = volunteer
            
            return visit_data
            
        except Exception as e:
            logger.error(f"Failed to parse submission: {e}")
            return None
    
    def _parse_date(self, date_string):
        """Parse date string from KoboToolbox"""
        if not date_string:
            return datetime.now().date()
        
        try:
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%dT%H:%M:%S']:
                try:
                    parsed = datetime.strptime(date_string, fmt)
                    return parsed.date()
                except ValueError:
                    continue
            
            # If all formats fail, return today
            return datetime.now().date()
            
        except Exception:
            return datetime.now().date()
    
    def _should_update_visit(self, visit, submission):
        """Check if visit should be updated"""
        submission_time = submission.get('_submission_time')
        if submission_time and visit.updated_at:
            try:
                sub_time = datetime.fromisoformat(submission_time.replace('Z', '+00:00'))
                return sub_time > visit.updated_at
            except Exception:
                pass
        return False
    
    def _update_visit(self, visit, visit_data):
        """Update existing visit with new data"""
        for key, value in visit_data.items():
            if key != 'volunteer' or value:  # Don't overwrite volunteer with None
                setattr(visit, key, value)
        visit.save()
