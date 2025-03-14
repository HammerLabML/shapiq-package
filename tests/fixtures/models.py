"""This fixtures module contains model fixtures for the tests."""

from typing import Any

import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression
from sklearn.ensemble import IsolationForest, RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

NR_FEATURES = 7  # Number of features for the tabular models

TABULAR_MODEL_FIXTURES = [
    ("custom_model", "custom_model"),
    ("lr_reg_model", "sklearn.linear_model.LinearRegression"),
    ("lr_clf_model", "sklearn.linear_model.LogisticRegression"),
]

TABULAR_TENSORFLOW_MODEL_FIXTURES = [
    ("sequential_model_1_class", "tensorflow.python.keras.engine.sequential.Sequential"),
    ("sequential_model_2_classes", "keras.src.models.sequential.Sequential"),
    ("sequential_model_3_classes", "keras.engine.sequential.Sequential"),
]

TABULAR_TORCH_MODEL_FIXTURES = [
    ("torch_clf_model", "torch.nn.modules.container.Sequential"),
    ("torch_reg_model", "torch.nn.modules.container.Sequential"),
]

TREE_MODEL_FIXTURES = [
    ("lightgbm_reg_model", "lightgbm.sklearn.LGBMRegressor"),
    ("xgboost_regressor", "xgboost.sklearn.XGBRegressor"),
    ("xgboost_booster", "xgboost.core.Booster"),
    ("lightgbm_basic", "lightgbm.basic.Booster"),
    ("rf_reg_model", "sklearn.ensemble.RandomForestRegressor"),
    ("rf_clf_model", "sklearn.ensemble.RandomForestClassifier"),
    ("dt_clf_model", "sklearn.tree.DecisionTreeClassifier"),
    ("dt_reg_model", "sklearn.tree.DecisionTreeRegressor"),
]


class CustomModel:
    def __init__(self, data: tuple[np.ndarray, np.ndarray]):
        self.data = data

    def __call__(self, *args, **kwargs):
        return self.data[1]


@pytest.fixture
def custom_model(background_reg_dataset) -> CustomModel:
    """Return a callable mock custom model"""
    return CustomModel(background_reg_dataset)


@pytest.fixture
def xgboost_regressor(background_reg_dataset):
    """Return a xgb regression model"""
    import xgboost as xgb

    X, y = background_reg_dataset
    model = xgb.XGBRegressor(n_estimators=10, max_depth=1)
    model.fit(X, y, verbose=False)
    return model


@pytest.fixture
def xgboost_booster(background_reg_dataset):
    """Return a xgb booster"""
    import xgboost as xgb

    X, y = background_reg_dataset
    dtrain = xgb.DMatrix(X, label=y)
    params = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7}
    booster = xgb.train(params=params, dtrain=dtrain, num_boost_round=0)
    return booster


@pytest.fixture
def lightgbm_basic(background_reg_dataset):
    """Return a lgm basic booster"""
    import lightgbm as lgb

    X, y = background_reg_dataset
    train_data = lgb.Dataset(X, label=y)
    model = lgb.train(params={}, train_set=train_data, num_boost_round=1)
    return model


@pytest.fixture
def sequential_model_1_class():
    """Return a keras nn with output dimension 1"""
    return _sequential_model(1)


@pytest.fixture
def sequential_model_2_classes():
    """Return a keras nn with output dimension 2"""
    return _sequential_model(2)


@pytest.fixture
def sequential_model_3_classes():
    """Return a keras nn with output dimension 3"""
    return _sequential_model(3)


def _sequential_model(output_shape_nr):
    """Return a keras nn with specified output dimension"""
    import keras

    model = keras.Sequential(
        [
            keras.layers.Input(shape=(NR_FEATURES,)),
            keras.layers.Dense(2, activation="relu", name="layer1"),
            keras.layers.Dense(output_shape_nr, name="layer2"),
        ]
    )
    model.compile(optimizer="adam", loss="mse")
    X, y = make_regression(n_samples=100, n_features=NR_FEATURES, random_state=42)
    model.fit(X, y, epochs=0, batch_size=32)
    return model


@pytest.fixture
def xgb_reg_model():
    """Return a simple xgboost regression model."""
    from xgboost import XGBRegressor

    X, y = make_regression(n_samples=100, n_features=7, random_state=42)
    model = XGBRegressor(random_state=42, n_estimators=3)
    model.fit(X, y)
    return model


@pytest.fixture
def rf_clf_binary_model() -> RandomForestClassifier:
    """Return a simple random forest model."""
    X, y = make_classification(
        n_samples=100,
        n_features=NR_FEATURES,
        random_state=42,
        n_classes=2,
        n_informative=7,
        n_repeated=0,
        n_redundant=0,
    )
    model = RandomForestClassifier(random_state=42, max_depth=3, n_estimators=3)
    model.fit(X, y)
    return model


@pytest.fixture
def xgb_clf_model():
    """Return a simple xgboost classification model."""
    from xgboost import XGBClassifier

    X, y = make_classification(
        n_samples=100,
        n_features=NR_FEATURES,
        random_state=42,
        n_classes=3,
        n_informative=7,
        n_repeated=0,
        n_redundant=0,
    )
    model = XGBClassifier(random_state=42, n_estimators=3)
    model.fit(X, y)
    return model


@pytest.fixture
def torch_clf_model():
    """Return a simple torch model."""
    import torch

    model = torch.nn.Sequential(
        torch.nn.Linear(7, 10),
        torch.nn.ReLU(),
        torch.nn.Linear(10, 3),
    )
    model.eval()
    return model


@pytest.fixture
def torch_reg_model():
    """Return a simple torch model."""
    import torch

    model = torch.nn.Sequential(
        torch.nn.Linear(7, 10),
        torch.nn.ReLU(),
        torch.nn.Linear(10, 1),
    )
    model.eval()
    return model


@pytest.fixture
def tabpfn_classification_problem() -> tuple[Any, np.ndarray, np.ndarray, np.ndarray]:
    """Returns a very simple tabpfn classifier and dataset."""
    from tabpfn import TabPFNClassifier

    data, labels = make_classification(n_samples=10, n_features=3, random_state=42, n_redundant=1)
    data, x_test, labels, _ = train_test_split(data, labels, random_state=42, train_size=8)
    model = TabPFNClassifier()
    model.fit(data, labels)
    return model, data, labels, x_test


@pytest.fixture
def tabpfn_regression_problem() -> tuple[Any, np.ndarray, np.ndarray, np.ndarray]:
    """Returns a very simple tabpfn regressor and dataset."""
    from tabpfn import TabPFNRegressor

    data, labels = make_regression(n_samples=10, n_features=3, random_state=42)
    data, x_test, labels, _ = train_test_split(data, labels, random_state=42, train_size=8)
    model = TabPFNRegressor()
    model.fit(data, labels)
    return model, data, labels, x_test


@pytest.fixture
def dt_reg_model() -> DecisionTreeRegressor:
    """Return a simple decision tree model."""
    X, y = make_regression(n_samples=100, n_features=NR_FEATURES, random_state=42)
    model = DecisionTreeRegressor(random_state=42, max_depth=3)
    model.fit(X, y)
    return model


@pytest.fixture
def dt_clf_model() -> DecisionTreeClassifier:
    """Return a simple decision tree model."""
    X, y = make_classification(
        n_samples=100,
        n_features=NR_FEATURES,
        random_state=42,
        n_classes=3,
        n_informative=7,
        n_repeated=0,
        n_redundant=0,
    )
    model = DecisionTreeClassifier(random_state=42, max_depth=3)
    model.fit(X, y)
    return model


@pytest.fixture
def lr_clf_model() -> LogisticRegression:
    """Return a simple logistic regression model."""
    X, y = make_classification(
        n_samples=100,
        n_features=7,
        random_state=42,
        n_classes=3,
        n_informative=7,
        n_repeated=0,
        n_redundant=0,
    )
    model = LogisticRegression(random_state=42, max_iter=200)
    model.fit(X, y)
    return model


@pytest.fixture
def lr_reg_model() -> LinearRegression:
    """Return a simple linear regression model."""
    X, y = make_regression(n_samples=100, n_features=7, random_state=42)
    model = LinearRegression()
    model.fit(X, y)
    return model


@pytest.fixture
def lightgbm_reg_model():
    """Return a simple lightgbm regression model."""
    from lightgbm import LGBMRegressor

    X, y = make_regression(n_samples=100, n_features=NR_FEATURES, random_state=42)
    model = LGBMRegressor(random_state=42, n_estimators=3)
    model.fit(X, y)
    return model


@pytest.fixture
def lightgbm_clf_model():
    """Return a simple lightgbm classification model."""
    from lightgbm import LGBMClassifier

    X, y = make_classification(
        n_samples=100,
        n_features=NR_FEATURES,
        random_state=42,
        n_classes=3,
        n_informative=7,
        n_repeated=0,
        n_redundant=0,
    )
    model = LGBMClassifier(random_state=42, n_estimators=3)
    model.fit(X, y)
    return model


@pytest.fixture
def dt_clf_model_tree_model():
    """Return a simple decision tree as a TreeModel."""
    from shapiq.explainer.tree.validation import validate_tree_model

    X, y = make_classification(
        n_samples=100,
        n_features=NR_FEATURES,
        random_state=42,
        n_classes=3,
        n_informative=7,
        n_repeated=0,
        n_redundant=0,
    )
    model = DecisionTreeClassifier(random_state=42, max_depth=3)
    model.fit(X, y)
    tree_model = validate_tree_model(model)
    return tree_model


@pytest.fixture
def rf_reg_model() -> RandomForestRegressor:
    """Return a simple random forest model."""
    X, y = make_regression(n_samples=100, n_features=7, random_state=42)
    model = RandomForestRegressor(random_state=42, max_depth=3, n_estimators=3)
    model.fit(X, y)
    return model


@pytest.fixture
def rf_clf_model() -> RandomForestClassifier:
    """Return a simple (classification) random forest model."""
    X, y = make_classification(
        n_samples=100,
        n_features=NR_FEATURES,
        random_state=42,
        n_classes=3,
        n_informative=7,
        n_repeated=0,
        n_redundant=0,
    )
    model = RandomForestClassifier(random_state=42, max_depth=3, n_estimators=3)
    model.fit(X, y)
    return model


# Isolationforest model
@pytest.fixture
def if_clf_model(if_clf_dataset) -> IsolationForest:
    """Return a simple isolation forest model."""
    X, y = if_clf_dataset

    # X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    model = IsolationForest(random_state=42, n_estimators=3)
    model.fit(X, y)
    return model
