# import library
# python 3.7.7 version
import keras # 2.3.1 version
import warnings # python 내장
import numpy as np # 1.18.1 version
import pandas as pd # 1.0.3 version
import os # python 내장
from sklearn.preprocessing import MinMaxScaler # scikit-learn 0.23.1
from sklearn import datasets, linear_model # scikit-learn 0.23.1
from sklearn.externals import joblib # scikit-learn 0.23.1
import tensorflow as tf # 2.1.0 version
from keras.models import Model # 2.3.1 version
from keras.layers import Input, Dense, LSTM, Bidirectional # 2.3.1 version
from keras import backend as K # 2.3.1 version
from keras.models import load_model # 2.3.1 version # 모델 저장하고 로드하는 라이브러리
from mlxtend.feature_selection import SequentialFeatureSelector as sfs # 0.17.2 version
from sklearn import datasets, linear_model 
from sklearn.model_selection import train_test_split, GridSearchCV # scikit-learn 0.23.1

from sqlalchemy import create_engine
import pymysql

warnings.filterwarnings(action='ignore')

# ddd db에 맞게 수정
engine = create_engine("mysql+mysqldb://root:" + "#" + "@localhost/ddd", encoding='utf-8')
conn = engine.connect()

data = pd.read_sql_table(table_name='week_data', con = engine)

conn.close()

def transform(data):
        
    data['price_mean'] = data['price_mean'].replace(0.0,np.nan)
    data = data.fillna(method='ffill')
   
    # 원본 데이터의 '한우가격' 값 한칸씩 떙겨서 우리가 맞출려는 y_value 생성
    data['y_value'] = None
    
    for i in range(0,(len(data)-1)):
        data['y_value'][i] = data['price_mean'][i+1]
        
    data['y_value'] = data['y_value'].astype('float')
    
    # y값 lag변수 추가
    data['lag1_price'] = data['y_value'].shift(1)
    data['lag2_price'] = data['y_value'].shift(2)
    data['lag3_price'] = data['y_value'].shift(3)
    data['lag5_price'] = data['y_value'].shift(5)
    data['lag10_price'] = data['y_value'].shift(10)
    data['lag15_price'] = data['y_value'].shift(15)

    # 원본 데이터의 '한우가격' 삭제
    del data['price_mean']

    # lag변수로 인해 생기는 결측치 제거
    data = data.iloc[15:len(data),]
    data = data.reset_index()
    data = data.fillna(method = 'ffill')
    
    del data['index']

    # train, test data 나누기 -> 이것도 데이터업데이트할 때마다 바꿔주어야할 것 같은데..
    train, test = train_test_split(data, test_size=0.3, random_state=123, shuffle = False)
    
    # 첫번째 feature normailization -> 칼럼명 전처리 코드에 맞게 변경해줘야함!
    scaler = MinMaxScaler()
    train_x = scaler.fit_transform(train.drop(['week_date','y_value'],axis=1))
    test_x = scaler.transform(test.drop(['week_date','y_value'],axis=1))
    train_y = scaler.fit_transform(pd.DataFrame(train['y_value']))
    test_y = scaler.transform(pd.DataFrame(test['y_value']))

    feature_names = list(data.drop(['week_date','y_value'],axis=1).columns)

    # Feature Selection
    clf = linear_model.LinearRegression()
    # 선정된 모델에 맞는 feature selection 수행
    sfs1 = sfs(clf,k_features = 5,forward=True,floating=False, scoring='r2',cv=5)
    sfs1 = sfs1.fit(train_x, train_y,custom_feature_names=feature_names)
    
    # selected feature 출력
    features = list(sfs1.k_feature_names_)

    # 선정된 feature로 다시 Feature Normalization
    train_x = scaler.fit_transform(train[features])
    test_x = scaler.transform(test[features])
    train_y= scaler.fit_transform(pd.DataFrame(train['y_value']))
    test_y= scaler.transform(pd.DataFrame(test['y_value']))

    # LSTM input에 맞게 3차원 timestep 추가해서 array 형태로 변환
    train_X = train_x.reshape(train_x.shape[0], 1, train_x.shape[1])
    test_X = test_x.reshape(test_x.shape[0], 1, test_x.shape[1])

    # train the model
    K.clear_session()     # tensorflow의 graph 영역을 clear한다.

    xInput = Input(batch_shape=(None, train_X.shape[1], train_X.shape[2]))
    xLstm_1 = LSTM(10, return_sequences = True)(xInput)
    xLstm_2 = Bidirectional(LSTM(10))(xLstm_1)
    xOutput = Dense(1)(xLstm_2)

    model = Model(xInput, xOutput)
    model.compile(loss='mse', optimizer='adam')
    model.fit(train_X, train_y, epochs=500, batch_size=20,verbose=1)

    # predict
    y_hat = model.predict(test_X, batch_size=1)
    y_hat = scaler.inverse_transform(y_hat)
    
    # save the model
    #joblib.dump(model, '백엔드_디렉토리_경로/model.pkl')- 백앤드에 해당 경로 입력해주라고 말해주기
    
    #미래 예측값 1개 return
    return y_hat[-1]

if __name__ == '__main__':
    print(transform(data))
