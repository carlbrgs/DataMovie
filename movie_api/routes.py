from flask import Blueprint, jsonify
from .services import make_request_with_retry
import os
import gzip
import json
import pandas as pd
from sqlalchemy import create_engine
import urllib.request
import traceback

api = Blueprint('api', __name__)

@api.route("/movie/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": os.getenv("TMDB_API_KEY")}
    result = make_request_with_retry(url, params)
    return jsonify(result)

@api.route("/allmovie", methods=["GET"])
def download_file():
    url = "http://files.tmdb.org/p/exports/movie_ids_10_16_2024.json.gz"
    out_file = './movieAll.json'
    data_list = []

    try:
        with urllib.request.urlopen(url) as response:
            with gzip.GzipFile(fileobj=response) as uncompressed:
                for line in uncompressed:
                    json_data = json.loads(line)
                    data_list.append(json_data)
        
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)

        return jsonify({"message": "File downloaded and processed successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred"}), 500
    

@api.route("/loadmovies", methods=["GET", "POST"])
def transform_and_load_to_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MOVIE_FILE_PATH = os.path.join(BASE_DIR, '..', 'movieAll.json')
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"MOVIE_FILE_PATH: {MOVIE_FILE_PATH}")
    
    try:
        with open(MOVIE_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data:
                print("Data loaded successfully")

        df = pd.DataFrame(data)
        print("DataFrame created successfully")
        print(df.head())

        engine = create_engine("mysql+pymysql://root:@localhost:3306/movies")
        print("Database engine created successfully")
        df.to_sql('movies', con=engine, if_exists='replace', index=False)
        print("Data loaded into database successfully")
        
        return jsonify({"message": "Data loaded successfully into MySQL"}), 200

    except FileNotFoundError:
        print("movieAll.json file not found")
        return jsonify({"message": "movieAll.json file not found"}), 404
    except json.JSONDecodeError as jde:
        print(f"JSON decode error: {str(jde)}")
        return jsonify({"message": f"JSON decode error: {str(jde)}"}), 400
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500