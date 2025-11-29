import pickle, pprint
with open("save.hmty", "rb") as f:
    with open("debugbin.log", "w") as f2:
        pprint.pprint(pickle.load(f), stream=f2, indent=4)