from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
load_dotenv()

class Config:
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    BEARER_TOKEN = os.getenv('BEARER_TOKEN')
    USER_ACCESS_TOKEN = os.getenv('USER_ACCESS_TOKEN')
    USER_ACCESS_SECRET = os.getenv('USER_ACCESS_SECRET')
    TWITTER_SEARCH_URL = os.getenv('TWITTER_SEARCH_URL')
    ANALYSTS = {
        'NFL Fantasy Football': 'NFLFantasy',
        'PFF Fantasy Football': 'PFF_Fantasy',
        'FantasyPros': 'FantasyPros',
        'Bleacher Report': 'BleacherReport',
        'Danny Heifetz':'Danny_Heifetz',
        'Kyle Yates':'KyleYNFL',
        'Joe Bryant':'Football_Guys',
        'Chris Raybon':'ChrisRaybon',
        'Dan Harris':'danharris80',
        'Dylan Chappine':'dylanchappine',
        'John Paulsen':'4for4_John',
        'Joe Bond':'F6P_Joe',
        'Nathan Jahnke':'PFF_NateJahnke',
        'Justin Boone':'justinboone',
        'Cecil Lammey':'CecilLammey',
        'Kyle Soppe':'KyleSoppeESPN',
        'Sigmund Bloom':'SigmundBloom',
        'Chris Meaney':'chrismeaney',
        'Ben Cummins':'BenCumminsFF',
        'Ian Rapoport':'RapSheet',
        'Field Yates':'FieldYates',
        'Adam Schefter':'AdamSchefter',
        'Matthew Berry':'MatthewBerryTMR',
        'Stephania Bell':'Stephania_ESPN',
        'Adam Levitan':'adamlevitan',
        'Evan Silva':'evansilva',
        'JJ Zachariason':'LateRoundQB',
        'Matt Harmon':'MattHarmon_BYB',
        'Brooks C. Carmean':'brookscarmean',
        'Mike Clay':'MikeClayNFL',
        'Jason Moore':'jasonffl',
        'Mike Wright':'FFHitman',
        'Fantasy Footballers':'TheFFBallers'
    }
