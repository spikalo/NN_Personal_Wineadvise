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
    st.header(f"Hello, {name}. Let's find your wine match!")

    zuur_score = average_score([
        "1 How do you like the sharpness of a green apple in your wine?",
        "2 Do you enjoy the flavors like lemon in your wine?",
        "3 How would you describe tolerance of acidic flavors in wine? do you prefer a spicy taste (5) or something more subtle (1)",
        "4 Do you prefer a light refreshing wine (1) or a heavier dry wine (5)?",
        "5 How do you feel about the tartness of berries in your wine?",
        "6 How important is the freshness that acid adds to a wine to you?"
    ])
    
    body_vol_score = average_score([
        "7 How important is the mouthfeel of the wine to you? Do you like light, fresh wines (1), or rich, fuller wines (5)?",
        "8 How do you feel about wines that are rich and full-bodied?",
        "9 Do you enjoy a creamy texture in your wine?",
        "10 Is a heavy wine something you look for?",
        "11 Do you prefer dishes with meat and fish fried in butter (5, creamier) or from the grill (1, firmer)?"
        "12 How important is the length of the aftertaste to you?"
    ])
    
    suiker_zoet_score = average_score([
        "13 How sweet can the wine be for you?",
        "14 How do you feel about a slight sweetness in your wine?",
        "15 Is a balanced sweetness with a hint of dryness appealing to you?",
        "16 Do you prefer dessert wines with high sweetness?",
        "17 How important is the sweetness and other components in the wine for you?"
        "18 How would you describe the sweetness level of your favorite wine?"
        "19 If you have a preference, do you prefer savory (1) or sweet (5) snacks?"
    ])
    
    # Using loc for safer data setting
    data.loc[0, 'Zuur'] = zuur_score
    data.loc[0, 'Body / vol'] = body_vol_score
    data.loc[0, 'Suiker / zoet'] = suiker_zoet_score
    
    # Safely update remaining columns using loc
    for column in data.columns[4:]:  # Skip the name and the first three columns already handled
        data.loc[0, column] = st.slider(f"How much do you like the taste of {column.lower()} in your wine?", 1.0, 5.0, 3.0, 0.1)
    
    # Final preference question
    preference = st.selectbox(
        "Where does your preference lie?",
        ("Strak droog (zuur)", "Volle zachte droge wijn (body/vol)", "Mild droge wijn (suiker/zoet)")
    )
    
    if st.button("Submit Preferences"):
        # Save back to CSV
        data.to_csv(data_path, index=False)
        
        # Find best match based on preference
        if preference == "Strak droog (zuur)":
            best_match = data.loc[data['Zuur'].idxmax(), 'Druivensoort']
        elif preference == "Volle zachte droge wijn (body/vol)":
            best_match = data.loc[data['Body / vol'].idxmax(), 'Druivensoort']
        else:
            best_match = data.loc[data['Suiker / zoet'].idxmax(), 'Druivensoort']
        
        st.success(f"Preferences submitted! Your best match is: {best_match}. View results in the 'Uitslagen' tab.")
