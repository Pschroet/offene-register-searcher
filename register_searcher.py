import json
import os

class Register_Searcher(object):

    def __init__(self, jsonl=None, ignore_exception=False):
        self.jsonl = jsonl
        self.jsonl_db = open(self.jsonl, mode="r")
        self.read_line = 1
        self.ignore_exception = ignore_exception

    def search(self, terms=[], allterms=False):
        for entry in self.jsonl_db:
            try:
                allterms_found = []
                entry_data = json.loads(entry)
                for t in terms:
                    #defined this way, because of argument allterms
                    #see condition for print after the loop
                    term_found = []
                    if "name" in entry_data and t in entry_data["name"]:
                        term_found.append(True)
                    else:
                        term_found.append(False)
                    if "officers" in entry_data:
                        for o in entry_data["officers"]:
                            if "name" in o and t in o["name"]:
                                term_found.append(True)
                            else:
                                term_found.append(False)
                            if "other_attributes" in o:
                                for officer_attribute in o["other_attributes"]:
                                    if isinstance(o["other_attributes"][officer_attribute], str) and t in o["other_attributes"][officer_attribute]:
                                        term_found.append(True)
                                    else:
                                        term_found.append(False)
                    if True in term_found:
                        if allterms:
                            allterms_found.append(True)
                        else:
                            print("Found term '" + str(t) + "' in line " + str(self.read_line) + ": " + str(entry_data))
                    elif allterms:
                        allterms_found.append(False)
                if allterms and False not in allterms_found:
                    print("Found all terms " + str(terms) + " in line " + str(self.read_line) + ": " + str(entry_data))
                self.read_line += 1
            except Exception as e:
                print("Error in data in line " + str(self.read_line) + ":" + os.linesep + "-> " + str(entry))
                if self.ignore_exception:
                    print(str(e))
                else:
                    raise