from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "api_break_check.py"
SDK = "v0.2.16"
PROMPT = "Review one API endpoint migration"
POLICY = "Previously valid required fields and response meanings must remain available. A documented client change is adaptation; a removed required field or changed meaning is breaking."


def address(account):
    return "0x" + account.hex()


def deploy(vm, direct_deploy, owner):
    vm.sender = owner
    return direct_deploy(str(CONTRACT), "Community Directory API", POLICY, sdk_version=SDK)


def prepare(contract, vm, owner, consumer):
    contract.add_endpoint("profile", "GET profile returns id and display_name as required string fields for every successful request.", "GET profile returns id, display_name, and optional avatar_url while preserving existing required fields.")
    contract.open_consumer_registry()
    vm.sender = consumer
    contract.register_consumer("mobile", "Mobile Client", "The client reads id and display_name, treats avatar_url as optional, and accepts additional JSON response fields.")
    vm.sender = owner
    contract.start_endpoint_reviews()


def test_complete_map_and_validator_replay(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    prepare(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_llm(PROMPT, json.dumps({"consumer_impact_codes": "0", "contract_change_mask": "0000", "migration_note": "Existing required fields and meanings remain unchanged for the registered client."}))
    contract.assess_endpoint("profile")
    leader = direct_vm._captured_validators[-1][0]
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"consumer_impact_codes": "0", "contract_change_mask": "0000", "migration_note": "The optional addition leaves every registered consumer usage intact without adaptation."}))
    assert direct_vm.run_validator(leader_result=leader) is True
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"consumer_impact_codes": "2", "contract_change_mask": "0100", "migration_note": "This independently derived consumer impact conflicts with the leader result."}))
    assert direct_vm.run_validator(leader_result=leader) is False
    contract.open_acknowledgements()
    direct_vm.sender = direct_bob
    contract.acknowledge_endpoint("mobile", "profile", "The mobile client can adopt this endpoint without a required code change.")
    direct_vm.sender = direct_alice
    contract.finalize_migration_map()
    assert contract.get_state()["phase"] == "COMPLETE"
    assert contract.get_endpoint("profile")["classification"] == "COMPATIBLE"
    assert contract.get_endpoint("profile")["consumer_impact_codes"] == "0"
    assert contract.get_endpoint("profile")["contract_change_mask"] == "0000"


def test_owner_and_consumer_identity_are_enforced(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_owner"):
        contract.add_endpoint("x", "Old endpoint contract with required response fields and stable meanings.", "New endpoint contract with compatible response fields and stable meanings.")
    direct_vm.sender = direct_alice
    contract.add_endpoint("x", "Old endpoint contract with required response fields and stable meanings.", "New endpoint contract with compatible response fields and stable meanings.")
    contract.open_consumer_registry()
    direct_vm.sender = direct_bob
    contract.register_consumer("one", "First", "Reads the required response fields and relies on their documented meanings in the old endpoint.")
    with direct_vm.expect_revert("one_consumer_per_address"):
        contract.register_consumer("two", "Second", "Attempts to register the same address a second time with another client usage profile.")


def test_flagged_revision_and_bad_model_output_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    prepare(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_llm(PROMPT, json.dumps({"consumer_impact_codes": "2", "contract_change_mask": "1000", "migration_note": "The proposed response removes a required field used by the registered client."}))
    contract.assess_endpoint("profile")
    contract.revise_proposed_contract("profile", "GET profile returns id and display_name with their original meanings and adds optional avatar_url without removing fields.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"consumer_impact_codes": "9", "contract_change_mask": "0000", "migration_note": "This impact code is outside the closed response schema."}))
    with direct_vm.expect_revert("invalid_consumer_impact_codes"):
        contract.assess_endpoint("profile")
    assert contract.get_endpoint("profile")["state"] == "REVISED"
    assert contract.get_state()["assessed_count"] == 0
