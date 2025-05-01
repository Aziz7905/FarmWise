import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

class PesticideModel:
    def __init__(self):
        # Load the cleaned pesticide dataset
        file_path = "assets/final_cleaned_pesticide_data.csv"
        self.pesticide_data = pd.read_csv(file_path)
        
        # Ensure column names are consistent
        self.pesticide_data.columns = self.pesticide_data.columns.str.strip()
        
        # Select relevant columns
        self.disease_column = "USAGE"
        self.pesticide_column = "SUBSTANCE ACTIVE"
        
        # Drop rows with missing values in essential columns
        self.pesticide_data = self.pesticide_data.dropna(subset=[self.disease_column, self.pesticide_column])
        
        # Initialize the sentence embedding model
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        # Generate embeddings
        disease_texts = self.pesticide_data[self.disease_column].astype(str).tolist()
        pesticide_texts = self.pesticide_data[self.pesticide_column].astype(str).tolist()
        
        self.disease_embeddings = self.model.encode(disease_texts, convert_to_tensor=True)
        self.pesticide_embeddings = self.model.encode(pesticide_texts, convert_to_tensor=True)
    
    def recommend(self, input_disease):
        """
        Given a disease name, find the most relevant pesticide based on semantic similarity.
        Returns a dictionary with pesticide details in the correct format.
        """
        try:
            # Encode the input disease
            input_embedding = self.model.encode(input_disease, convert_to_tensor=True)
            
            # Compute similarity scores
            similarity_scores = util.pytorch_cos_sim(input_embedding, self.disease_embeddings)
            
            # Get the best match
            best_match_idx = torch.argmax(similarity_scores).item()
            recommendation = self.pesticide_data.iloc[best_match_idx].to_dict()
            
            # Calculate match score (convert similarity score to percentage)
            match_score = similarity_scores[0][best_match_idx].item() * 100
            
            # Return in the correct format expected by the controller
            return {
                'SUBSTANCE ACTIVE': recommendation.get(self.pesticide_column, 'Unknown'),
                'USAGE': recommendation.get(self.disease_column, 'Unknown'),
                'SOCIETE': recommendation.get('SOCIETE', 'Unknown'),
                'CONC.': recommendation.get('CONC.', 'Unknown'),
                'score': match_score
            }
        except Exception as e:
            print(f"Error in recommendation: {e}")
            return None

def load_pesticide_model():
    return PesticideModel()