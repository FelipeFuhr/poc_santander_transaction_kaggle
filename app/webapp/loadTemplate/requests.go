package loadTemplate

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"net/http"
)

var modelApiAddress = "http://model-api:9001"

type InstanceRequest struct {
	Model_name string `json:"model_name"`
	Data       string `json:"data"`
}

type UploadRequest struct {
	Model_name string `json:"model_name"`
	Model      string `json:"model"`
}

type TrainRequest struct {
	Model_name string `json:"model_name"`
	Data       string `json:"data"`
	Retrain    int    `json:"retrain"`
}

type GenericResponse struct {
	Message string
}

func sendInstancePredictRequest(model_name string, data string, w http.ResponseWriter, r *http.Request) (string, int, error) {
	job, err := json.Marshal(InstanceRequest{model_name, data})
	if err != nil {
		return "", -1, err
	}

	resp, err := http.Post(modelApiAddress+"/instance_predict", "application/json", bytes.NewBuffer(job))
	if err != nil {
		return "", -1, err
	}

	// Extracts Body from above Post Response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", -1, err
	}

	// Unmarshal Json
	var gr GenericResponse
	if err = json.Unmarshal(body, &gr); err != nil {
		return "", -1, err
	}

	return gr.Message, resp.StatusCode, nil
}

func sendUploadModelRequest(model_name string, model string, w http.ResponseWriter, r *http.Request) (string, int, error) {
	job, err := json.Marshal(UploadRequest{model_name, model})
	if err != nil {
		return "", -1, err
	}

	resp, err := http.Post(modelApiAddress+"/upload_model", "application/json", bytes.NewBuffer(job))
	if err != nil {
		return "", -1, err
	}

	// Extracts Body from above Post Response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", -1, err
	}

	// Unmarshal Json
	var gr GenericResponse
	if err = json.Unmarshal(body, &gr); err != nil {
		return "", -1, err
	}

	return gr.Message, resp.StatusCode, nil
}

func sendBatchPredictRequest(model_name string, data string, w http.ResponseWriter, r *http.Request) (string, error) {
	job, err := json.Marshal(InstanceRequest{model_name, data})
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		lerror.Println("Error Marshalling payload")
		return "", err
	}
	_, err = http.Post(modelApiAddress+"/batch_predict", "application/json", bytes.NewBuffer(job))
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		lerror.Println("Error Sending Payload")
		return "", err
	}

	return "", nil
}

func sendTrainModelRequest(model_name string, data string, retrain int, w http.ResponseWriter, r *http.Request) (string, int, error) {
	job, err := json.Marshal(TrainRequest{model_name, data, int(retrain)})
	if err != nil {
		return "", -1, err
	}

	resp, err := http.Post(modelApiAddress+"/train_model", "application/json", bytes.NewBuffer(job))
	if err != nil {
		return "", -1, err
	}

	// Extracts Body from above Post Response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", -1, err
	}

	// Unmarshal Json
	var gr GenericResponse
	if err = json.Unmarshal(body, &gr); err != nil {
		return "", -1, err
	}

	return gr.Message, resp.StatusCode, nil
}
