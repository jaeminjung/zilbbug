# import requests
import time
import json
import os
import data_file, func_file, dict_file


curr_API_KEY = data_file.curr_API_KEY

print("---Start---")
start_time = time.time()

# zilbbug1 = "고수달"
# zilbbug2 = "고구마유시"

# summoner info
# get puuid each summoner
info_URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"

bobs = ["강자석", "강찬밥", "maengsdog"]
puuid_bobs = data_file.puuid_bobs
# puuid_bobs = func_file.find_puuids(func_file.encode_arr(bobs), info_URL, curr_API_KEY)

zilbbugs = ["고수달", "고구마유시", "cree", "H1GHR MUSlC", "모하쉔", "암살럭스", "카시스 페델리안", "입털면6완두콩", "게이온"]
puuid_zilbbugs = data_file.puuid_zilbbugs
# puuid_zilbbugs = func_file.find_puuids(func_file.encode_arr(zilbbugs), info_URL, curr_API_KEY)

#---------------------------------
# get match ids
# need bob's puuids
start = 0
count = 10
match_id_URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?start={}&count={}&api_key={}"
# response = requests.get(match_id_URL.format(puuid, 0, 10, curr_API_KEY))
# response = requests.get(match_id_URL.format(puuid, 10, 20, curr_API_KEY))

# bob_puuid = 'fU0LxUK_TCnuFTMKtW9JBiGQENyRsuewod-mfQYoTgUoqrvKGz0ExXkLaJMJ_jl6rU1Mq3w2M1VoKg'
# match_ids = func_file.get_match_ids(bob_puuid, match_id_URL, start, count, curr_API_KEY)
# print(match_ids)


# -------------------------------
# get match detail by match_id

# ex_match_id = match_ids[0]
match_detail_URL = "https://asia.api.riotgames.com/lol/match/v5/matches/{}?api_key={}"
# match_detail = func_file.get_match_detail(ex_match_id, match_detail_URL, curr_API_KEY)

# print(data_file.ex_match_detail.keys())
# print(data_file.ex_match_detail["info"]["queueId"])
# print(data_file.ex_match_detail["info"]["gameCreation"]//1000) # check datetime 
# print(data_file.ex_match_detail["info"]["gameDuration"]/1000/60) # check draw - > erase less than 8 minutes
# print(data_file.ex_match_detail["metadata"]["participants"]) # check zilbbugs
match_count = 0
zilbbug_game = 0
num_zilbbug = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
match_id_dict = {}

for puuid_bob in puuid_bobs:
    date_flag = True
    while date_flag:
        match_ids = func_file.get_match_ids(puuid_bob, match_id_URL, start, count, curr_API_KEY)
        if match_ids != None:
            print("match_ids : ", match_ids)
            if len(match_ids) == 0:
                    date_flag = False
            for match_id in match_ids:
                print("match_id : ", match_id)
                if match_id in match_id_dict:  # check duplicate match_id
                    os.system('say "duplicate"')
                    time.sleep(2)
                    continue
                else:
                    match_id_dict[match_id] = 1

                match_detail = func_file.get_match_detail(match_id, match_detail_URL, curr_API_KEY)
                if match_detail == None:
                    continue
                if func_file.check_datetime(match_detail["info"]["gameCreation"]//1000): # check game created in 2021
                    os.system('say "datetime datetime"')
                    print("datetime in 2020 game found")
                    time.sleep(2)
                    date_flag = False
                    continue
                if match_detail["info"]["queueId"] != 420: # check 5vs5 solo rank
                    continue
                if match_detail["info"]["gameDuration"]/1000/60 < 8: # ignore draw game
                    continue

                puuid_zilbbugs = func_file.find_zilbbugs(match_detail["metadata"]["participants"], dict_file.name_dict)
                if puuid_zilbbugs:
                    func_file.analyze_match(match_detail, puuid_zilbbugs, puuid_bob)
                    num_zilbbug[len(puuid_zilbbugs)] += 1
                    zilbbug_game += 1
                print("match_count : ", match_count)
                match_count += 1
                print(num_zilbbug)
            
        else: # if match_ids is None
            continue
        print("start : ", start, " count : ", count)
        start += count

    start = 0
    count= 10
    print("next bob id")
    os.system('say "next bob"')
    time.sleep(2)

dict_file.print_dict()
print("total lookup match : ", match_count)
print("zilbbug game : ", zilbbug_game)
print(num_zilbbug)
print("---End---")
end_time = time.time()
print("time tooked : ", (end_time - start_time) / 60)

with open("error.txt", "w") as f:
    json.dump(data_file.error_arr, f)