{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7bc3bbb9",
   "metadata": {},
   "outputs": [],
   "source": [
    "# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality\n",
    "# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.\n",
    "# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.\n",
    "\n",
    "import os\n",
    "import warnings\n",
    "import sys\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.linear_model import ElasticNet\n",
    "\n",
    "import mlflow\n",
    "import mlflow.sklearn\n",
    "\n",
    "\n",
    "def eval_metrics(actual, pred):\n",
    "    rmse = np.sqrt(mean_squared_error(actual, pred))\n",
    "    mae = mean_absolute_error(actual, pred)\n",
    "    r2 = r2_score(actual, pred)\n",
    "    return rmse, mae, r2\n",
    "\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    warnings.filterwarnings(\"ignore\")\n",
    "    np.random.seed(40)\n",
    "\n",
    "    # Read the wine-quality csv file (make sure you're running this from the root of MLflow!)\n",
    "    wine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), \"wine-quality.csv\")\n",
    "    data = pd.read_csv(wine_path)\n",
    "\n",
    "    # Split the data into training and test sets. (0.75, 0.25) split.\n",
    "    train, test = train_test_split(data)\n",
    "\n",
    "    # The predicted column is \"quality\" which is a scalar from [3, 9]\n",
    "    train_x = train.drop([\"quality\"], axis=1)\n",
    "    test_x = test.drop([\"quality\"], axis=1)\n",
    "    train_y = train[[\"quality\"]]\n",
    "    test_y = test[[\"quality\"]]\n",
    "\n",
    "    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5\n",
    "    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5\n",
    "\n",
    "    with mlflow.start_run():\n",
    "        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)\n",
    "        lr.fit(train_x, train_y)\n",
    "\n",
    "        predicted_qualities = lr.predict(test_x)\n",
    "\n",
    "        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)\n",
    "\n",
    "        print(\"Elasticnet model (alpha=%f, l1_ratio=%f):\" % (alpha, l1_ratio))\n",
    "        print(\"  RMSE: %s\" % rmse)\n",
    "        print(\"  MAE: %s\" % mae)\n",
    "        print(\"  R2: %s\" % r2)\n",
    "\n",
    "        mlflow.log_param(\"alpha\", alpha)\n",
    "        mlflow.log_param(\"l1_ratio\", l1_ratio)\n",
    "        mlflow.log_metric(\"rmse\", rmse)\n",
    "        mlflow.log_metric(\"r2\", r2)\n",
    "        mlflow.log_metric(\"mae\", mae)\n",
    "\n",
    "        mlflow.sklearn.log_model(lr, \"model\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}