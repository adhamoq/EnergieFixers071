"""
KoboToolbox API service for fetching visit data without pykobo dependency.
Uses direct REST API calls with requests library.
"""
import requests
import json
from datetime import datetime
from config import Config
import logging

logger = logging.getLogger(__name__)

class KoboToolboxService:
    """Service for interacting with KoboToolbox API using direct REST calls"""
    
    def __init__(self):
        self.base_url = Config.KOBO_BASE_URL
        self.api_token = Config.KOBO_API_TOKEN
        self.form_id = Config.KOBO_FORM_ID
        
        # Set up headers for API requests
        self.headers = {
            'Authorization': f'Token {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def is_configured(self):
        """Check if API token and form ID are configured"""
        return bool(self.api_token and self.form_id)
    
    def test_connection(self):
        """Test API connection"""
        if not self.is_configured():
            logger.warning("KoboToolbox API not configured - skipping connection test")
            return False
        
        try:
            # Test connection by getting user info
            url = f"{self.base_url}/api/v2/assets/"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                logger.info("KoboToolbox connection successful")
                return True
            else:
                logger.error(f"KoboToolbox connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"KoboToolbox connection test failed: {e}")
            return False
    
    def get_form_data(self, limit=None, since_date=None):
        """Fetch form submissions from KoboToolbox"""
        if not self.is_configured():
            logger.warning("KoboToolbox API not configured - returning empty data")
            return []
        
        try:
            # Build API URL for form data
            url = f"{self.base_url}/api/v2/assets/{self.form_id}/data/"
            params = {}
            
            if limit:
                params['limit'] = limit
            if since_date:
                params['start'] = since_date.isoformat()
            
            logger.info(f"Fetching data from KoboToolbox: {url}")
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            logger.info(f"Retrieved {len(results)} submissions from KoboToolbox")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch KoboToolbox data: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching KoboToolbox data: {e}")
            return []
    
    def sync_visits(self):
        """Sync visits from KoboToolbox to local database"""
        if not self.is_configured():
            logger.info("KoboToolbox not configured - skipping sync")
            return 0
        
        try:
            # Import models here to avoid circular imports
            from core.models import Visit, Volunteer
            
            submissions = self.get_form_data()
            synced_count = 0
            
            for submission in submissions:
                visit_data = self._parse_submission(submission)
                if visit_data:
                    try:
                        # Check if visit already exists
                        submission_id = submission.get('_id')
                        existing_visit = Visit.select().where(
                            Visit.kobo_submission_id == submission_id
                        ).first()
                        
                        if not existing_visit:
                            # Create new visit
                            visit = Visit.create(**visit_data)
                            synced_count += 1
                            logger.debug(f"Created new visit: {visit.address}")
                        else:
                            # Update existing visit if submission is newer
                            if self._should_update_visit(existing_visit, submission):
                                for key, value in visit_data.items():
                                    if key != 'kobo_submission_id':  # Don't update ID
                                        setattr(existing_visit, key, value)
                                existing_visit.save()
                                synced_count += 1
                                logger.debug(f"Updated visit: {existing_visit.address}")
                                
                    except Exception as e:
                        logger.error(f"Failed to save visit: {e}")
                        continue
            
            logger.info(f"Synced {synced_count} visits from KoboToolbox")
            return synced_count
            
        except Exception as e:
            logger.error(f"Visit sync failed: {e}")
            return 0
    
    def _parse_submission(self, submission):
        """Parse KoboToolbox submission into visit data"""
        try:
            # Extract data from introductie group (as per your existing structure)
            intro_data = submission.get('introductie', {})
            
            if not intro_data:
                # If no introductie group, try to get data from root level
                intro_data = submission
            
            # Parse visit data
            visit_data = {
                'kobo_submission_id': submission.get('_id'),
                'address': intro_data.get('adres', ''),
                'visit_date': self._parse_date(intro_data.get('afspraakTijd')),
                'visit_data': submission,  # Store full submission as JSON
                'status': 'completed'
            }
            
            # Try to match volunteer by name
            volunteer_names = intro_data.get('uitvoerders', '').split(',')
            if volunteer_names and volunteer_names[0].strip():
                volunteer_name = volunteer_names[0].strip()
                try:
                    from core.models import Volunteer
                    volunteer = Volunteer.select().where(
                        Volunteer.name.contains(volunteer_name)
                    ).first()
                    if volunteer:
                        visit_data['volunteer'] = volunteer
                except Exception as e:
                    logger.warning(f"Could not match volunteer '{volunteer_name}': {e}")
            
            return visit_data
            
        except Exception as e:
            logger.error(f"Failed to parse submission: {e}")
            return None
    
    def _parse_date(self, date_string):
        """Parse date string from KoboToolbox"""
        if not date_string:
            return datetime.now().date()
        
        try:
            # Try different date formats commonly used in KoboToolbox
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%fZ']:
                try:
                    parsed = datetime.strptime(str(date_string).split('T')[0], fmt.split('T')[0])
                    return parsed.date()
                except ValueError:
                    continue
            
            # If all formats fail, return today
            logger.warning(f"Could not parse date '{date_string}', using today")
            return datetime.now().date()
            
        except Exception as e:
            logger.error(f"Error parsing date '{date_string}': {e}")
            return datetime.now().date()
    
    def _should_update_visit(self, visit, submission):
        """Check if visit should be updated based on submission time"""
        submission_time = submission.get('_submission_time')
        if submission_time and visit.updated_at:
            try:
                # Parse submission time
                sub_time = datetime.fromisoformat(
                    submission_time.replace('Z', '+00:00').replace('+00:00', '')
                )
                return sub_time > visit.updated_at.replace(tzinfo=None)
            except Exception as e:
                logger.warning(f"Could not compare submission times: {e}")
        return False
    
    def get_form_info(self):
        """Get information about the form"""
        if not self.is_configured():
            return None
        
        try:
            url = f"{self.base_url}/api/v2/assets/{self.form_id}/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get form info: {e}")
            return None