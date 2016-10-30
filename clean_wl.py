import json,glob,re
from datetime import date,datetime,timedelta
from pprint import pprint
start_date = "1/1/1970"
start_date = datetime.strptime(start_date, "%d/%m/%Y")
debug = False
white_list = "whitelist.json"
wl_cache = {}

with open(white_list) as json_row:
    player_list = json.load(json_row)
    for player in player_list:
        wl_cache[player["uuid"]] = player["name"]




player_list= glob.glob('stats\*.json')
deleted_players = {}
clean_list = []

for player in player_list:
    with open(player) as json_data:
        data = json.load(json_data)
        uuid = re.search("(stats\\\)(.*)\.json",player)
        uuid = uuid.group(2)
        ms_f_joined = data["ftbl.stat.first_joined"]["progress"]
        ms_f_joined = start_date + timedelta(milliseconds=ms_f_joined)
        ms_l_seen = data["ftbl.stat.last_seen"]["progress"]
        ms_l_seen = start_date + timedelta(milliseconds=ms_l_seen)
        played_time = data["stat.playOneMinute"]

        
        been_offline_for = (ms_l_seen + timedelta(days=10)) < datetime.today()
        if((played_time < 600) or been_offline_for):
            if(uuid in wl_cache): 
                deleted_players[uuid] = wl_cache[uuid]
                if(debug):
                    print(wl_cache[uuid])
                    print("\t playedtime =\t"+str(played_time))
                    print("\t joined =\t"+str(ms_f_joined))
                    print("\t last seen =\t"+str(ms_l_seen))
        else:
            if(uuid in wl_cache):
                clean_list.append({'uuid':uuid, 'name':wl_cache[uuid]})

with open('clean_whitelist.json', 'w') as outfile:
    #json_data = json.dumps(clean_list, sort_keys=True,indent=2, separators=(',', ': '))
    json.dump(clean_list ,outfile, indent=2)
with open('removed_players.json', 'w') as outfile:
    json.dump(deleted_players,outfile,indent=2)
print(str(len(deleted_players)) +" players has been removed" )
                
#ftbl.stat.first_joined
#ftbl.stat.last_seen
