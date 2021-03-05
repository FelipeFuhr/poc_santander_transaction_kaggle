package loadTemplate

import (
	"net/http"
)

func Index(w http.ResponseWriter, r *http.Request) {
	activeItem := "Home"
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
	tpl.ExecuteTemplate(w, "index.gohtml", data)
}
