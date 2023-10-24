import os
import json
#TODO: make cli arg that can specify this
input_fname = None
json_fname = "intermediates.json"
#from ./win32/dump_versioned_json.exe
data_json_dumper_binaries = "./binaries/dump_versioned_json.exe"
data_json_maker_binaries = "./binaries/make_versioned_json.exe"

#TODO: add thing that converts the thing back

TARGET_SLOTS = 120

def delete_file(fname : str):
    os.system("del " + fname)

def main():
    #handle args here

    for root, dirs, files in os.walk("./"):
        for fn in files:
            if ".player" in fn:
                input_fname = fn
                break
    if input_fname == None:
        print("No player data found.")
        return
    
    #convert to json with binaries
    #"./binaries/dump_versioned_json.exe in.player intermediates.json" 
    #cmd shell doesnt like this command idk why
    os.system(f"powershell.exe \"{data_json_dumper_binaries} {input_fname} {json_fname} \"")
    player_data = None
    with open(json_fname, "r") as f:
        player_data = json.loads(f.read())

    empty_bag = [None] * TARGET_SLOTS

    #should be a REFERENCE to item bags
    item_bags : dict = player_data["content"]["inventory"]["itemBags"]
    #first pad bags
    for v in item_bags.values():
        pad_length = TARGET_SLOTS - len(v)
        padding = [None] * pad_length
        v += padding
    
    #add new bags
    item_bags["armoryBag"] = empty_bag
    item_bags["farmBag"] = empty_bag
    item_bags["objectBag2"] = empty_bag
    item_bags["hobbyBag"] = empty_bag
    item_bags["vehicleBag"] = empty_bag
    
    delete_file(json_fname)
    #dump back 2 json
    with open(json_fname, "w+") as f:
        f.write(json.dumps(player_data, indent=2))
    #convert
    os.system(f"powershell.exe \"{data_json_maker_binaries} {json_fname} {input_fname}\"")
    #delete intermediates
    delete_file(json_fname)
    #exit
    print("Player converted.")
    return





if __name__ == "__main__":
    main()