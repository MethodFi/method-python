from typing import TypedDict, Optional, List

from method.resource import Resource, ResourceListOpts, ResourceStatusLiterals
from method.configuration import Configuration
from method.errors import ResourceError
from method.resources.Accounts.Account import AccountLiabilityTypesLiterals, AccountLiabilityAutoLoan, AccountLiabilityCollection, \
    AccountLiabilityCreditCard, AccountLiabilityCreditBuilder, AccountLiabilityMortgage, AccountLiabilityStudentLoan, AccountLiabilityStudentLoans, \
    AccountLiabilityInsurance, AccountLiabilityLoan, AccountLiabilityMedical, AccountLiabilityPersonalLoan, AccountLiabilityUtility


class AccountUpdate(TypedDict):
    id: str
    status: ResourceStatusLiterals
    account_id: str
    type: AccountLiabilityTypesLiterals
    auto_loan: Optional[AccountLiabilityAutoLoan]
    credit_card: Optional[AccountLiabilityCreditCard]
    mortgage: Optional[AccountLiabilityMortgage]
    personal_loan: Optional[AccountLiabilityPersonalLoan]
    student_loans: Optional[AccountLiabilityStudentLoans]
    error: Optional[ResourceError]
    created_at: str
    updated_at: str


class AccountUpdatesResource(Resource):
    def __init__(self, config: Configuration):
        super(AccountUpdatesResource, self).__init__(config.add_path('updates'))

    def retrieve(self, upt_id: str) -> AccountUpdate:
        return super(AccountUpdatesResource, self)._get_with_id(upt_id)

    def list(self, params: ResourceListOpts) -> List[AccountUpdate]:
        return super(AccountUpdatesResource, self)._list(params)

    def create(self) -> AccountUpdate:
        return super(AccountUpdatesResource, self)._create({})