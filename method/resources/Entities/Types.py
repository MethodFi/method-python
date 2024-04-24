from typing import TypedDict, Optional

class EntityKYCAddressRecordData(TypedDict):
    address: str
    city: str
    postal_code: str
    state: str
    address_term: int


class EntityIdentity(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    dob: Optional[str]
    address: Optional[EntityKYCAddressRecordData]
    ssn: Optional[str]
