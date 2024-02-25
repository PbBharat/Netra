import pandas as pd
from fuzzywuzzy import fuzz


def data_import(drug_name):
    df= pd.read_csv("/home/aneesh.paul/Downloads/Drugs Data - Sheet1.csv")

    # List to hold the indices of rows with fuzzy partial ratio > 90
    # selected_indices = []

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        # Calculate fuzzy partial ratio
        actual_drug_name= df.loc[index, "Drug Name"]
        print(actual_drug_name)
        ratio = fuzz.partial_ratio(actual_drug_name, drug_name)
        print(ratio)
        
        # Check if the ratio is greater than 90
        if ratio > 90:
            # If yes, append the index to the list
            selected_index= index
            break

    # Filter the DataFrame to get the rows with fuzzy partial ratio > 90
    compo = df.iloc[selected_index, 1]
    event = df.iloc[selected_index, 4]

    return {"compo" : compo, "events": event}
