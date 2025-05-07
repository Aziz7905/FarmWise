import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

class PesticideRecommender:
    DISEASE_TO_KEYWORD = {
        'ESCA': 'Esca grapevine',
        'Black Rot': 'Black rot grapevine',
        'Leaf Blight': 'Leaf blight grapevine',
        'brown spots': 'brown spots date palm',
        'white scale': 'white scale date palm',
        'grenning': 'greening citrus',
        'canker': 'canker citrus',
        'blackspot': 'black spot citrus',
        'rust': 'apple rust',
        'scab': 'apple scab',
        'multiple_diseases': 'apple diseases'
    }
    
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.data.columns = self.data.columns.str.strip()
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self._precompute_embeddings()
    
    def _precompute_embeddings(self):
        disease_texts = self.data['USAGE'].astype(str).tolist()
        self.disease_embeddings = self.model.encode(disease_texts, convert_to_tensor=True)
    
    def recommend(self, disease_name, top_k=3):
        search_term = self.DISEASE_TO_KEYWORD.get(disease_name, disease_name)
        input_embedding = self.model.encode(search_term, convert_to_tensor=True)
        
        similarity_scores = util.pytorch_cos_sim(input_embedding, self.disease_embeddings)
        top_k = min(top_k, len(similarity_scores[0]))
        top_results = torch.topk(similarity_scores, k=top_k)
        
        recommendations = []
        for score, idx in zip(top_results[0][0], top_results[1][0]):
            idx = idx.item()
            recommendations.append({
                'pesticide': self.data.iloc[idx]['SUBSTANCE ACTIVE'],
                'company': self.data.iloc[idx].get('SOCIETE', 'N/A'),
                'concentration': self.data.iloc[idx].get('CONC.', 'N/A'),
                'usage': self.data.iloc[idx]['USAGE'],
                'score': round(score.item() * 100, 2)
            })
            
        return recommendations