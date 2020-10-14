
class GoogleDriveError(Exception):
    def __init__(self, reason):
        self.reason = reason
    
    def __str__(self):
        return 'Google Drive Error: %s' % self.reason

class TagError(Exception):
    def __init__(self, reason, full_tag=None, template_id=None):
        self.reason = reason
        self.full_tag = full_tag
        self.template_id = template_id

    def set_reason(self, reason):
        self.reason = reason

    def set_full_tag(self, full_tag):
        self.full_tag = full_tag    

    def set_template_id(self, template_id):
        self.template_id = template_id

    def is_set(self):
        return None not in (self.reason, self.full_tag, self.template_id)

    def as_dict(self):
        return {
            'reason': self.reason,
            'full_tag': self.full_tag,
            'template_id': self.template_id,
        }
