# Ingest the data from dataset/spotify-2023 into a database
import sys
import json
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Get the path to the dataset
dataset_path = os.path.join(os.path.dirname(__file__), 'dataset/')

# Get the path to the queries
queries_path = os.path.join(os.path.dirname(__file__), 'queries/')


def insert_to_spotify_2023(supabase):
  #remove non utf-8 characters from csv
  with open(os.path.join(dataset_path, 'spotify-2023.csv'), 'rb') as f:
      contents = f.read()
      contents = contents.decode('utf-8', 'ignore')
      contents = contents.encode('utf-8', 'ignore')
      f.close()
  with open(os.path.join(dataset_path, 'spotify-2023.csv'), 'wb') as f:
      f.write(contents)
      f.close()

  # read the csv file
  df = pd.read_csv(os.path.join(dataset_path, 'spotify-2023.csv'))
  # convert the dataframe to json
  data = df.to_json(orient='records')
  # convert the json to a python dictionary
  data = json.loads(data)
  # insert the data into the table
  supabase.table('spotify_2023').insert(data).execute()
  response = supabase.table('spotify_2023').select("*").execute()
  print(response)
 
def main():
  load_dotenv()
  supabase_url = os.getenv('SUPABASE_URL')
  supabase_key = os.getenv('SUPABASE_KEY')
  supabase: Client = create_client(supabase_url, supabase_key)
  insert_to_spotify_2023(supabase)


main()
