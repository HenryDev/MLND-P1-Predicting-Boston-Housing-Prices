"""Load the Boston dataset and examine its target (label) distribution."""

# Load libraries
import numpy as np
import pylab as pl
from sklearn import datasets
from sklearn.tree import DecisionTreeRegressor
from sklearn import cross_validation
from sklearn import metrics
from sklearn.grid_search import GridSearchCV
from sklearn.neighbors import NearestNeighbors


def load_data():
    """Load the Boston dataset."""
    boston = datasets.load_boston()
    return boston


def explore_city_data(city_data):
    """Calculate the Boston housing statistics."""

    # Get the labels and features from the housing data
    housing_prices = city_data.target
    housing_features = city_data.data

    # Please calculate the following values using the Numpy library
    # Size of data (number of houses)?
    print "number of data points:"
    print housing_features.size

    # Number of features?
    print "features count:"
    print housing_features.shape[1]

    # Minimum price?
    print "minimum price:"
    print min(housing_prices)

    # Maximum price?
    print "max price:"
    print max(housing_prices)

    # Calculate mean price?
    print "mean price:"
    print np.mean(housing_prices)

    # Calculate median price?
    print "median price:"
    print np.median(housing_prices)

    # Calculate standard deviation?
    print "standard deviation:"
    print np.std(housing_prices)

    q75 = np.percentile(housing_prices, 75)
    q25 = np.percentile(housing_prices, 25)
    iqr = q75 - q25
    print "interquartile range:"
    print iqr

    outlier_count = 0
    for i in housing_prices:
        if i < q25 - 1.5 * iqr or i > q75 + 1.5 * iqr:
            outlier_count += 1
    print "outlier count:"
    print outlier_count


def split_data(city_data):
    """Randomly shuffle the sample set. Divide it into 70 percent training and 30 percent testing data."""

    # Get the features and labels from the Boston housing data
    X, y = city_data.data, city_data.target

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3)
    return X_train, y_train, X_test, y_test


def performance_metric(label, prediction):
    """Calculate and return the appropriate error performance metric."""

    # The following page has a table of scoring functions in sklearn:
    # http://scikit-learn.org/stable/modules/classes.html#sklearn-metrics-metrics

    return metrics.mean_absolute_error(label, prediction)
    # return metrics.mean_squared_error(label, prediction)
    # return metrics.median_absolute_error(label, prediction)
    # return metrics.r2_score(label, prediction)
    # return metrics.explained_variance_score(label, prediction)


def learning_curve(depth, X_train, y_train, X_test, y_test):
    """Calculate the performance of the model after a set of training data."""

    # We will vary the training set size so that we have 50 different sizes
    sizes = np.round(np.linspace(1, len(X_train), 50))
    train_err = np.zeros(len(sizes))
    test_err = np.zeros(len(sizes))

    print "Decision Tree with Max Depth: "
    print depth

    for i, s in enumerate(sizes):
        # Create and fit the decision tree regressor model
        regressor = DecisionTreeRegressor(max_depth=depth)
        regressor.fit(X_train[:s], y_train[:s])

        # Find the performance on the training and testing set
        train_err[i] = performance_metric(y_train[:s], regressor.predict(X_train[:s]))
        test_err[i] = performance_metric(y_test, regressor.predict(X_test))

    # Plot learning curve graph
    learning_curve_graph(sizes, train_err, test_err)


def learning_curve_graph(sizes, train_err, test_err):
    """Plot training and test error as a function of the training size."""

    pl.figure()
    pl.title('Decision Trees: Performance vs Training Size')
    pl.plot(sizes, test_err, lw=2, label='test error')
    pl.plot(sizes, train_err, lw=2, label='training error')
    pl.legend()
    pl.xlabel('Training Size')
    pl.ylabel('Error')
    pl.show()


def model_complexity(X_train, y_train, X_test, y_test):
    """Calculate the performance of the model as model complexity increases."""

    print "Model Complexity: "

    # We will vary the depth of decision trees from 2 to 25
    max_depth = np.arange(1, 25)
    train_err = np.zeros(len(max_depth))
    test_err = np.zeros(len(max_depth))

    for i, d in enumerate(max_depth):
        # Setup a Decision Tree Regressor so that it learns a tree with depth d
        regressor = DecisionTreeRegressor(max_depth=d)

        # Fit the learner to the training data
        regressor.fit(X_train, y_train)

        # Find the performance on the training set
        train_err[i] = performance_metric(y_train, regressor.predict(X_train))

        # Find the performance on the testing set
        test_err[i] = performance_metric(y_test, regressor.predict(X_test))

    # Plot the model complexity graph
    model_complexity_graph(max_depth, train_err, test_err)


def model_complexity_graph(max_depth, train_err, test_err):
    """Plot training and test error as a function of the depth of the decision tree learn."""

    pl.figure()
    pl.title('Decision Trees: Performance vs Max Depth')
    pl.plot(max_depth, test_err, lw=2, label='test error')
    pl.plot(max_depth, train_err, lw=2, label='training error')
    pl.legend()
    pl.xlabel('Max Depth')
    pl.ylabel('Error')
    pl.show()


def fit_predict_model(city_data):
    """Find and tune the optimal model. Make a prediction on housing data."""

    # Get the features and labels from the Boston housing data
    X, y = city_data.data, city_data.target

    # Setup a Decision Tree Regressor
    regressor = DecisionTreeRegressor()

    parameters = {'max_depth': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)}

    # 1. Find an appropriate performance metric. This should be the same as the
    # one used in your performance_metric procedure above:
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html

    scorer = metrics.make_scorer(metrics.mean_absolute_error, greater_is_better=False)

    # 2. We will use grid search to fine tune the Decision Tree Regressor and
    # obtain the parameters that generate the best training performance. Set up
    # the grid search object here.
    # http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV

    reg = GridSearchCV(estimator=regressor, param_grid=parameters, scoring=scorer, cv=50, n_jobs=-1)

    # Fit the learner to the training data to obtain the best parameter set
    print "Final Model: "
    print reg.fit(X, y)

    # Use the model to predict the output of a particular sample
    x = [11.95, 0.00, 18.100, 0, 0.6590, 5.6090, 90.00, 1.385, 24, 680.0, 20.20, 332.09, 12.13]
    y = reg.predict([x])
    print "House: " + str(x)
    print "Prediction: " + str(y)
    print "best estimator:"
    print reg.best_estimator_
    print "best params:"
    print reg.best_params_
    print "best score:"
    print reg.best_score_


def rinse_and_repeat(city_data):
    parameters = {'max_depth': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)}
    scorer = metrics.make_scorer(metrics.mean_absolute_error, greater_is_better=False)
    model = GridSearchCV(estimator=DecisionTreeRegressor(), param_grid=parameters, scoring=scorer, n_jobs=-1)
    model.fit(city_data.data, city_data.target)
    house = [11.95, 0.00, 18.100, 0, 0.6590, 5.6090, 90.00, 1.385, 24, 680.0, 20.20, 332.09, 12.13]
    prediction = model.predict([house])
    best_depth = model.best_params_['max_depth']
    return {'prediction': prediction[0], 'best_depth': best_depth}


def find_nearest_neighbor_indexes(features):
    neighbor_model = NearestNeighbors(n_neighbors=10)
    neighbor_model.fit(features)
    x = [11.95, 0.00, 18.100, 0, 0.6590, 5.6090, 90.00, 1.385, 24, 680.0, 20.20, 332.09, 12.13]
    distance, indices = neighbor_model.kneighbors([x])
    return indices


def main():
    """Analyze the Boston housing data. Evaluate and validate the
    performanance of a Decision Tree regressor on the housing data.
    Fine tune the model to make prediction on unseen data."""

    # Load data
    city_data = load_data()

    # Explore the data
    explore_city_data(city_data)

    # Training/Test dataset split
    X_train, y_train, X_test, y_test = split_data(city_data)

    # Learning Curve Graphs
    max_depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for max_depth in max_depths:
        learning_curve(max_depth, X_train, y_train, X_test, y_test)

    # Model Complexity Graph
    model_complexity(X_train, y_train, X_test, y_test)

    # Tune and predict Model
    fit_predict_model(city_data)

    aggregate_result = {'predictions': [], 'best_depths': []}
    for _ in range(30):
        result = rinse_and_repeat(city_data)
        aggregate_result['predictions'].append(result['prediction'])
        aggregate_result['best_depths'].append(result['best_depth'])
    depths = np.array(aggregate_result['best_depths'])
    predictions = np.array(aggregate_result['predictions'])

    print "best depths:"
    print depths
    print "depths mode:"
    print np.argmax(np.bincount(depths))
    print "predictions:"
    print predictions
    print "predictions average:"
    average_prediction = np.mean(predictions)
    print average_prediction

    indices = find_nearest_neighbor_indexes(city_data.data)
    neighbor_prices_total = []
    for i in indices:
        neighbor_prices_total.append(city_data.target[i])

    print "nearest neighbors average:"
    print np.mean(neighbor_prices_total)


if __name__ == "__main__":
    main()
