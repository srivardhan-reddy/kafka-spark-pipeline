import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import pickle

# Load the data
df = pd.read_csv('fake_data.csv')

# Split the data into train and test sets
X = df.drop(['scattering_coefficient_b'], axis=1)
y = df['scattering_coefficient_b']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regressor
lr = LinearRegression()
lr.fit(X_train, y_train)

# Train the random forest regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Train the gradient boosting regressor
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb.fit(X_train, y_train)

# Save the trained models as pickle files
with open('lr_model.pkl', 'wb') as f:
    pickle.dump(lr, f)

with open('rf_model.pkl', 'wb') as f:
    pickle.dump(rf, f)
    
with open('gb_model.pkl', 'wb') as f:
    pickle.dump(gb, f)
