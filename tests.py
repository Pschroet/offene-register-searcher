import os
import sys
import unittest
from io import StringIO
from json import dumps, JSONDecodeError
from register_searcher import Compare_Mode, Register_Searcher

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
                        "federal_state": "Musterstadtland",
                        "native_company_number": "Musterstadt MUS 999999",
                        "registered_office": "Musterstadt 1",
                        "registrar": "Meisterstadt"
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
        self.searcher = Register_Searcher(jsonl="test.jsonl")
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = self.in_data

    def tearDown(self):
        #direct the output back to the default
        sys.stdout = sys.__stdout__
        self.out = None

    def testJSONFindCompanyNamePos(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testJSONFindCompanyNameNeg(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Moster"])
        output = self.out.getvalue()
        assert output == ""

    def testJSONFindCompanyNameTwoTermsPos(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Muster", "Co KG"], allterms=True)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found all terms" in output

    def testJSONFindCompanyNameTwoTermsNeg(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Muster", "GmbH"], allterms=True)
        output = self.out.getvalue()
        assert output == ""

    def testJSONFindCompanyNameTwoTermsOneInc(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Muster", "GmbH"], allterms=False)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testJSONFindCompanyNameTwoTermsNoneInc(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Moster", "GmbH"], allterms=False)
        output = self.out.getvalue()
        assert output == ""

    def testJSONFindCompanyNameFalseDataException(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl", ignore_exception=False)
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = self.false_in_data
        with self.assertRaises(JSONDecodeError):
            self.searcher.search(compare_mode=Compare_Mode.json, terms=["Muster"])

    def testJSONFindCompanyNameFalseDataIgnoreException(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl", ignore_exception=True)
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = self.false_in_data
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" in output

    def testJSONNoTermPassed(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl")
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = self.false_in_data
        self.searcher.search(compare_mode=Compare_Mode.json, terms=[])
        output = self.out.getvalue()
        assert "Error" not in output and "No terms given" in output

    def testJSONEmptyFilePassed(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl", ignore_exception=True)
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = StringIO("")
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Empty"])
        output = self.out.getvalue()
        assert "Error" not in output and output == ""

    def testJSONNoFileSet(self):
        self.searcher = Register_Searcher()
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["NoFile"])
        output = self.out.getvalue()
        assert "Error" not in output and "File not set" in output

    def testJSONFindRegisteredAddress(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Musterstraße 1"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testJSONFindFederalState(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Musterstadtland"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testJSONFindRegisteredOffice(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Musterstadt 1"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testJSONFindRegistrar(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Meisterstadt"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testJSONFindCurrentStatus(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["registered"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testStringFindCompanyNamePos(self):
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testStringFindCompanyNameNeg(self):
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Moster"])
        output = self.out.getvalue()
        assert output == ""

    def testStringFindCompanyNameTwoTermsPos(self):
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Muster", "Co KG"], allterms=True)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found all terms" in output

    def testStringFindCompanyNameTwoTermsNeg(self):
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Muster", "GmbH"], allterms=True)
        output = self.out.getvalue()
        assert output == ""

    def testStringFindCompanyNameTwoTermsOneInc(self):
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Muster", "GmbH"], allterms=False)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testStringFindCompanyNameTwoTermsNoneInc(self):
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Moster", "GmbH"], allterms=False)
        output = self.out.getvalue()
        assert output == ""

    def testStringFindCompanyNameFalseDataIgnoreException(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl", ignore_exception=True)
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = self.false_in_data
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Muster"])
        output = self.out.getvalue()
        assert output == ""

    def testStringNoTermPassed(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl")
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = self.false_in_data
        self.searcher.search(compare_mode=Compare_Mode.string, terms=[])
        output = self.out.getvalue()
        assert "Error" not in output and "No terms given" in output

    def testStringEmptyFilePassed(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl")
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = StringIO("")
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Empty"])
        output = self.out.getvalue()
        assert "Error" not in output and output == ""

    def testStringNoFileSet(self):
        self.searcher = Register_Searcher()
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["NoFile"])
        output = self.out.getvalue()
        assert "Error" not in output and "File not set" in output

    def testRegexFindCompanyNamePos(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testRegexFindCompanyNameNeg(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Moster"])
        output = self.out.getvalue()
        assert output == ""

    def testRegexFindCompanyNameTwoTermsPos(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Muster", "Co KG"], allterms=True)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found all terms" in output

    def testRegexFindCompanyNameTwoTermsNeg(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Muster", "GmbH"], allterms=True)
        output = self.out.getvalue()
        assert output == ""

    def testRegexFindCompanyNameTwoTermsOneInc(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Muster", "GmbH"], allterms=False)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testRegexFindCompanyNameTwoTermsNoneInc(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Moster", "GmbH"], allterms=False)
        output = self.out.getvalue()
        assert output == ""

    def testRegexFindCompanyNameFalseDataIgnoreException(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl", ignore_exception=True)
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = self.false_in_data
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Muster"])
        output = self.out.getvalue()
        assert "Error" not in output and output == ""

    def testRegexNoTermPassed(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl")
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = self.false_in_data
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=[])
        output = self.out.getvalue()
        assert "Error" not in output and "No terms given" in output

    def testRegexEmptyFilePassed(self):
        self.searcher = Register_Searcher(jsonl="test.jsonl")
        self.searcher._jsonl_db.close()
        self.searcher._jsonl_db = StringIO("")
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Empty"])
        output = self.out.getvalue()
        assert "Error" not in output and output == ""

    def testRegexNoFileSet(self):
        self.searcher = Register_Searcher()
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["NoFile"])
        output = self.out.getvalue()
        assert "Error" not in output and "File not set" in output

    def testRegexFindCompanyNameIgnoreCasePos(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["MUster"], ignore_case=True)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testRegexFindCompanyNameCaseSensativeNeg(self):
        #data contains 'Meisterstadt', which should not be found, if case is not ignored
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["MEster"])
        output = self.out.getvalue()
        assert output == ""

    def testRegexFindCompanyNameCaseInsensativeNeg(self):
        #data contains 'Meisterstadt', which should not be found, if case is not ignored
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["mEister"], ignore_case=True)
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testRegexFindCityActualRegex(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["M.*stadt"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testRegexFindCityActualRegexCaseSensitive(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["M1337m.*MUS999999"], ignore_case=False)
        output = self.out.getvalue()
        assert output == ""

    def testFileSetNone(self):
        self.searcher = Register_Searcher(jsonl=None)
        assert self.searcher._jsonl_db is None

    def testFileSetNotExisting(self):
        self.searcher = Register_Searcher(jsonl="")
        assert self.searcher._jsonl_db is None

    def testFileSetEmpty(self):
        self.searcher = Register_Searcher(jsonl="empty.jsonl")
        assert self.searcher._jsonl_db is None

    def testOffsetJSONZero(self):
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testOffsetJSONTooFar(self):
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testOffsetJSONPos(self):
        self.searcher = Register_Searcher(jsonl="multiline.jsonl", offset=1)
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Muster"])
        output = self.out.getvalue()
        assert "Error" not in output and output == ""

    def testOffsetJSONNeg(self):
        self.searcher = Register_Searcher(jsonl="multiline.jsonl", offset=1)
        self.searcher.search(compare_mode=Compare_Mode.string, terms=["Monster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testOffsetStringZero(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testOffsetStringTooFar(self):
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testOffsetStringPos(self):
        self.searcher = Register_Searcher(jsonl="multiline.jsonl", offset=1)
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Muster"])
        output = self.out.getvalue()
        assert "Error" not in output and output == ""

    def testOffsetStringNeg(self):
        self.searcher = Register_Searcher(jsonl="multiline.jsonl", offset=1)
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Monster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testOffsetRegexZero(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testOffsetRegexTooFar(self):
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Muster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testOffsetRegexPos(self):
        self.searcher = Register_Searcher(jsonl="multiline.jsonl", offset=1)
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Muster"])
        output = self.out.getvalue()
        assert "Error" not in output and output == ""

    def testOffsetRegexNeg(self):
        self.searcher = Register_Searcher(jsonl="multiline.jsonl", offset=1)
        self.searcher.search(compare_mode=Compare_Mode.regex, terms=["Monster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

    def testEndStringPos(self):
        self.searcher = Register_Searcher(jsonl="multiline.jsonl", offset=1, end=1)
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Monster"])
        output = self.out.getvalue()
        assert "Error" not in output and "Found term" not in output and output == ""

    def testEndStringNeg(self):
        self.searcher = Register_Searcher(jsonl="multiline.jsonl", offset=1, end=0)
        self.searcher.search(compare_mode=Compare_Mode.json, terms=["Monster"])
        output = self.out.getvalue()
        assert output != "" and "Error" not in output and "Found term" in output

if __name__ == "__main__":
    unittest.main()
