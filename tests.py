import register_searcher
import sys
import unittest
from json import dumps, JSONDecodeError
from io import StringIO

test_data_struct = {
                    "all_attributes": {
                        "_registerArt": "MUS",
                        "_registerNummer": "999999",
                        "additional_data": {
                            "AD": True,
                            "CD": True,
                            "DK": True,
                            "HD": False,
                            "SI": True,
                            "UT": True,
                            "VÖ": False
                        },
                        "federal_state": "Musterstadt",
                        "native_company_number": "Musterstadt MUS 999999",
                        "registered_office": "Musterstadt",
                        "registrar": "Musterstadt"
                    },
                    "company_number": "M1337M_MUS999999",
                    "current_status": "currently registered",
                    "jurisdiction_code": "de",
                    "name": "Muster & Co KG",
                    "officers": [
                        {
                            "name": "Max Mustermann",
                            "other_attributes": {
                                "city": "Musterstadt",
                                "firstname": "Max",
                                "flag": "vertretungsberechtigt gemäß allgemeiner Vertretungsregelung",
                                "lastname": "Mustermann"
                            },
                            "position": "Geschäftsführer",
                            "start_date": "2018-12-22",
                            "type": "person"
                        }
                    ],
                    "registered_address": "Musterstraße 1, 34346 Musterstadt.",
                    "retrieved_at": "2018-12-23T09:05:00Z"
                   }

false_data_struct = "{'single': 'quote'}"

class Test(unittest.TestCase):

    def setUp(self):
        self.in_data = StringIO(dumps(test_data_struct))
        self.false_in_data = StringIO(false_data_struct)
        #redirect the output to be able to check it, to avoid other workarounds or changing the code
        self.out = StringIO()
        sys.stdout = self.out
        #the files exists, but the the dictionary is easier to change for tests
        self.searcher = register_searcher.Register_Searcher(jsonl="test.jsonl")
        self.searcher.jsonl_db.close()
        self.searcher.jsonl_db = self.in_data

    def tearDown(self):
        #direct the output back to the default
        sys.stdout = sys.__stdout__
        self.out = None

    def testJSONFindCompanyNamePos(self):
        self.searcher.search_json(terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output

    def testJSONFindCompanyNameNeg(self):
        self.searcher.search_json(terms=["Moster"])
        output = self.out.getvalue()
        assert output == ""

    def testJSONFindCompanyNameTwoTermsPos(self):
        self.searcher.search_json(terms=["Muster", "Co KG"], allterms=True)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output

    def testJSONFindCompanyNameTwoTermsNeg(self):
        self.searcher.search_json(terms=["Muster", "GmbH"], allterms=True)
        output = self.out.getvalue()
        assert output == ""

    def testJSONFindCompanyNameTwoTermsOneInc(self):
        self.searcher.search_json(terms=["Muster", "GmbH"], allterms=False)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output

    def testJSONFindCompanyNameTwoTermsNoneInc(self):
        self.searcher.search_json(terms=["Moster", "GmbH"], allterms=False)
        output = self.out.getvalue()
        assert output == ""

    def testJSONFindCompanyNameFalseDataException(self):
        self.searcher = register_searcher.Register_Searcher(jsonl="test.jsonl", ignore_exception=False)
        self.searcher.jsonl_db.close()
        self.searcher.jsonl_db = self.false_in_data
        self.assertRaises(JSONDecodeError, self.searcher.search_json, {"terms": ["Muster"]})

    def testJSONFindCompanyNameFalseDataIgnoreException(self):
        self.searcher = register_searcher.Register_Searcher(jsonl="test.jsonl", ignore_exception=True)
        self.searcher.jsonl_db.close()
        self.searcher.jsonl_db = self.false_in_data
        self.searcher.search_json(terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" in output

    def testJSONNoTermPassed(self):
        self.searcher = register_searcher.Register_Searcher(jsonl="test.jsonl")
        self.searcher.jsonl_db.close()
        self.searcher.jsonl_db = self.false_in_data
        self.searcher.search_json(terms=[])
        output = self.out.getvalue()
        assert "Error" not in output and "No terms given" in output

    def testJSONEmptyFilePassed(self):
        self.searcher = register_searcher.Register_Searcher(jsonl="test.jsonl")
        self.searcher.jsonl_db.close()
        self.searcher.jsonl_db = StringIO("")
        self.searcher.search_json(terms=["Empty"])
        output = self.out.getvalue()
        assert "Error" not in output and "File is empty" in output

    def testJSONNoFileSet(self):
        self.searcher = register_searcher.Register_Searcher()
        self.searcher.search_json(terms=["NoFile"])
        output = self.out.getvalue()
        assert "Error" not in output and "No JSONL file set" in output

if __name__ == "__main__":
    unittest.main()
