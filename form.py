import streamlit as st
import pandas as pd

def average_score(questions):
    scores = [st.slider(f"{question}", 1.0, 5.0, 3.0, 0.1) for question in questions]
    average = sum(scores) / len(questions)
    return round(average, 1)

def show_form():
    # Loading the dataset
    data_path = 'csv/user_data.csv'
    data = pd.read_csv(data_path)
    
    # Extracting the name from the CSV file
    name = data.at[0, 'Druivensoort']
    st.header(f"Hallo, {name}. Laten we jouw wijnmatch vinden!")

    zuur_score = average_score([
        "1 Hoe vind je de scherpte van een groene appel in je wijn?",
        "2 Geniet je van smaken zoals citroen in je wijn?",
        "3 Hoe zou je je tolerantie voor zure smaken in wijn beschrijven? Heb je liever een pittige smaak (5) of iets subtielers (1)?",
        "4 Geef je de voorkeur aan een lichte verfrissende wijn (1) of een zwaardere droge wijn (5)?",
        "5 Hoe sta je tegenover de zurigheid van bessen in je wijn?",
        "6 Hoe belangrijk is de frisheid die zuur aan een wijn toevoegt voor jou?"
    ])
    
    body_vol_score = average_score([
        "7 Hoe belangrijk is het mondgevoel van de wijn voor jou? Hou je van lichte, frisse wijnen (1) of van rijke, volle wijnen (5)?",
        "8 Wat vind je van wijnen die rijk en vol zijn?",
        "9 Geniet je van een romige textuur in je wijn?",
        "10 Is een zware wijn iets wat je zoekt?",
        "11 Heb je een voorkeur voor gerechten met vlees en vis gebakken in boter (5, romiger) of van de grill (1, steviger)?",
        "12 Hoe belangrijk is de lengte van de nasmaak voor jou?"
    ])
    
    suiker_zoet_score = average_score([
        "13 Hoe zoet mag de wijn voor jou zijn?",
        "14 Wat vind je van een lichte zoetheid in je wijn?",
        "15 Is een gebalanceerde zoetheid met een hint van droogte aantrekkelijk voor jou?",
        "16 Geef je de voorkeur aan dessertwijnen met een hoge zoetheid?",
        "17 Hoe belangrijk zijn de zoetheid en andere componenten in de wijn voor jou?",
        "18 Hoe zou je het zoetheidsniveau van je favoriete wijn beschrijven?",
        "19 Als je een voorkeur hebt, hou je dan van hartige (1) of zoete (5) snacks?"
    ])
    
    # Using loc for safer data setting
    data.loc[0, 'Zuur'] = zuur_score
    data.loc[0, 'Body / vol'] = body_vol_score
    data.loc[0, 'Suiker / zoet'] = suiker_zoet_score
    
    # Safely update remaining columns using loc
    for column in data.columns[4:]:  # Skip the name and the first three columns already handled
        data.loc[0, column] = st.slider(f"Hoe veel houd je van de smaak van {column.lower()} in je wijn?", 1.0, 5.0, 3.0, 0.1)
    
    # Final preference question
    preference = st.selectbox(
        "Waar ligt uw voorkeur?",
        ("Strak droog (zuur)", "Volle zachte droge wijn (body/vol)", "Mild droge wijn (suiker/zoet)")
    )
    
    if st.button("Voorkeuren indienen"):
        # Save back to CSV
        data.to_csv(data_path, index=False)
        
        # Find best match based on preference
        if preference == "Strak droog (zuur)":
            best_match = data.loc[data['Zuur'].idxmax(), 'Druivensoort']
        elif preference == "Volle zachte droge wijn (body/vol)":
            best_match = data.loc[data['Body / vol'].idxmax(), 'Druivensoort']
        else:
            best_match = data.loc[data['Suiker / zoet'].idxmax(), 'Druivensoort']
        
        st.success(f"Voorkeuren ingediend! Uw beste match is: {best_match}. Bekijk de resultaten in het tabblad 'Uitslagen'.")
