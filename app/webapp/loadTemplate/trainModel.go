package loadTemplate

import (
	"bytes"
	"encoding/base64"
	"fmt"
	"io"
	"net/http"
)

func TrainModel(w http.ResponseWriter, r *http.Request) {
	var err error

	var status int  // status coded from API
	var rmsg string // message returned from API

	var smsg string // success message
	var emsg string // error message

	activeItem := "Train Model"
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
		tpl.ExecuteTemplate(w, "trainModel.gohtml", data)
	} else {
		f, _, err1 := r.FormFile("form")
		if err1 != nil {
			data.Message = fmt.Sprintf("Error: File not found.")
			tpl.ExecuteTemplate(w, "trainModel.gohtml", data)
			return
		}
		defer f.Close()

		// Encodes data as base64
		f.Seek(0, 0)
		buf := bytes.NewBuffer(nil)
		if _, err = io.Copy(buf, f); err != nil {
			data.Message = fmt.Sprintf("Error: File not valid.")
			http.Error(w, err.Error(), http.StatusInternalServerError)
			tpl.ExecuteTemplate(w, "trainModel.gohtml", data)
			return
		}
		// Encodes model to Base64
		datab64 := base64.StdEncoding.EncodeToString(buf.Bytes())
		mn_form, ok := r.Form["model_name"]
		model_name := mn_form[0]
		if !ok {
			model_name = "default_model"
			smsg = fmt.Sprintf("Sent [Train Model Request] with default model. ")
			emsg = fmt.Sprintf("Error processing [Train Model Request] with default model. ")
		} else {
			smsg = fmt.Sprintf("Sent [Train Model Request] with [%s] model. ", model_name)
			emsg = fmt.Sprintf("Error processing [Train Model Request] with default model. ")
		}

		if rmsg, status, err = sendTrainModelRequest(model_name, datab64, w, r); err == nil {
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
		tpl.ExecuteTemplate(w, "trainModel.gohtml", data)
	}
}
