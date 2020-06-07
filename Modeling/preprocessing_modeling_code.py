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
from mlxtend.feature_selection import ExhaustiveFeatureSelector as efs # 0.17.2 version

warnings.filterwarnings(action='ignore')

#################### 실시간으로 데이터 받아올 api 코드 입력####################
data = pd.merge(price, weather, on='주간날짜')

del data2['Unnamed: 0']
del data2['year']
del data2['month']
del data2['날짜']
data2 = data2.reset_index(drop=True)

# 원본 데이터의 '한우가격' 값 한칸씩 떙겨서 우리가 맞출려는 y_value 생성 
data['y_value'] = 1
for i in range(0,(len(data2)-1)):
    data['y_value'][i] = data['한우 평균경매 금액_주간평균'][i+1]
data['y_value'] = data['y_value'].astype('float')
data = data.dropna()

# y값 lag변수 추가
data['lag1_price'] = data['y_value'].shift(1)
data['lag2_price'] = data['y_value'].shift(2)
data['lag3_price'] = data['y_value'].shift(3)
data['lag5_price'] = data['y_value'].shift(5)
data['lag10_price'] = data['y_value'].shift(10)
data['lag15_price'] = data['y_value'].shift(15)

# 원본 데이터의 '한우가격' 삭제 
del data['한우 평균경매 금액_주간평균']
################### 여기까지 전처리 코드 입력 ################################

# train, test data 나누기 -> 이것도 데이터업데이트할 때마다 바꿔주어야할 것 같은데..
train = data.iloc[:690,:]
test = data.iloc[690:]

# 첫번째 feature normailization -> 칼럼명 전처리 코드에 맞게 변경해줘야함!
train_x = scaler.fit_transform(train.drop(['주간날짜','y_value'],axis=1))
test_x = scaler.transform(test.drop(['주간날짜','y_value'],axis=1))
train_y= scaler.fit_transform(pd.DataFrame(train['y_value']))
test_y= scaler.transform(pd.DataFrame(test['y_value']))

feature_names = data.drop(['주간날짜','y_value'],axis=1).columns
feature_names = [list(i) for i in feature_names]
feature_names = [''.join(i) for i in feature_names]

# Feature Selection
regression = linear_model.LinearRegression()
# 선정된 모델에 맞는 feature selection 수행
efs = efs(regression,
         min_features=3,
         max_features=12,
         scoring='r2',
         cv=5)

efs.fit(train_x, train_y,custom_feature_names=feature_names)
# selected feature 출력
features = list(efs.best_feature_names_)

# Feature Normalization
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
print('Model training is complete')

# predict
y_hat = model.predict(test_X, batch_size=1)
y_hat = scaler.inverse_transform(y_hat)
print(y_hat)

# save the model
file_name = 'cow_lstm.h5'
model.save(file_name)
print('Model is saved in', file_name)

#저장한 모델 사용할떄
# model = load_model('cow_lstm.h5')

