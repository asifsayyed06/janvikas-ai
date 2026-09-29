import sqlite3
from datetime import datetime
import pandas as pd
from ai_engine import analyze_request

DB = "janvikas.db"

def connect():
    return sqlite3.connect(DB)

def init_db():
    con = connect()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        district TEXT,
        ward TEXT,
        language TEXT,
        category TEXT,
        population_affected INTEGER,
        priority TEXT,
        priority_score INTEGER,
        urgency TEXT,
        reason TEXT,
        recommendation TEXT,
        department TEXT,
        signals TEXT,
        status TEXT DEFAULT 'New',
        latitude REAL,
        longitude REAL,
        created_at TEXT
    )
    """)
    con.commit()
    con.close()

def add_request(title, description, district, ward, language, category, population, analysis):
    con = connect()
    con.execute("""
    INSERT INTO requests
    (title,description,district,ward,language,category,population_affected,
     priority,priority_score,urgency,reason,recommendation,department,signals,status,
     latitude,longitude,created_at)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        title, description, district, ward, language, category, population,
        analysis["priority"], analysis["priority_score"], analysis["urgency"],
        analysis["reason"], analysis["recommendation"], analysis["department"],
        ", ".join(analysis["signals"]), "New",
        analysis.get("latitude", 18.5204), analysis.get("longitude", 73.8567),
        datetime.now().isoformat(timespec="seconds")
    ))
    con.commit()
    con.close()

def get_requests():
    con = connect()
    df = pd.read_sql_query("SELECT * FROM requests ORDER BY id DESC", con)
    con.close()
    return df

def update_status(request_id, status):
    con = connect()
    con.execute("UPDATE requests SET status=? WHERE id=?", (status, request_id))
    con.commit()
    con.close()

def seed_demo_data():
    demo = [
        ("Potholes near school",
         "Deep potholes are causing accidents near a school and ambulance movement is difficult.",
         "Pune","Ward 12","English","Roads",3500),
        ("Water supply interruption",
         "Families have not received drinking water for three days.",
         "Pune","Ward 8","English","Water",5200),
        ("Streetlights not working",
         "Several streetlights are broken around the bus stop.",
         "Nashik","Ward 4","English","Public Safety",900),
        ("Primary health centre shortage",
         "The local health centre has long queues and shortage of basic medicines.",
         "Ahmednagar","Ward 7","English","Healthcare",6800),
        ("Garbage collection issue",
         "Waste has accumulated for a week near the market.",
         "Nagpur","Ward 19","English","Sanitation",2100),
    ]
    for item in demo:
        title, desc, district, ward, language, category, pop = item
        add_request(title, desc, district, ward, language, category, pop,
                    analyze_request(title, desc, category, pop))
