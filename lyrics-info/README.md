# CMPT 756 Lyrics Info Service
The lyrics info service maintains a list of meta data related to songs such as lyrics, release date, record company etc. Users can query this table with the music id from the main music table. 

### Installation
    pip install virtualenv (if you don't already have virtualenv installed)
    virtualenv venv to create your new environment (called 'venv' here)
    source venv/bin/activate to enter the virtual environment
    pip install -r requirements.txt
    python3 app.py 5000

### APIs

1. Create the lyrics info table

    Method type: GET <br>
    http://127.0.0.1:5000/api/v1/music/info/lyricsinfo/create

2. Populate the lyrics info table (from music_info.csv)

    Method type: GET <br>
    http://127.0.0.1:5000/api/v1/music/info/lyricsinfo/populate

3. Get data from the lyrics info table <br>
   http://127.0.0.1:5000/api/v1/music/info/lyricsinfo/create

   Response: <br>
        { <br>
            "lyrics": "This song has some fantastic lyrics", <br>
            "music_id": "22e47f97-11ca-4c3c-8e77-f3068fddaf6e", <br>
            "num_sales": "7802", <br>
            "record_company": "758 Studio", <br>
            "release_date": "23-02-2022" <br>
        }     
