def parse_results(results_for_team):
    xx = [str(results_for_team[result])
          for result in ['wins', 'ties', 'losses']]
    return '/'.join(xx)

def process(teams, matrix):
    average = {'home': {'wins': 0, 'ties': 0, 'losses': 0},
               'away': {'wins': 0, 'ties': 0, 'losses': 0}}

    results = [{'home': {'wins': 0, 'ties': 0, 'losses': 0},
                'away': {'wins': 0, 'ties': 0, 'losses': 0}}
               for team in teams]

    for i, line in enumerate(matrix):
        for j, cell in enumerate(line):
            if i != j:
                calc = cmp(*cell) + 1
                home_result = ['wins', 'ties', 'losses'][2 - calc]
                away_result = ['wins', 'ties', 'losses'][calc]
                average['home'][home_result] += 1
                average['away'][away_result] += 1
                results[i]['home'][home_result] += 1
                results[j]['away'][away_result] += 1
    
    points = [((3 * (result['home']['wins'] + result['away']['wins']) +
                result['home']['ties'] + result['away']['ties']),
               teams[i])
              for i, result in enumerate(results)]
    
    for place in ['home', 'away']:
        for result in ['losses', 'ties', 'wins']:
            average[place][result] /= 20.0
    
    for k, v in average['home'].iteritems():
        print '%s %.2f %.2f%%' % (k, v, v / 0.19)
    
    print '---'

    for point, team in reversed(sorted(points)):
        i = teams.index(team)
        home = parse_results(results[i]['home'])
        away = parse_results(results[i]['away'])
        print '%s: %s - %s, %s' % (team, point, home, away)
