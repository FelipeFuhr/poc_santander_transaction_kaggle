package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	// db "database"
	lt "loadTemplate"
)

func init() {
	// Loads template and template-part .gohtml files
}

func main() {
	// declares a Serve Mux and Server
	m := http.NewServeMux()
	s := http.Server{Addr: ":9000", Handler: m}
	// config.ServerAddress, Handler: m}

	// Serve css, javascript and image files
	serveAssets(m)

	// Treats system interruptions for proper shutdown
	sysi := make(chan os.Signal, 1)
	signal.Notify(sysi, syscall.SIGINT, syscall.SIGTERM)
	go func(s *http.Server) {
		<-sysi
		doShutdown(s)
	}(&s)

	// Routing
	m.HandleFunc("/", lt.Index)
	m.HandleFunc("/predict-instance", lt.PredictInstance)
	m.HandleFunc("/predict-batch", lt.PredictBatch)
	m.HandleFunc("/upload-model", lt.UploadModel)
	m.HandleFunc("/train-model", lt.TrainModel)

	// Listen and Serve with Transport Layer Security
	log.Fatal(s.ListenAndServe())
}

func doShutdown(s *http.Server) {
	log.Println("Shutting Down Application.")
	if err := s.Shutdown(context.Background()); err != http.ErrServerClosed {
		log.Fatal(err)
	}
	return
}

func serveAssets(m *http.ServeMux) {
	// Serve css files
	m.Handle("/css/", http.StripPrefix("/css/",
		http.FileServer(http.Dir("template/assets/css"))))
	// Serve image files
	m.Handle("/img/", http.StripPrefix("/img/",
		http.FileServer(http.Dir("template/assets/images"))))
	// Serve javascript files
	m.Handle("/js/", http.StripPrefix("/js/",
		http.FileServer(http.Dir("template/assets/js"))))
}
