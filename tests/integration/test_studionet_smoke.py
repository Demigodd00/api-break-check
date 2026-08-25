import json
from pathlib import Path
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


@pytest.mark.integration
def test_studionet_endpoint_classification(default_account, secondary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "api_break_check.py")
    deployed = ok(factory.deploy_contract_tx(args=["Community Directory API", "Preserve required fields and meanings. A documented client change is adaptation; removal or meaning changes are breaking."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    owner = factory.build_contract(address, account=default_account)
    consumer = factory.build_contract(address, account=secondary_account)
    ok(owner.add_endpoint(args=["profile", "GET profile returns required id and display_name string fields for every successful request.", "GET profile preserves id and display_name and adds optional avatar_url without changing existing meanings."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.open_consumer_registry(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(consumer.register_consumer(args=["mobile", "Mobile Client", "Reads id and display_name, accepts extra JSON fields, and ignores avatar_url when absent."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner.start_endpoint_reviews(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(owner.assess_endpoint(args=["profile"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    observed = owner.get_endpoint(args=["profile"]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)["classification"]
    assert observed in ("COMPATIBLE", "ADAPTATION", "BREAKING")
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": observed}, sort_keys=True))
