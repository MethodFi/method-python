from typing import TypedDict, Optional, List

from method.resource import MethodResponse, Resource, ResourceListOpts
from method.configuration import Configuration

from method.resources.Entities.Types import EntityKYCAddressRecordData, EntityIdentityType


class EntitySensitive(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    phone_history: List[str]
    email: Optional[str]
    dob: Optional[str]
    address: Optional[EntityKYCAddressRecordData]
    address_history: List[EntityKYCAddressRecordData]
    ssn_4: Optional[str]
    ssn_6: Optional[str]
    ssn_9: Optional[str]
    identities: List[EntityIdentityType]


class EntitySensitiveResource(Resource):
    def __init__(self, config: Configuration):
        super(EntitySensitiveResource, self).__init__(config.add_path('sensitive'))

    def retrieve(self) -> MethodResponse[EntitySensitive]:
        return super(EntitySensitiveResource, self)._get()
    
    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[EntitySensitive]]:
        return super(EntitySensitiveResource, self)._list(params)
