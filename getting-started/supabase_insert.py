import cassiopeia as cass
from cassiopeia import Summoner, Match
from cassiopeia.data import Queue
from collections import Counter
import sys
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()
api_key = os.getenv("RIOT_API_KEY")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

client: Client = create_client(url, key)

cass.set_riot_api_key(api_key)
# cass.set_default_region("NA")
cass.apply_settings({"logging": {"print_calls": False}})


def main():
    # May not work if the, sometimes grabbing modules from the wrong place
    # if len(sys.argv) == 2:
    #     summoner_name = sys.argv[1]
    #     print_newest_match(name=summoner_name, region="NA", count=10)
    # elif len(sys.argv) == 3:
    #     summoner_name = sys.argv[1]
    #     count = int(sys.argv[2])
    #     print_newest_match(name=summoner_name, region="NA", count=count)
    # elif len(sys.argv) == 4:
    #     summoner_name = sys.argv[1]
    #     region = sys.argv[2]
    #     count = int(sys.argv[3])
    #     print_newest_match(name=summoner_name, region=region, count=count)
    # else:
    #     print("Invalid number of arguments")
    

    summoner_name = "Pobelter"
    print_newest_match(name=summoner_name, region="NA", count=30)



def print_newest_match(name: str, region: str, count: int = 10):

    # Notice how this function never makes a call to the summoner endpoint because we provide all the needed data!

    summoner = Summoner(name=name, region=region)

    # A MatchHistory is a lazy list, meaning it's elements only get loaded as-needed.

    match_history = cass.get_match_history(
        continent=summoner.region.continent,
        puuid=summoner.puuid,
        queue=Queue.aram,
        count=count,
    )
    # match_history = summoner.match_history 

    try:
        insert_summoner(summoner)
    except:
        pass

    # Load the entire match history by iterating over all its elements so that we know how long it is.
    # Unfortunately since we are iterating over the match history and accessing the summoner's champion for each match,
    # we need to know what version of the static data the champion should have. To avoid pulling many different
    # static data versions, we will instead create a {champion_id -> champion_name} mapping and just access the champion's
    # ID from the match data (which it provides directly).
    champion_id_to_name_mapping = {
        champion.id: champion.name for champion in cass.get_champions(region=region)
    }
    played_champions = Counter()
    for match in match_history:
        # insert match into the database
        try:
            insert_match(match)
        except:
            continue
        try:
            insert_summoner(summoner)
        except:
            pass
        try:
            insert_player(match, summoner, champion_id_to_name_mapping, played_champions)
        except:
            pass


    print("Length of match history:", len(match_history))

    # Print the aggregated champion results
    print(f"Top 10 champions {summoner.name} played:")
    for champion_name, count in played_champions.most_common(10):
        print(champion_name, count)
    print()

    match = match_history[0]
    print("Match ID:", match.id)

    p = match.participants[summoner]
    print(
        "\nSince the match was created from a matchref, we only know one participant:"
    )
    # print(p.summoner.name, 'playing', p.champion.name)
    print(
        p.summoner.region,
        p.summoner.account_id,
        p.summoner.name,
        p.summoner.id,
        p.champion.id,
    )



def insert_player(match, summoner, champion_id_to_name_mapping, played_champions):
    champion_id = match.participants[summoner].champion.id
    champion_name = champion_id_to_name_mapping[champion_id]
    played_champions[champion_name] += 1

    # insert into the participant table which has the following columns: summoner_id, match_id, champion, kills, deaths, assists, win
    kills = match.participants[summoner].stats.kills
    deaths = match.participants[summoner].stats.deaths
    assists = match.participants[summoner].stats.assists
    win = match.participants[summoner].stats.win
    champion = match.participants[summoner].champion.name

    penta_kills = match.participants[summoner].stats.penta_kills
    quadra_kills = match.participants[summoner].stats.quadra_kills
    triple_kills = match.participants[summoner].stats.triple_kills 
    
    spell_1_casts = match.participants[summoner].stats.spell_1_casts
    spell_2_casts = match.participants[summoner].stats.spell_2_casts
    spell_3_casts = match.participants[summoner].stats.spell_3_casts
    spell_4_casts = match.participants[summoner].stats.spell_4_casts

    summoner_spell_1_casts = match.participants[summoner].stats.summoner_spell_1_casts
    summoner_spell_2_casts = match.participants[summoner].stats.summoner_spell_2_casts
    total_cc_dealt = match.participants[summoner].stats.total_time_cc_dealt
    total_damage_dealt_to_champions = match.participants[summoner].stats.total_damage_dealt_to_champions
    total_damage_taken = match.participants[summoner].stats.total_damage_taken
    total_heal = match.participants[summoner].stats.total_heal
    total_minions_killed = match.participants[summoner].stats.total_minions_killed
    gold_earned = match.participants[summoner].stats.gold_earned
    kda = match.participants[summoner].stats.kda


    # insert summoner into the supabase database
    # Has the following columns: summoner_id, match_id, champion, kills, deaths, assists, win, penta_kills,
    # quadra_kills, triple_kills, spell_1_casts, spell_2_casts, spell_3_casts, spell_4_casts, summoner_spell_1_casts,
    # summoner_spell_2_casts, total_cc_dealt, total_damage_dealt_to_champions, total_damage_taken, total_heal,
    # total_minions_killed, gold_earned, kda
    # If it doesn't exist, insert it. If it does exist, do nothing.

    participant_data = {
        'summoner_id': summoner.id,
        'match_id': match.id,
        'champion': champion,
        'kills': kills,
        'deaths': deaths,
        'assists': assists,
        'win': win,
        'penta_kills': penta_kills,
        'quadra_kills': quadra_kills,
        'triple_kills': triple_kills,
        'spell_1_casts': spell_1_casts,
        'spell_2_casts': spell_2_casts,
        'spell_3_casts': spell_3_casts,
        'spell_4_casts': spell_4_casts,
        'summoner_spell_1_casts': summoner_spell_1_casts,
        'summoner_spell_2_casts': summoner_spell_2_casts,
        'total_cc_dealt': total_cc_dealt,
        'total_damage_dealt_to_champions': total_damage_dealt_to_champions,
        'total_damage_taken': total_damage_taken,
        'total_heal': total_heal,
        'total_minions_killed': total_minions_killed,
        'gold_earned': gold_earned,
        'kda': kda
    }


    client.table('participants').insert(participant_data).execute()
    

def insert_match(match):
        # insert match into the database
    duration = str(match.duration)
    creation = str(match.creation)
    patch = str(match.patch)
    id = match.id
    mode = match.mode.name
    

    # insert into the match table which has the following columns: match_id, duration, creation, patch, mode
    # If it doesn't exist, insert it. If it does exist, do nothing.

    match_data = {
        'match_id': id,
        'duration': duration,
        'creation': creation,
        'patch': patch,
        'mode': mode
    }

    client.table('matches').insert(match_data).execute()


def insert_summoner(summoner):
    # insert summoner into the supabase database, if it doesn't already exist
    # Has the following columns: name, region, puuid, account_id, summoner_id, summoner_level
    # If it doesn't exist, insert it. If it does exist, do nothing.

    summoner_data = {
        'name': summoner.name,
        'region': summoner.region.value,
        'puuid': summoner.puuid,
        'account_id': summoner.account_id,
        'summoner_id': summoner.id,
        'summoner_level': summoner.level
    }

    client.table('summoners').insert(summoner_data).execute()




if __name__ == "__main__":
    main()