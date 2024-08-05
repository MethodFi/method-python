from typing import TypedDict, Optional, Literal, List


EntityTypesLiterals = Literal[
    'individual',
    'c_corporation',
    's_corporation',
    'llc',
    'partnership',
    'sole_proprietorship',
    'receive_only'
]


EntityCapabilitiesLiterals = Literal[
    'payments:send',
    'payments:receive',
    'payments:limited-send',
    'data:retrieve'
]


EntityStatusesLiterals = Literal[
    'active',
    'incomplete',
    'disabled'
]


CreditScoreStatusesLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


EntityIndividualPhoneVerificationTypesLiterals = Literal[
    'method_sms',
    'method_verified',
    'sms',
    'tos'
]


CreditScoreStatusesLiterals = Literal[
    'completed',
    'in_progress',
    'pending',
    'failed'
]


CreditReportBureausLiterals = Literal[
    'experian',
    'equifax',
    'transunion'
]


EntitySensitiveFieldsLiterals = Literal[
    'first_name',
    'last_name',
    'phone',
    'phone_history',
    'email',
    'dob',
    'address',
    'address_history',
    'ssn_4',
    'ssn_6',
    'ssn_9',
    'identities'
]


class EntityIndividual(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    dob: Optional[str]


class EntityAddress(TypedDict):
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]


class EntityCorporationOwner(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    dob: Optional[str]
    address: EntityAddress


class EntityCorporation(TypedDict):
    name: Optional[str]
    dba: Optional[str]
    ein: Optional[str]
    owners: List[EntityCorporationOwner]


class EntityReceiveOnly(TypedDict):
    name: str
    phone: Optional[str]
    email: Optional[str]


class EntityKYCAddressRecordData(TypedDict):
    address: str
    city: str
    postal_code: str
    state: str
    address_term: int


class EntityIdentityType(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    dob: Optional[str]
    address: Optional[EntityKYCAddressRecordData]
    ssn: Optional[str]
