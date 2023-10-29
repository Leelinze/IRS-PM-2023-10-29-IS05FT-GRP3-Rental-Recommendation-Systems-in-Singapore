import random
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from collections import defaultdict
from surprise import SVD
from surprise import Dataset
from surprise import Reader
from surprise import dump
import os
# from DataManger import FormData
from app.services.GeneticAlgorithm import genetic_algorithm

class Recommender:
    def __init__(self, modelpath,topn,alpha,svd_param): 
        self.matrix_factorization_model = None
        self.mode=None
        self.modelpath=modelpath
        self.set_MFmodel(modelpath)
        self.recommend_num=topn
        self.svd_param=svd_param
        self.popularity_recommend_result=None
        self.weighted_content_based_recommend_result=None
        self.matrix_factorization_recommendation_result=None
        self.matrix_factorization_recommendation_df=None
        self.content_based_recommend_result=None
        self.content_based_recommend_with_diversity_result=None
        self.hybrid_recommendations_result=None
        self.alpha=alpha
        self.data=None
        self.rating=None
        self.user_preference=None
        self.weight_vector=None
        self.currUID=None
    def set_MFmodel(self, model_path):
        file_name = os.path.expanduser(model_path)
        _, model = dump.load(file_name)
        self.matrix_factorization_model=model

    def popularity_based_recommendation(self, df,rating_cols):
        df = df.assign(total_rating=df[rating_cols].sum(axis=1))
        sorted_df = df.sort_values(by='total_rating', ascending=False)
        max_total_rating = sorted_df['total_rating'].max()
        topn_candidates = sorted_df[sorted_df['total_rating'] == max_total_rating]
        
        if len(topn_candidates) <= self.recommend_num:
            self.popularity_recommend_result = topn_candidates
        else:
            sampled_rows = random.sample(topn_candidates.index.tolist(), self.recommend_num)
            self.popularity_recommend_result = df.loc[sampled_rows]
        pass

    def weighted_content_based_recommendation(self, data,user_preference,weight_vector):
        # data_vector=data.drop('HouseID',axis=1).values
        if 'HouseID' in data.columns:
            data_process = data.drop('HouseID', axis=1)

        if 'weighted_similarity' in data_process.columns:
            data_process = data_process.drop('weighted_similarity', axis=1)

        data_vector = data_process.values
        weighted_data_vector = data_vector * weight_vector
        user_preference = user_preference.reshape(1, -1)
        weighted_user_vector =  user_preference * weight_vector
        weighted_similarities = cosine_similarity(weighted_user_vector, weighted_data_vector)
        data['weighted_similarity'] = weighted_similarities.transpose()
        self.weighted_content_based_recommend_result = data.sort_values(by='weighted_similarity', ascending=False) 
        pass
    def content_based_recommendation(self, data,user_preference):
        similarities = cosine_similarity(user_preference, data)
        data['similarity'] = similarities.transpose()
        data['similarity']= similarities.transpose()
        self.content_based_recommend_result = data.nlargest(self.recommend_num, 'similarity')
        pass

    def content_based_recommendation_with_diversity(self, data,user_preference,weight_vector):
        self.weighted_content_based_recommendation(data,user_preference,weight_vector)
        item_features=self.weighted_content_based_recommend_result
        item_features = item_features[item_features['weighted_similarity'] >= 0]
        item_features_without_similarity = item_features.drop(['weighted_similarity', 'HouseID'], axis=1)
        item_features = item_features.reset_index(drop=True)
        similarity_matrix = cosine_similarity(item_features_without_similarity)

        diversity_matrix = 1 - similarity_matrix
        id_to_index = {row['HouseID']: index for index, row in item_features.iterrows()}


        # for epsilon in np.linspace(0, 0.5, 1):
        epsilon=0.2
        recommendation, score = genetic_algorithm(item_features, epsilon, self.recommend_num,diversity_matrix,id_to_index)
        self.content_based_recommend_with_diversity_result = item_features.loc[item_features['HouseID'].isin(recommendation)]
        pass
    
    def matrix_factorization_recommendation(self, user_id, df):
        if 'user_id' not in df.columns or 'item_id' not in df.columns:
            raise ValueError("DataFrame must contain 'user_id' and 'item_id' columns")
    
        item_ids = df['item_id'].unique()
        predictions = defaultdict(float)
        
        for item_id in item_ids:
            predictions[item_id] = self.matrix_factorization_model.predict(user_id, item_id, verbose=True).est
        
        recommended_items = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        est = pd.DataFrame(recommended_items, columns=['HouseID', 'est'])
        self.matrix_factorization_recommendation_df=est
        self.matrix_factorization_recommendation_result=[item[0] for item in recommended_items]
        pass
    
    def hybrid_recommendation(self):
        """
        Hybrid recommendation function that combines matrix factorization and content-based recommendations.
        
        :param user_id: ID of the user
        :param item_id: ID of the item
        :param matrix_factorization_model: Trained matrix factorization model
        :param content_based_model: Trained content-based model
        :param alpha: Weight for matrix factorization recommendation score (0 <= alpha <= 1)
        :return: Hybrid recommendation score
        """
        # Get the matrix factorization recommendation score
        matrix_factorization_df=self.matrix_factorization_recommendation_df
        content_based_df=self.weighted_content_based_recommend_result[['HouseID', 'weighted_similarity']]
        scaler = MinMaxScaler(feature_range=(-1, 1))
        matrix_factorization_df['est'] = scaler.fit_transform(matrix_factorization_df[['est']])
        merged_df = pd.merge(matrix_factorization_df, content_based_df, on='HouseID')
        merged_df['weighted_score'] = self.alpha * merged_df['weighted_similarity'] + (1 - self.alpha) * merged_df['est']
        self.hybrid_recommendations_result = merged_df.sort_values(by='weighted_score', ascending=False)
        pass
    def set_param(self,weight_vector,user_vector_w,data_vector):
        # print("Setting parameters:")
        # print("Weight Vector:", weight_vector)
        # print("User Vector W:", user_vector_w)
        # print("Data Vector:", data_vector)
        self.data=data_vector
        self.user_preference=user_vector_w
        self.weight_vector=weight_vector          
    def noRating_recommend(self):
        # print("Data:", self.data)
        # print("User Preference:", self.user_preference)
        # print("Weight Vector:", self.weight_vector)
        # self.content_based_recommendation_with_diversity(self.data,self.user_preference,self.weight_vector)
        self.weighted_content_based_recommendation(self.data,self.user_preference,self.weight_vector)

    def Rating_recommend(self):
        self.weighted_content_based_recommendation(self.data,self.user_preference,self.weight_vector)
        self.matrix_factorization_recommendation(self.currUID,self.rating)
        self.hybrid_recommendation()
    
    def recommend(self):
        if self.mode=="content_based":
            print("no rating")
            self.noRating_recommend()
        else:
            print("rating")
            self.Rating_recommend()

    # def get_result_old(self):
    #     result=self.content_based_recommend_with_diversity_result.head(self.recommend_num)
    #     result_list=result['HouseID'].tolist()
    #     return result_list
    
    def get_result(self):
        if self.mode=="content_based":
            print("no rating")
            result_w=self.weighted_content_based_recommend_result.head(self.recommend_num)
            result_w_list=result_w['HouseID'].tolist()
            # result_wd=self.content_based_recommend_with_diversity_result.head(self.recommend_num)
            # result_wd_list=result_wd['HouseID'].tolist()
            # merged_list = result_w_list[:int(self.recommend_num/2)] + result_wd_list[:int(self.recommend_num/2)]
            # return merged_list

            return result_w_list
        else:
            print("rating")
            result=self.hybrid_recommendations_result.head(self.recommend_num)
            result_list=result['HouseID'].tolist()
            return result_list
        
    def model_update(self,df):
        algo = SVD(**self.svd_param)
        reader = Reader(rating_scale=(0,5)) # assumes datafile contains: user, item, ratings (in this order)
        data = Dataset.load_from_df(df, reader)
        self.matrix_factorization_model = algo.fit(data.build_full_trainset())
        dump.dump(self.modelpath, algo=self.matrix_factorization_model)
        pass