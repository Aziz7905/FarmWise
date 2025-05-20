from enum import Enum

class SubscriptionTier(Enum):
    FREE = 'Free'
    STANDARD = 'Standard'
    PREMIUM = 'Premium'

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]
