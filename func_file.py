import time
import requests
import datetime
from urllib import parse
import dict_file, data_file
import os


def encode_arr(arr):
    a = []
    for name in arr:
        a.append(parse.quote(name, encoding='utf-8'))
    return a

def find_puuids(arr, info_URL, curr_API_KEY):
    a = []
    # print(arr)
    for name in arr:
        response = requests.get(info_URL.format(name, curr_API_KEY))
        time.sleep(0.05)
        # print(response.json())
        puuid = response.json()["puuid"]
        a.append(puuid)
    return a

def get_match_ids(puuid, match_id_URL, start, count, curr_API_KEY):
    response = requests.get(match_id_URL.format(puuid, start, count, curr_API_KEY))
    time.sleep(0.05)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        os.system('say "waiting"')
        print("waiting 20 secs")
        time.sleep(20)
        get_match_ids(puuid, match_id_URL, start, count, curr_API_KEY)
    else:
        os.system('say "ids error"')
        print(response)
        print("error is append - puuid is : ", puuid + "  , start : " + str(start) )
        data_file.error_arr.append("puuid, " + str(puuid) + ", start, " + str(start) +", "+ str(response.status_code))
        return None

def get_match_detail(match_id, match_detail_URL, curr_API_KEY):
    response = requests.get(match_detail_URL.format(match_id, curr_API_KEY))
    time.sleep(0.5)
    # print(response)
    # print(response.status_code)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        os.system('say "waiting"')
        print("waiting 20 secs")
        time.sleep(20)
        get_match_detail(match_id, match_detail_URL, curr_API_KEY)
    else:
        os.system('say "match error"')
        print(response)
        print("error_arr is append - match_id : ", match_id)
        data_file.error_arr.append("match_id, " + str(match_id) + ", status_code, " + str(response.status_code))
        return None
    

def check_datetime(num):
    date = datetime.datetime.fromtimestamp(num).strftime('%Y')
    return date == 2020

def find_zilbbugs(participants, name_dict):
    a = []
    for participant in participants:
        if participant in name_dict:
            a.append(participant)
            print("found match with ", name_dict[participant])
    return a

def cal_kda(numerator, denominator):
    if denominator == 0:
        return numerator
    return numerator / denominator

def analyze_match(match_detail, puuid_zilbbugs, puuid_bob):
    
    game_duration = match_detail["info"]["gameDuration"]/1000/60

    for participant_dict in match_detail["info"]["participants"]:
        if participant_dict["puuid"] == puuid_bob:
            bob_win = participant_dict["win"]
            # print("bob_win:", bob_win)
            bob_damge_per_m = participant_dict["totalDamageDealtToChampions"] / game_duration
            bob_numerator = participant_dict["assists"] + participant_dict["kills"]
            bob_denominator = participant_dict["deaths"]
            bob_kda = cal_kda(bob_numerator, bob_denominator)
            break
    
    for puuid_zilbbug in puuid_zilbbugs:
        for participant_dict in match_detail["info"]["participants"]:
            if participant_dict["puuid"] == puuid_zilbbug:
                zilbbug_win = participant_dict["win"]
                # print("zilbbug_win : ", zilbbug_win)
                zilbbug_damge_per_m = participant_dict["totalDamageDealtToChampions"] / game_duration
                zilbbug_numerator = participant_dict["assists"] + participant_dict["kills"]
                zilbbug_denominator = participant_dict["deaths"]
                zilbbug_kda = cal_kda(zilbbug_numerator, zilbbug_denominator)

                ref_dict = dict_file.m_dict[puuid_zilbbug]
                ref_dict["count"] += 1
                if bob_win == zilbbug_win:
                    ref_dict["same_team_sum_kda"] += zilbbug_kda
                    ref_dict["same_team_sum_damage_per_m"] += zilbbug_damge_per_m    
                    ref_dict["same_team_sum_kda_bob"] += bob_kda
                    ref_dict["same_team_sum_damage_per_m_bob"] += bob_damge_per_m
                    if bob_win == True:
                        ref_dict["same_team_win"] += 1
                    else:
                        ref_dict["same_team_lose"] += 1
                else:
                    ref_dict["diff_team_sum_kda"] += zilbbug_kda
                    ref_dict["diff_team_sum_damage_per_m"] += zilbbug_damge_per_m    
                    ref_dict["diff_team_sum_kda_bob"] += bob_kda
                    ref_dict["diff_team_sum_damage_per_m_bob"] += bob_damge_per_m
                    if zilbbug_win == True:
                        ref_dict["diff_team_win"] += 1
                    else:
                        ref_dict["diff_team_lose"] += 1
                break

    return 0