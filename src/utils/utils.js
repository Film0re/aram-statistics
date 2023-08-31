const statPropertyToLabel = {
  'champion_name': 'Champion Name',
  'games_played': 'Games Played',
  'wins': 'Wins',
  'win_percent': 'Win Rate',
  'avg_kills': 'Average Kills',
  'avg_assists': 'Average Assists',
  'avg_deaths': 'Average Deaths',
  'avg_kda': 'Average KDA',
  'avg_total_minions_killed': 'Average CS',
  'avg_spell_1_casts': 'Average Q Casts',
  'avg_spell_2_casts': 'Average W Casts',
  'avg_spell_3_casts': 'Average E Casts',
  'avg_spell_4_casts': 'Average Ult Casts',
  'avg_summoner_spell_1_casts': 'Average Summoner Spell 1 Casts',
  'avg_summoner_spell_2_casts': 'Average Summoner Spell 2 Casts',
  'avg_total_cc_dealt': 'Average Total CC Dealt',
  'avg_total_damage_dealt_to_champions': 'Average Total Damage Dealt to Champions',
  'avg_total_damage_taken': 'Average Total Damage Taken',
  'avg_total_heal': 'Average Total Heal',
  'avg_gold_earned': 'Average Gold Earned'
};

export function convertStatPropertyToLabel(statProperty) {
  return statPropertyToLabel[statProperty] || statProperty;
}
