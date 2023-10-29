import math
from flair.nn import Classifier
from flair.data import Sentence
import pandas as pd
import joblib
import spacy
import asent
from textblob import TextBlob


class RatingEstimator:
    def __init__(self,model_path):
        self.model=None
        self.set_model(model_path)
        self.classifier=Classifier.load('sentiment')
        self.nlp = None
        self.nlp_init()
        self.sentiment_data=None
        self.rating=None

    def nlp_init(self):
        self.nlp = spacy.blank('en')
        self.nlp.add_pipe('sentencizer')

        # add the rule-based sentiment model
        self.nlp.add_pipe("asent_en_v1")
        pass
    
    def set_model(self,model_path):
        self.model = joblib.load(model_path)

    def exponential_mapping(self,score, sentiment_value):
        a = 2.0  


        normalized_score = max(0, min(1, (score - 0.5) / 0.5))


        center = 0.99 if sentiment_value == 'POSITIVE' else 0.01


        mapped_score = math.exp(-a * abs(normalized_score - center))

        mapped_score = mapped_score * 5.0

        return mapped_score


    def analyze_sentiment_flair(self,text):
        sentence = Sentence(text)
        self.classifier.predict(sentence)

        positivity_score = sentence.labels[0].score
        sentiment_value = sentence.labels[0].value

        estimated_rating = self.exponential_mapping(positivity_score, sentiment_value)

        return estimated_rating, sentiment_value,positivity_score

    def analyze_sentiment_textblob(self,text):
        testimonial = TextBlob(text)
        
        sentiment_value = testimonial.sentiment.polarity
        subjectivity_value = testimonial.sentiment.subjectivity
        # estimated_rating=(testimonial.sentiment.polarity+1)*2.5
        # return estimated_rating,sentiment_value,subjectivity_value
        return sentiment_value,subjectivity_value



    def analyze_sentiment_asent(self,text):
        doc = self.nlp(text)
        
        neg_value = doc._.polarity.negative
        neu_value = doc._.polarity.neutral
        pos_value = doc._.polarity.positive
        compound_value=doc._.polarity.compound
        # estimated_rating=sentiment_mapping(neg_value,neu_value,pos_value,compound_value)
        # return neg_value,neu_value,pos_value,compound_value,estimated_rating
        return neg_value,neu_value,pos_value,compound_value

    def get_sentiment(self,text):
        
        estimated_rating, sentiment_flair,positivity_flair=self.analyze_sentiment_flair(text)
        sentiment_textblob,subjectivity_textblob=self.analyze_sentiment_textblob(text)
        neg_asent,neu_asent,pos_asent,compound_asent=self.analyze_sentiment_asent(text)
        
        self.sentiment_data = {
            'estimated_rating': estimated_rating,
            'pos_asent': pos_asent,
            'neg_asent': neg_asent,
            'positivity_flair': positivity_flair,
            'sentiment_flair': sentiment_flair,
            'sentiment_textblob': sentiment_textblob,
            'compound_asent': compound_asent,
            'neu_asent': neu_asent,
            'subjectivity_textblob': subjectivity_textblob
        }

        pass


    def rating_estimation(self):
        rating_list = [2, 2.5, 3]
        sentiment_list = ['NEGATIVE', 'POSITIVE']
        
        sentiment = self.sentiment_data.get('sentiment_flair')
        sentiment = sentiment_list.index(sentiment)

        
        positivity = self.sentiment_data.get('positivity_flair', 0)
        if positivity >= 0.9:
            self.rating=self.sentiment_data.get('estimated_rating')
            return self.rating

        feature_names = ['pos_value_asent', 'neg_value_asent', 'probability', 'estimated_sentiment_flair', 'estimated_sentiment_textblob', 'compound_value_asent', 'neu_value_asent', 'estimated_subjectivity_textblob']
        cols = ['pos_asent', 'neg_asent', 'positivity_flair', 'sentiment_flair', 'sentiment_textblob', 'compound_asent', 'neu_asent', 'subjectivity_textblob']
        model_input = pd.DataFrame([{col: self.sentiment_data[col] for col in cols}])
        model_input.columns = feature_names
        
        model_predictions = self.model.predict(model_input)
        self.rating = rating_list[model_predictions[0]]
        
        return self.rating
    
    def comments_to_rating(self,comments):
        self.get_sentiment(comments)
        return self.rating_estimation()