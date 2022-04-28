# Imports
import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime
from sklearn.preprocessing import RobustScaler, LabelEncoder

class Rossmann(object):
    def __init__(self):
        self.home_path = ''
        self.competition_distance_scaler   = pickle.load(open(self.home_path + 'parameter/competition_distance_scaler.pkl', 'rb'))
        self.competition_time_month_scaler = pickle.load(open(self.home_path + 'parameter/competition_time_month_scaler.pkl', 'rb'))
        self.promo_time_week_scaler        = pickle.load(open(self.home_path + 'parameter/promo_time_week_scaler.pkl', 'rb'))
        self.store_type_scaler             = pickle.load(open(self.home_path + 'parameter/store_type_scaler.pkl', 'rb'))
        self.year_scaler                   = pickle.load(open(self.home_path + 'parameter/year_scaler.pkl', 'rb'))
        self.store_type_scaler             = pickle.load(open(self.home_path + 'parameter/store_type_scaler.pkl', 'rb'))
        
    def data_cleaning(self, df1):

        # Columns to receive (not sales or costumers)
        old_cols = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo',
                       'StateHoliday', 'SchoolHoliday', 'StoreType', 'Assortment',
                       'CompetitionDistance', 'CompetitionOpenSinceMonth',
                       'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek',
                       'Promo2SinceYear', 'PromoInterval']

        # Function: Transform to snake case
        snake_case =  lambda x: inflection.underscore(x)

        # CaLL function to New columns
        new_cols = list(map(snake_case, old_cols))

        # Rename
        df1.columns = new_cols

        # Transform 'date': 'object' to 'datetime'
        df1['date'] = pd.to_datetime(df1['date'])

        ## 1.5 Fillout NA Values
        df1['competition_distance'] = df1['competition_distance'].apply(lambda x: 200000 if math.isnan(x) else x)
        
        df1['competition_open_since_month'] = df1.apply(lambda x: x['date'].month 
                                                        if math.isnan(x['competition_open_since_month']) 
                                                        else x['competition_open_since_month'], axis=1)
        
        df1['competition_open_since_year'] = df1.apply(lambda x: x['date'].year
                                                        if math.isnan(x['competition_open_since_year']) 
                                                        else x['competition_open_since_year'], axis=1)

        df1['promo2_since_week'] = df1.apply(lambda x: x['date'].week
                                                        if math.isnan(x['promo2_since_week']) 
                                                        else x['promo2_since_week'], axis=1)

        df1['promo2_since_year'] = df1.apply(lambda x: x['date'].year
                                                        if math.isnan(x['promo2_since_year']) 
                                                        else x['promo2_since_year'], axis=1)

        month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 
                     9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        # Fill 'NA' with 0
        df1['promo_interval'].fillna(0, inplace=True)

        # Create column month_map to map
        df1['month_map'] = df1['date'].dt.month.map(month_map)

        # Check if sale is in promo by date
        df1['is_promo'] = df1.apply(lambda x: 0 if x['promo_interval']==0 
                                    else 1 if x['month_map'] in x['promo_interval'].split(',') else 0, axis=1)

        # Change float64 to int32
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype(int)
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype(int)
        df1['promo2_since_week'] = df1['promo2_since_week'].astype(int)
        df1['promo2_since_year'] = df1['promo2_since_year'].astype(int)
        
        return df1
    
    
    def feature_engineering(self, df2):

        # Feature year
        df2['year'] = df2['date'].dt.year

        # Feature month
        df2['month'] = df2['date'].dt.month

        # Feature day
        df2['day'] = df2['date'].dt.day

        # Feature week of year
        df2['week_of_year'] = df2['date'].dt.isocalendar().week
        df2['week_of_year'] = df2['week_of_year'].astype('int32', copy=False)

        # Feature year_week
        df2['year_week'] = df2['date'].dt.strftime('%Y-%W')

        # Feature competition_since = The year and month are separated in the dataset, join them
        df2['competition_since'] = df2.apply(lambda x: datetime.datetime(year=x['competition_open_since_year'], month=x['competition_open_since_month'], day=1), axis=1)
        df2.head()

        # Feature competition_time_month = quantity of months since competition has been placed
        df2['competition_time_month'] = ((df2['date'] - df2['competition_since'])/30).apply(lambda x: x.days).astype(int)

        # Feature promo_since = The year and week of the start of promo are separeted, join them
        df2['promo_since'] = df2['promo2_since_year'].astype(str) + '-' + df2['promo2_since_week'].astype(str)
        df2['promo_since'] = df2['promo_since'].apply(lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days=7))

        # Feature promo_time_week = Difference between the sale date and the promo extended started date
        df2['promo_time_week'] = ((df2['date'] - df2['promo_since'])/7).apply(lambda x: x.days).astype(int)
        # If the column has negative values, the store is in regular promo
        # If the column has positive values, the store is in extended promo 

        # Feature assortment = Instead of a,b,c values, use basic,extra,extended values
        df2['assortment'] = df2['assortment'].apply(lambda x: 'basic' if x=='a' else 'extra' if x=='b' else 'extended')

        # Feature state_holiday = Instead of a,b,c,0 values, use public_holiday,easter_holyday,christmas_holiday,regular_day values
        df2['state_holiday'] = df2['state_holiday'].apply(lambda x: 'public_holiday' if x=='a' else 'easter_holiday' if x=='b' else 'christmas_holiday' if x=='c' else 'regular_day')

        ## 3.1 Row Filter (don't have sales,costumers anymore)
        df2 = df2[df2['open']==1]

        ## 3.2 Columns Selection
        cols_drop = ['open', 'month_map', 'promo_interval']
        df2 = df2.drop(columns=cols_drop, axis=1)
        
        return df2


    def data_preparation(self, df5):

        ## 5.2 Rescaling 
        # competition_distance
        df5['competition_distance'] = self.competition_distance_scaler.fit_transform(df5[['competition_distance']].values)

        # competition_time_month
        df5['competition_time_month'] = self.competition_time_month_scaler.fit_transform(df5[['competition_time_month']].values)

        # promo_time_week
        df5['promo_time_week'] = self.promo_time_week_scaler.fit_transform(df5[['promo_time_week']].values)

        # year
        df5['year'] = self.year_scaler.fit_transform(df5[['year']].values)

        ### 5.3.1 Encoding
        # Enconding | state_holiday | One-Hot-Enconding method
        df5 = pd.get_dummies(data=df5, columns=['state_holiday'])

        # Enconding | store_type | Label Enconding method
        le = LabelEncoder()
        df5['store_type'] = self.store_type_scaler.fit_transform(df5['store_type'])

        # Enconding | assortment | Ordinal Enconding
        dict_assortment = {'basic': 1, 'extra': 2, 'extended': 3}
        df5['assortment'] = df5['assortment'].map(dict_assortment)

        ### 5.3.3 Nature Transformation
        # day_of_week
        df5['day_of_week_sin'] = df5['day_of_week'].apply(lambda x: np.sin(x * (2*np.pi/7)))
        df5['day_of_week_cos'] = df5['day_of_week'].apply(lambda x: np.cos(x * (2*np.pi/7)))

        # month
        df5['month_sin'] = df5['month'].apply(lambda x: np.sin(x * (2*np.pi/12)))
        df5['month_cos'] = df5['month'].apply(lambda x: np.cos(x * (2*np.pi/12)))

        # day
        df5['day_sin'] = df5['day'].apply(lambda x: np.sin(x * (2*np.pi/30)))
        df5['day_cos'] = df5['day'].apply(lambda x: np.cos(x * (2*np.pi/30)))

        # week_of_year
        df5['week_of_year_sin'] = df5['week_of_year'].apply(lambda x: np.sin(x * (2*np.pi/52)))
        df5['week_of_year_cos'] = df5['week_of_year'].apply(lambda x: np.cos(x * (2*np.pi/52)))

        ## 5.4 Select Columns from boruta
        cols_selected = [ 'store',
                                 'promo',
                                 'store_type',
                                 'assortment',
                                 'competition_distance',
                                 'competition_open_since_month',
                                 'competition_open_since_year',
                                 'promo2',
                                 'promo2_since_week',
                                 'promo2_since_year',
                                 'competition_time_month',
                                 'promo_time_week',
                                 'day_of_week_sin',
                                 'day_of_week_cos',
                                 'month_sin',
                                 'month_cos',
                                 'day_sin',
                                 'day_cos',
                                 'week_of_year_sin',
                                 'week_of_year_cos']

        return df5[cols_selected]
    
    def get_prediction(self, model, original_data, test_data): # The user will receive the same data with one more column = prediction
        
        # Prediction
        pred = model.predict(test_data)
        
        # Join prediction into the original data
        original_data['prediction'] = np.expm1(pred)
        
        return original_data.to_json(orient='records', date_format='iso')