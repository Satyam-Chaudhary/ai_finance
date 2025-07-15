from backend.llm.llm_utils import enrich_transaction

result = enrich_transaction("Uber ride to airport", 320)
print(result)
