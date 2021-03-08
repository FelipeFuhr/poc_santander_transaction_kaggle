# POC Santander Transaction - Kaggle Competition

MLOps Proof of Concept using the Santander Transaction Competition as basis.

ref: https://www.kaggle.com/c/santander-customer-transaction-prediction/overview

## Things still missing:
- Good Tests
- Kubernetes
- Communication with / Run on AWS

## Data EDA and Selection

The Data EDA is made in the data_eda.ipynb notebook. The Model Selection is made on the model_selection.ipynb notebook. These notebooks are inside the notebooks folder.

## Model Api

Model API is the application responsible for providing the model endpoints. It allows the user to update the model and to make predictions.

## Webapp

Model API is a webapp made in golang that communicates with the API endpoints.

## How to Run it

One way to run it is to run the following command inside the app folder:

```
$ docker-compose up --build --force-recreate --no-deps -d
```

After this, the default port for the webapp is 9000 and the port for the API is 9001

Example used: 
    example_value_0.json


