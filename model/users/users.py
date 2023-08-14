import dataclasses
import datetime


@dataclasses.dataclass
class User:
    first_name: str
    last_name: str
    email: str
    gender: str
    phone: str
    birthday: datetime.date
    subjects: str
    hobby: str
    image: str
    address: str
    state: str
    city: str
