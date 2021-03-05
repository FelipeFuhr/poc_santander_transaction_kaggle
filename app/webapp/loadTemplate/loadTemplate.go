package loadTemplate

import (
	"html/template"
)

var tpl *template.Template

type HeaderData struct {
	ActiveItem string
}

type FooterData struct {
	ActiveItem string
}

func init() {
	tpl = template.Must(template.ParseGlob("template/[a-z]*.gohtml"))
	template.Must(tpl.ParseGlob("template/template-parts/[a-z]*.gohtml"))
}
