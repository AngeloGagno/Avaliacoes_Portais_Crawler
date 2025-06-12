from datetime import datetime

class AirbnbParser:
    def __init__(self, accommodations: list):
        self.accommodation = accommodations

    def reference(self):
        return self.accommodation.get('reference')
    
    def name(self):
        return self.accommodation.get('name')
    
    def channel(self):
        return self.accommodation.get('channel').replace('bk_','')
    
    def status_local(self):
        return self.accommodation['status']['local']['enabled']

    def account_id(self):
        config = self.accommodation.get('config')
        if config:
            if config.get('accountId'):
                return config.get('accountId')['value']
            return None
    
    def listing_id(self):
        config = self.accommodation.get('config')
        if config:
            if config.get('listingId'):
                listing_id = config.get('listingId')['value']
                return f'airbnb.com.br/rooms/{listing_id}'
            return None
        
    def status_publishment(self):
        status = self.accommodation['status'].get('publishment','inactive')
        if status == 'inactive':
            return 'inactive' 

        if status.get('error'):
            return 'error'
        
        if status.get('active') is True:
            return 'active'
        
        if status.get('pending') is True:
            return 'pending'
        
        return 'inactive'

    def alerts(self):
        return self.accommodation['alerts'].get('count',0)
    
    def sync_alerts(self):
        sync_alerts = self.accommodation['alerts']['syncAlerts']
        if sync_alerts['has'] is True:
            return ", ".join(item["type"] for item in sync_alerts["value"])
        return ""
            
    def rejection_alerts(self):
        rejection_alert = self.accommodation['alerts']['rejectionAlerts']
        return rejection_alert['has']

    def warnings_alerts(self):
        warnings_alerts = self.accommodation['alerts']['warnings']
        if warnings_alerts['has'] is True:
            return ", ".join(item["type"] for item in warnings_alerts["value"])
        return ""


    def generic_parser_reviews(self, attribute: str, field: str = 'value'):
        scores = self.accommodation.get('scores', [])
        for item in scores:
            if item.get('type') == attribute:
                return item.get(field, None)
        return None

    
    def parse_accommodation(self):   
        parsed = {
                'accommodation_id':self.reference(),
                'accommodation_name':self.name(),
                'airbnb_account_id':self.account_id(),
                'accommodation_link':self.listing_id(),
                'channel_name':self.channel(),
                'local_status':self.status_local(),
                'publishment_status':self.status_publishment(),
                'alert':self.alerts(),
                'sync_alert':self.sync_alerts(),
                'rejection_alert':self.rejection_alerts(),
                'warning_alert':self.warnings_alerts(),
                'review_count':self.generic_parser_reviews('rating','count'),
                'review_value':self.generic_parser_reviews('rating'),
                'cleanliness_value':self.generic_parser_reviews('cleanliness'),
                'location_value':self.generic_parser_reviews('location'),
                'truthfulness_value':self.generic_parser_reviews('accuracy'),
                'checkin_value':self.generic_parser_reviews('checkin'),
                'communication_value':self.generic_parser_reviews('communication'),
                'scrap_data': datetime.now().date().isoformat()
            }
            
        return parsed