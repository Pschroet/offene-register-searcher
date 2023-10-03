import argparse
import os
import register_searcher

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("terms", default=[], nargs="+")
    argparser.add_argument("-j", "--jsonl", required=True, action="store", default=None)
    argparser.add_argument("-a", "--allterms", action="store_true", default=False, required=False)
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
            reg_par.search(terms=args.terms, allterms=args.allterms)