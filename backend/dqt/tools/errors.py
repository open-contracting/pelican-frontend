
class GoogleDriveError(Exception):
    def __init__(self, reason):
        self.reason = reason
    
    def __str__(self):
        return 'Google Drive Error: %s' % self.reason


