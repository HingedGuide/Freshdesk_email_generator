import os

class Config:
    FRESHDESK_API_KEY = os.getenv('FRESHDESK_API_KEY', 'your_api_key')
    FRESHDESK_DOMAIN = 'your freshdesk domain (company.freshdesk.com)'
