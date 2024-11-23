from enum import Enum

class UserRolesEnum(str, Enum):
    passenger = "passenger"
    driver = "driver"

class BookingStatusEnum(str, Enum):
    requested = "requested"
    approved = "approved"
    rejected = "rejected"
    completed = "completed"
    canceled = "canceled" 