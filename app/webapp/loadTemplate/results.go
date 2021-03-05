package loadTemplate

import (
	"net/http"
)

func Results(w http.ResponseWriter, r *http.Request) {
	activeItem := "Results"
	data := struct {
		Hd HeaderData
		Fd FooterData
	}{
		HeaderData{
			activeItem,
		},
		FooterData{
			activeItem,
		},
	}
	tpl.ExecuteTemplate(w, "results.gohtml", data)
}
