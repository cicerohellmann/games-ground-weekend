"""raw.json (parsed official programme pages) -> data JSON for the page's <script id="data">."""
import json, sys, re
raw = json.load(open(sys.argv[1], encoding='utf-8'))
LIKE = {
 'Crafting Com Workshops': 'making things with your hands: costumes, 3D printing, make-up, sewing, wigs, foam',
 'Soldering Workshop': 'trying electronics for the first time; total beginners welcome, just drop by',
 'Welcome 2 Nerdistan': 'meeting the Nerdistan Arcade Bash crew and hearing what is on all weekend',
 'Japan Game Show Special!': 'Japanese games (SEGA and others), live gameplay and joining in from the audience',
 'Germany’s Biggest Beyblade Tournament': 'Beyblade battles, big tournaments and prizes; sign up online first',
 'Kleine Spiele, große Fragen: Entwirf ein Minispiel mit Botschaft': 'young people (11 to 15) who want to invent a small game about something that matters',
 'Super Smash Bros. Melee Tournament': 'fast fighting games and a loud crowd, as a player or a fan',
 'Warm up with Kiri playing Warhammer Blood Bowl': 'Warhammer and strategy games, watching a streamer play live',
 'Panel: The Power of Emerging Creators in Gaming': 'streaming and content creation, and how small creators work with game studios',
 'FLINTA Magic the Gathering Workshop': 'Magic: The Gathering in a FLINTA space, learning or playing cards',
 'New Game Announcement!': 'strategy games and being first to see a new reveal',
 'Playable for Everyone': 'accessible games and designing games everyone can play',
 'Another New Game Announcement!': 'strategy games and being first to see a new reveal',
 "Let's Talk Cosplay!": 'starting cosplay or taking it further, tools, community and the business side',
 'Warhammer Blood Bowl Panel': 'Warhammer, fantasy football and chaotic strategy games',
 'Cosplay Contest: Extravaganza': 'cosplay, costumes and cheering on makers on a big stage',
 'Warhammer Blood Bowl Tournament!': 'watching or following a Blood Bowl strategy tournament through the afternoon',
 'Game Audio Workshop': 'sound, music and making a game scene sound alive; no experience needed',
 'Warhammer Blood Bowl Tournament: Semifinals': 'watching tense strategy matches with live commentary',
 'Retromania': 'old-school games and nostalgia; you can play on the big screen',
 "Olaf's Saturday Night Quiz Show": 'pub quizzes and game trivia with friends; one phone per team',
 'Stranger Bits with 0r4 and Daimon Chip': 'chiptune, 8-bit music and live electronic sets',
 'Beyblade Finals': 'the big Beyblade showdown after a full day of battles',
 'Always HIGHscore feat. Imp powered by GoJoe': 'high-score challenges and streamer shows',
 'GG Girls: A Gaming Drag Show': 'drag, dance, costumes and nerdy stage numbers',
 'Electric Social Afterparty': 'keeping the night going: arcade games, pinball, drinks and a DJ',
 'Warm up with VulcanHD': 'real-time strategy (Broken Arrow) and watching a streamer play live',
 'Hangover Hangout': 'a slow, chatty Sunday start with the community',
 'Panel on Radio Commander': 'strategy games about command and decision-making',
 'The Solo Voice Choir': 'game music, singing and how a solo artist got into game audio',
 'Low Budget Cosplay': 'cosplay on a small budget with everyday and recycled materials',
 'Panel on Veil of Ashes': 'steampunk war machines and tactical strategy games',
 'Jeder Hund hat einen Grund: Löse den Fall, versteh das Warum': 'kids (6 to 10) with a parent who like detective games and stories',
 'Dungeons & Dragons Liveshow': 'Dungeons & Dragons and watching a live pen & paper adventure',
 'My Chat Became My Home. Then It Got Ugly.': 'starting to stream, and how creators deal with hate and set boundaries',
 'Richie & Tristan Show: The Multiverse': 'kids who want to play friendly PS5 battles on stage',
 'Panel on Broken Arrow': 'modern warfare and large real-time tactics games',
 'Your First Steps into Cosplay: A Beginner’s Guide': 'wanting to try cosplay and not knowing where to start',
 'Broken Arrow Tournament: Semifinals': 'watching a real-time strategy tournament live',
 'Make Your Own Card & Board Game': 'kids and grown-ups who want to invent a card or board game together; drop in',
 'Live at Games Ground: Primalavera!': 'game soundtracks sung live, musical theatre voices',
 'Baumann Bergmann Pokinsson': 'quirky indie rock and live bands',
 'D&D Open Play with the Quest Community Dungeon Masters': 'playing D&D at a table yourself, beginner or veteran',
 'Cosplay Catwalk': 'showing off your own costume on stage, or watching others do it',
 'Recap Reality': 'talking over the weekend with the community, honestly and casually',
 'Kann man das noch reparieren?': 'fixing your own controller or console and knowing what is safe to repair',
 'EndGegner Jazz': 'game soundtracks played as jazz and rock by a live band',
}
AGES = {
 'Kleine Spiele, große Fragen: Entwirf ein Minispiel mit Botschaft': 'Ages 11–15',
 'Jeder Hund hat einen Grund: Löse den Fall, versteh das Warum': 'Ages 6–10, with parents',
 'Make Your Own Card & Board Game': 'All ages',
}
WHERE = {
 'Relic Stage': 'Main building · right of the Main Entry',
 'Cage Stage': 'Haus 3 · ground level, left end',
 'The Forge': 'Haus 3 · ground level, right end',
 'Intraprenör': 'Haus 3 · 1st floor, left',
 'Portal Stage': 'Haus 3 · 1st floor, right end',
 'Lichthof': 'Not on this map: ask at the info point (Main Entry)',
 'Loft Breakout': 'Not on this map: ask at the info point (Main Entry)',
 'Electric Social': 'Off-site: Electric Social Berlin, Grunerstraße 13, 10179 Berlin',
}
def hm24(t):
    m = re.fullmatch(r'(\d+):(\d\d) (am|pm)', t)
    h = int(m.group(1)) % 12 + (12 if m.group(3) == 'pm' else 0)
    return '%02d:%s' % (h, m.group(2))
LANG = {'DE': 'German only', 'EN': 'English', 'DE / EN': 'German & English'}
out = []
for key, date, pre in (('sat', '2026-11-07', 2611070), ('sun', '2026-11-08', 2611080)):
    for i, e in enumerate(raw[key]):
        room, note = e['stage'], ''
        if e['title'] == 'Electric Social Afterparty':
            room = 'Electric Social'
        if not room:
            room = 'Portal Stage'
            note = 'Stage not listed in the official program; shown at the Portal Stage area (Dominion Days).'
        assert e['title'] in LIKE, e['title']
        lang = ' / '.join(e['langs'])
        desc = e['desc']
        if e['sub']:
            desc = e['sub'] + '\n\n' + desc
        out.append(dict(
            id=str(pre * 100 + i + 1), day=date, t0=hm24(e['times'][1]), t1=hm24(e['times'][2]),
            room=room, where=WHERE[room], title=e['title'], desc=desc, like=LIKE[e['title']],
            spk=e['hosts'], fmt=LANG.get(lang), lvl=AGES.get(e['title']), track=e['cat'] or None,
            de=lang == 'DE', note=note, also=[]))
json.dump({'sessions': out}, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(out), 'sessions')
