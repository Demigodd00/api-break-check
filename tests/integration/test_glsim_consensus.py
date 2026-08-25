from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Review one API endpoint migration"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"classification": "COMPATIBLE", "migration_note": "Existing required fields and meanings remain unchanged for the registered client."})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_endpoint_migration_flow():
    owner_account, consumer_account = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "api_break_check.py")
    deployed = factory.deploy_contract_tx(args=["Community Directory API", "Previously valid fields and meanings must remain. Documented client work is adaptation; removed fields or changed meanings are breaking."], account=owner_account, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    contract_address = extract_contract_address(deployed)
    owner = factory.build_contract(contract_address, account=owner_account)
    consumer = factory.build_contract(contract_address, account=consumer_account)
    ok(owner.add_endpoint(args=["profile", "GET profile returns id and display_name as required string fields for every successful request.", "GET profile preserves id and display_name and adds optional avatar_url without changing existing meanings."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.open_consumer_registry(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(consumer.register_consumer(args=["mobile", "Mobile Client", "Reads id and display_name, permits additional JSON fields, and ignores optional avatar_url when absent."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.start_endpoint_reviews(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.assess_endpoint(args=["profile"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.open_acknowledgements(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(consumer.acknowledge_endpoint(args=["mobile", "profile", "The registered mobile usage remains ready without a required migration change."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.finalize_migration_map(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert owner.get_state(args=[]).call()["phase"] == "COMPLETE"
