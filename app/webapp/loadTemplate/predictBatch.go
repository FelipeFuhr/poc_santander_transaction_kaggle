package loadTemplate

import (
	"bytes"
	"encoding/base64"
	"fmt"
	"io"
	"net/http"
)

func PredictBatch(w http.ResponseWriter, r *http.Request) {
	activeItem := "Predict Batch"
	data := struct {
		Hd      HeaderData
		Message string
		Fd      FooterData
	}{
		HeaderData{
			activeItem,
		},
		"",
		FooterData{
			activeItem,
		},
	}

	if r.Method == "GET" {
		tpl.ExecuteTemplate(w, "predictBatch.gohtml", data)
	} else {
		f, _, err := r.FormFile("form")
		if err != nil {
			msg := fmt.Sprintf("Error: File not found.")
			data.Message = msg
			tpl.ExecuteTemplate(w, "predictBatch.gohtml", data)
			return
		}
		defer f.Close()

		// Encodes csv file to send to api endpoint
		f.Seek(0, 0)
		buf := bytes.NewBuffer(nil)
		if _, err := io.Copy(buf, f); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		dataEncoded := base64.StdEncoding.EncodeToString(buf.Bytes())

		mn_form, ok := r.Form["model_name"]
		model_name := mn_form[0]
		if !ok {
			data.Message = fmt.Sprintf("Sent Predict Batch Request with default model %s.")
			// Sends encoded data
			sendBatchPredictRequest("default_model", dataEncoded, w, r)
		} else {
			data.Message = fmt.Sprintf("Sent Predict Batch Request with %s model.", model_name)
			sendBatchPredictRequest(model_name, dataEncoded, w, r)
		}
		tpl.ExecuteTemplate(w, "predictBatch.gohtml", data)
	}
}
