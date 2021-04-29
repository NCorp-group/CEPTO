from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any

from functools import reduce

def pascal_to_snake_case(string: str) -> str:
    return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, string).lower()

@unique
class LightGuideEvent(Enum):
    def __int__(self):
        return self.value

    def __repr__(self) -> str:
        return pascal_to_snake_case(self.name)

    def __str__(self) -> str:
        return pascal_to_snake_case(self.name)
    
    ArrivingAtBed = 1,
    ArrivingAtToilet = 2,
    LeavingBed = 3,
    LeavingPath = 4,
    LeavingToilet = 5,
    Notification = 6

def test_pascal_to_snake_case() -> None:
    snake_case = [
        'arriving_at_bed',
        'arriving_at_toilet',
        'leaving_bed',
        'leaving_path'
        'leaving_toilet',
        'notification'
    ]
    pascal_case = [ variant.name for variant in LightGuideEvent ]
    assert [ s == p for (s, p) in zip(snake_case, pascal_case) ]


@dataclass(frozen=True)
class HEUCODevent:
    device_model: str
    device_vendor: str
    # The length of the event period - in milliseconds. for example, if a PIR sensor has detected
    # movement and it covers 90 seconds, it would be 90000 ms.
    length: int = field(default=None)
    # For how long is the sensor blind, in seconds. forexample, a PIR sensor will detect movement
    # and then send it. After this, it will be "blind" typically between 10 and 120 seconds. This is
    # important for the classification services.
    sensor_blind_duration: int = None
    # ID of the user or patient to whom this event belongs.
    patient_id: str = None
    # ID of the caregiver - e.g. one helping with a rehab or care task that is reported.
    caregiver_id: int = None


