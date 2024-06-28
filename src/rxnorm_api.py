import requests
from typing import Dict, Any, Optional

class RxNormAPI:
    BASE_URL = "https://rxnav.nlm.nih.gov/REST"

    @staticmethod
    def _make_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the RxNorm API"""
        url = f"{RxNormAPI.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_rxcui(cls, drug_name: str) -> Optional[str]:
        """Get the RxCUI for a given drug name"""
        endpoint = "rxcui.json"
        params = {"name": drug_name}
        data = cls._make_request(endpoint, params)
        id_group = data.get("idGroup", {})
        rxnorm_id = id_group.get("rxnormId")
        return rxnorm_id[0] if rxnorm_id else None

    @classmethod
    def get_drug_properties(cls, rxcui: str) -> Dict[str, Any]:
        """Get drug properties for a given RxCUI"""
        endpoint = f"rxcui/{rxcui}/allProperties.json"
        params = {"prop": "all"}
        data = cls._make_request(endpoint, params)
        return data.get("propConceptGroup", {}).get("propConcept", [])

    @classmethod
    def get_drug_interactions(cls, rxcui: str) -> Dict[str, Any]:
        """Get drug interactions for a given RxCUI"""
        endpoint = f"interaction/interaction.json"
        params = {"rxcui": rxcui}
        return cls._make_request(endpoint, params)

    @classmethod
    def get_drug_names(cls, rxcui: str) -> Dict[str, Any]:
        """Get all names for a given RxCUI"""
        endpoint = f"rxcui/{rxcui}/allnames"
        return cls._make_request(endpoint)
