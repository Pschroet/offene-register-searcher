import argparse
import os
import register_searcher

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("terms", default=[], nargs="+", description="terms to search for in the data")
    argparser.add_argument("-j", "--jsonl", required=True, action="store", default=None, description="file to serve as database")
    argparser.add_argument("-a", "--allterms", action="store_true", default=False, required=False, description="line must contain all search terms")
    argparser.add_argument("-s", "--stringsearch", action="store_true", default=False, required=False, description="search lines with string comparison")
    args = argparser.parse_args()
    if not hasattr(args, "jsonl") or args.jsonl is None:
        print("argument jsonl file is missing, usage")
        print(argparser.format_usage())
    else:
        if not os.path.isfile(args.jsonl):
            print("file " + str(args.jsonl) + " not found")
        else:
            print("Searching for terms " + str(args.terms) + " in database " + str(args.jsonl))
            reg_par = register_searcher.Register_Searcher(jsonl=args.jsonl)
            if args.stringsearch: reg_par.search_string(terms=args.terms, allterms=args.allterms)
            else: reg_par.search_json(terms=args.terms, allterms=args.allterms)
