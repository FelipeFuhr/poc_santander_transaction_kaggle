package loadTemplate

import (
	"fmt"
	"net/http"
)

func UploadModel(w http.ResponseWriter, r *http.Request) {
	activeItem := "Upload Model"
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
		tpl.ExecuteTemplate(w, "uploadModel.gohtml", data)
	} else {
		f, _, err := r.FormFile("form")
		if err != nil {
			msg := fmt.Sprintf("Error: File not found.")
			data.Message = msg
			tpl.ExecuteTemplate(w, "uploadModel.gohtml", data)
			return
		}
		defer f.Close()

		mn_form, ok := r.Form["model_name"]
		model_name := mn_form[0]
		if !ok {
			data.Message = fmt.Sprintf("Sent Upload Request with default model.")
		} else {
			data.Message = fmt.Sprintf("Sent Upload Request with %s model.", model_name)
		}
		tpl.ExecuteTemplate(w, "uploadModel.gohtml", data)
	}
}
