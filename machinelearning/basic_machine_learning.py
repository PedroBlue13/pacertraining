from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

print("Acurácia:", model.score(X_test, y_test))
