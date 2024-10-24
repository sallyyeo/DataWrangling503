import os   # to set working directory
import re   # for regex
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

# Define regex for parsing
INIT_regex = re.compile(r'^WEBVTT\s*$')
SNo_regex = re.compile(r'^(\d+)\s*$')
Time_regex = re.compile(r'^(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\s*$')
NameUtt_regex = re.compile(r'^([^:]+):\s?(.*)$')

# Set your working directory
os.chdir('/Users/sallyyeo/Desktop/ANL503ECA')

# Read the VTT file, with handle file closure
vttpath = 'captured_dialogue.vtt'
with open(vttpath) as vtt:
    all_lines = vtt.readlines()

# Initialize lists to store extracted values
sno_list, time_from_list, time_to_list, reg_name_list, utterance_list = [], [], [], [], []

# Initialize an unknown speaker
unknown_speaker = None

lookingFor = 'INIT'
for i, current_line in enumerate(all_lines):
    if lookingFor == 'INIT':
        mo = INIT_regex.search(current_line)
        if mo:
            lookingFor = 'SNo'
            continue
    elif lookingFor == 'SNo':
        mo = SNo_regex.search(current_line)
        if mo:
            sno = int(mo.group(1))  # Retrieve only the seq number
            lookingFor = 'TimeFrom'
            continue
    elif lookingFor == 'TimeFrom':
        mo = Time_regex.search(current_line)
        if mo:
            time_from, time_to = mo.groups()
            lookingFor = 'RegName'
            continue
    elif lookingFor == 'RegName':
        mo = NameUtt_regex.search(current_line)
        if mo:
            reg_name, utterance = mo.groups()
        else:
            # If the current line does not match NameUtt_regex,
            # check if it's because it's a continuation of the last utterance or 
            # has no named speaker.
            if current_line.strip() == "":
                # Skip empty lines
                continue
            elif not unknown_speaker:
                # If there's no speaker, assign UNKNOWN
                reg_name = "UNKNOWN"
                utterance = current_line.strip()

        # Append values to lists
        sno_list.append(sno)
        time_from_list.append(time_from)
        time_to_list.append(time_to)
        reg_name_list.append(reg_name)
        utterance_list.append(utterance)

        # At the end of dialogue block, next thing look for SNo
        lookingFor = 'SNo'

# Create DataFrame from lists
df = pd.DataFrame({
    'SNo': sno_list,
    'TimeFrom': time_from_list,
    'TimeTo': time_to_list,
    'RegName': reg_name_list,
    'Utterance': utterance_list
})

# Print for debugging
print(df)

# SQLAlchemy engine URL for MySQL
# to handle special characters in password
engine_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="Ihtrmp@2405", 
    host="localhost",
    database="anl503eca"
)

engine = create_engine(engine_url)

# Create table in MySQL
df.to_sql('vtt', con=engine, if_exists='replace', index=False)