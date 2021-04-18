from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
load_dotenv()
print(env_path)