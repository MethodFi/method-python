from typing import TypedDict, Optional, List

from method.resource import MethodResponse, Resource, ResourceListOpts, ResourceStatusLiterals
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Accounts.Types import AccountLiabilityTypesLiterals, AccountLiabilityAutoLoan, \
    AccountLiabilityCreditCard, AccountLiabilityMortgage, AccountLiabilityStudentLoans, AccountLiabilityPersonalLoan, \
    AccountLiabilityCollection, AccountLiabilityCreditBuilder, AccountLiabilityLoan, AccountLiabilityInsurance, \
    AccountLiabilityMedical, AccountLiabilityUtility, AccountUpdateSourceLiterals


class AccountUpdate(TypedDict):
    id: str
    status: ResourceStatusLiterals
    account_id: str
    source: Optional[AccountUpdateSourceLiterals]
    type: AccountLiabilityTypesLiterals
    auto_loan: Optional[AccountLiabilityAutoLoan]
    credit_card: Optional[AccountLiabilityCreditCard]
    collection: Optional[AccountLiabilityCollection]
    mortgage: Optional[AccountLiabilityMortgage]
    personal_loan: Optional[AccountLiabilityPersonalLoan]
    student_loans: Optional[AccountLiabilityStudentLoans]
    credit_builder: Optional[AccountLiabilityCreditBuilder]
    loan: Optional[AccountLiabilityLoan]
    insurance: Optional[AccountLiabilityInsurance]
    medical: Optional[AccountLiabilityMedical]
    utility: Optional[AccountLiabilityUtility]
    data_as_of: Optional[str]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountUpdatesResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountUpdatesResource, self).__init__(config.add_path('updates'))

    def retrieve(self, upt_id: str) -> MethodResponse[AccountUpdate]:
        return super(AccountUpdatesResource, self)._get_with_id(upt_id)

    def list(self, params: Optional[ResourceListOpts] = None) -> MethodResponse[List[AccountUpdate]]:
        return super(AccountUpdatesResource, self)._list(params)

    def create(self) -> MethodResponse[AccountUpdate]:
        return super(AccountUpdatesResource, self)._create({})
