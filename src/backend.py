from fastapi import FastAPI, Request, Response, status
import pickle

app = FastAPI()
model_path = 'model/classifier.pkl'

@app.get("/")
def root():
    return {"message": "Your API is UP!"}


#check model
@app.get("/check-model")
def check_model(response: Response):
    try:
        with open(model_path, 'rb') as model:
            model = pickle.load(model)
            result = {'status': 'ok', 'message': 'model is ready to use'}
            return result
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'status': 'error', 'message': 'model is not found', 'detail_error': str(e)}
@app.post("/predict")
async def predict(response: Response, request: Request):
    try:
        data = await request.json()
        sepal_length = data['sepal_length']
        sepal_width = data['sepal_width']
        petal_length = data['petal_length']
        petal_width = data['petal_width']

        with open(model_path, 'rb') as model:
            model = pickle.load(model)
 
        #label prediction
        label = ['iris-setosa', 'iris-versicolor', 'iris-virginica']
    
        #predict
        try:
            result = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
            result = label[result[0]]
            return {
                'status': 'ok',
                'message': 'return prediction',
                'result': str(result)
            }
        except Exception as e:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'status': 'error', 'message': 'data invalid', 'detail_error': str(e)}

    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'status': 'error', 'message': 'model is not found', 'detail_error': str(e)}
