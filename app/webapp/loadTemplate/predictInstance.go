package loadTemplate

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"strings"
)

func PredictInstance(w http.ResponseWriter, r *http.Request) {
	var err error

	var status int  // status coded from API
	var rmsg string // message returned from API

	var smsg string // success message
	var emsg string // error message

	activeItem := "Predict Instance"
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
		tpl.ExecuteTemplate(w, "predictInstance.gohtml", data)
	} else {
		f, _, err1 := r.FormFile("form")
		if err1 != nil {
			data.Message = fmt.Sprintf("Error: File not found.")
			tpl.ExecuteTemplate(w, "predictInstance.gohtml", data)
			return
		}
		defer f.Close()

		// Encodes json data as base64
		f.Seek(0, 0)
		buf := bytes.NewBuffer(nil)
		if _, err = io.Copy(buf, f); err != nil {
			data.Message = fmt.Sprintf("Error: File not valid.")
			http.Error(w, err.Error(), http.StatusInternalServerError)
			tpl.ExecuteTemplate(w, "predictInstance.gohtml", data)
			return
		}

		mn_form, ok := r.Form["model_name"]
		jsonPayload := strings.Replace(string(buf.Bytes()), "\n", "", -1) // read json and substitute '\n'
		model_name := mn_form[0]
		if !ok || len(model_name) == 0 {
			model_name = "default_model"
			smsg = fmt.Sprintf("Sent [Instance Predict Request] with default model. ")
			emsg = fmt.Sprintf("Error processing [Instance Predict Request] with default model. ")
		} else {
			smsg = fmt.Sprintf("Sent [Instance Predict Request] with [%s] model. ", model_name)
			emsg = fmt.Sprintf("Error processing [Instance Predict Request] with default model. ")
		}
		// Sends encoded data
		if rmsg, status, err = sendInstancePredictRequest(model_name, jsonPayload, w, r); err == nil {
			if status == 200 {
				smsg = smsg + fmt.Sprintf("Return from API: '%s'.", rmsg)
				data.Message = smsg
				linfo.Println(smsg)
			} else {
				emsg = emsg + fmt.Sprintf("Return from API: '%s'.", rmsg)
				data.Message = emsg
				lerror.Println(smsg)
			}
		} else {
			data.Message = emsg
			lerror.Println(emsg)
		}
		tpl.ExecuteTemplate(w, "predictInstance.gohtml", data)
	}
}
