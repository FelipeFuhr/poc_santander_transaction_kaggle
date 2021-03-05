package loadTemplate

import (
	"fmt"
	"net/http"
)

func TrainModel(w http.ResponseWriter, r *http.Request) {
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
		f, _, err := r.FormFile("form")
		if err != nil {
			msg := fmt.Sprintf("Error: File not found.")
			data.Message = msg
			tpl.ExecuteTemplate(w, "trainModel.gohtml", data)
			return
		}
		defer f.Close()

		mn_form, mn_ok := r.Form["model_name"]
		model_name := mn_form[0]
		if !mn_ok {
			data.Message = fmt.Sprintf("Error: Model Name required.")
		} else {
			_, ok := r.Form["retrain_model"]
			if ok {
				data.Message = fmt.Sprintf("Sent Retrain Model Request with %s model.", model_name)
			} else {
				data.Message = fmt.Sprintf("Sent Train Model Request with %s model.", model_name)
			}
		}
		tpl.ExecuteTemplate(w, "trainModel.gohtml", data)
	}
}
