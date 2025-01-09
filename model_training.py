# model_training.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle

# 1. Laad de dataset
df = pd.read_csv('heart.csv')  # Zorg ervoor dat je het juiste pad naar je dataset gebruikt

# 2. Scheid features (X) en target (y)
X = df.drop('target', axis=1)  # Veronderstelt dat 'target' de naam is van je doelvariabele
y = df['target']

# 3. Split de data in training en test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Maak en train het model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# 5. Evalueer het model (optioneel)
score = model.score(X_test, y_test)
print(f"Model nauwkeurigheid: {score}")

# 6. Sla het model op
with open('modal2.pkl', 'wb') as file:
    pickle.dump(model, file)