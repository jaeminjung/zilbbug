import data_file

bobs = ["강자석", "강찬밥", "maengsdog"]
zilbbugs = ["고수달", "고구마유시", "cree", "H1GHR MUSlC", "모하쉔", "암살럭스", "카시스 페델리안", "입털면6완두콩", "게이온"]
name_dict = {}
for i, puuid in enumerate(data_file.puuid_zilbbugs):
    name_dict[puuid] = zilbbugs[i]
m_dict = {}

for zilbbug in data_file.puuid_zilbbugs:
    m_dict[zilbbug] = {}
    m_dict[zilbbug]["count"] = 0
    m_dict[zilbbug]["same_team_win"] = 0
    m_dict[zilbbug]["same_team_lose"] = 0
    m_dict[zilbbug]["same_team_sum_kda"] = 0
    m_dict[zilbbug]["same_team_sum_damage_per_m"] = 0
    m_dict[zilbbug]["same_team_sum_kda_bob"] = 0
    m_dict[zilbbug]["same_team_sum_damage_per_m_bob"] = 0
    
    m_dict[zilbbug]["diff_team_win"] = 0
    m_dict[zilbbug]["diff_team_lose"] = 0
    m_dict[zilbbug]["diff_team_sum_kda"] = 0
    m_dict[zilbbug]["diff_team_sum_damage_per_m"] = 0
    m_dict[zilbbug]["diff_team_sum_kda_bob"] = 0
    m_dict[zilbbug]["diff_team_sum_damage_per_m_bob"] = 0
    
def print_dict():
    for puuid in m_dict:
        print("------", name_dict[puuid], "------")
        print("total game : ", m_dict[puuid]["count"])
        print("same_team_win : ", m_dict[puuid]["same_team_win"])
        print("same_team_lose : ", m_dict[puuid]["same_team_lose"])
        
        same_team_count = m_dict[puuid]["same_team_win"] + m_dict[puuid]["same_team_lose"]
        if same_team_count == 0: same_team_count = 1
        print("same_team_sum_kda : ", m_dict[puuid]["same_team_sum_kda"] / same_team_count)
        print("same_team_sum_damage_per_m : ", m_dict[puuid]["same_team_sum_damage_per_m"] / same_team_count)
        print("bob_kda : ", m_dict[puuid]["same_team_sum_kda_bob"] / same_team_count)
        print("bob_damage_per_m : ", m_dict[puuid]["same_team_sum_damage_per_m_bob"] / same_team_count)

        print("diff_team_win : ", m_dict[puuid]["diff_team_win"])
        print("diff_team_lose : ", m_dict[puuid]["diff_team_lose"])

        diff_team_count = m_dict[puuid]["diff_team_win"] + m_dict[puuid]["diff_team_lose"]
        if diff_team_count == 0: diff_team_count = 1
        print("diff_team_sum_kda : ", m_dict[puuid]["diff_team_sum_kda"] / diff_team_count)
        print("diff_team_sum_damage_per_m : ", m_dict[puuid]["diff_team_sum_damage_per_m"] / diff_team_count)
        print("bob_kda : ", m_dict[puuid]["diff_team_sum_kda_bob"] / diff_team_count)
        print("bob_damage_per_m : ", m_dict[puuid]["diff_team_sum_damage_per_m_bob"] / diff_team_count)
