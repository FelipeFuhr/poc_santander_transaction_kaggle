package loadTemplate

import (
	"html/template"
	"log"
	"os"
)

var (
	linfo    *log.Logger
	lwarning *log.Logger
	lerror   *log.Logger
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
	linfo = log.New(os.Stdout, "INFO: ", log.Ldate|log.Ltime|log.Lshortfile)
	lwarning = log.New(os.Stdout, "WARNING: ", log.Ldate|log.Ltime|log.Lshortfile)
	lerror = log.New(os.Stdout, "ERROR: ", log.Ldate|log.Ltime|log.Lshortfile)
}
