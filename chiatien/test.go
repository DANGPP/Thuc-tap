package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"helm.sh/helm/v3/pkg/action"
	"helm.sh/helm/v3/pkg/chart/loader"
	"helm.sh/helm/v3/pkg/cli"
)

var (
	namespace   = "chiatien-ver2-hehe"
	releaseName = "chiatien"
	chartPath   = "./chiatien-chart"
	kubeContext = "docker-desktop"
)

// Sample request payload structure
type DeployRequest struct {
	Values map[string]interface{} `json:"values"`
}

func main() {
	http.HandleFunc("/deploy", handleDeploy)
	http.HandleFunc("/upgrade", handleUpgrade)
	http.HandleFunc("/uninstall", handleUninstall)
	log.Println("🚀 Server started on :8085")
	http.ListenAndServe(":8085", nil)
}

func getActionConfig() (*action.Configuration, error) {
	settings := cli.New()
	settings.KubeContext = kubeContext
	actionConfig := new(action.Configuration)
	if err := actionConfig.Init(settings.RESTClientGetter(), namespace, os.Getenv("HELM_DRIVER"), log.Printf); err != nil {
		return nil, err
	}
	return actionConfig, nil
}

func handleDeploy(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req DeployRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	actionConfig, err := getActionConfig()
	if err != nil {
		http.Error(w, fmt.Sprintf("Init error: %v", err), http.StatusInternalServerError)
		return
	}

	chart, err := loader.Load(chartPath)
	if err != nil {
		http.Error(w, fmt.Sprintf("Load chart error: %v", err), http.StatusInternalServerError)
		return
	}

	install := action.NewInstall(actionConfig)
	install.ReleaseName = releaseName
	install.Namespace = namespace
	install.CreateNamespace = true
	install.DryRun = false
	install.Wait = false
	install.Timeout = 10 * time.Minute

	release, err := install.Run(chart, req.Values)
	if err != nil {
		http.Error(w, fmt.Sprintf("Deploy error: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "success",
		"release": release.Name,
	})
}

func handleUpgrade(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req DeployRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	actionConfig, err := getActionConfig()
	if err != nil {
		http.Error(w, fmt.Sprintf("Init error: %v", err), http.StatusInternalServerError)
		return
	}

	chart, err := loader.Load(chartPath)
	if err != nil {
		http.Error(w, fmt.Sprintf("Load chart error: %v", err), http.StatusInternalServerError)
		return
	}

	upgrade := action.NewUpgrade(actionConfig)
	upgrade.Namespace = namespace
	upgrade.Wait = true
	upgrade.Timeout = 10 * time.Minute

	release, err := upgrade.Run(releaseName, chart, req.Values)
	if err != nil {
		http.Error(w, fmt.Sprintf("Upgrade error: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "upgraded",
		"release": release.Name,
	})
}

func handleUninstall(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	actionConfig, err := getActionConfig()
	if err != nil {
		http.Error(w, fmt.Sprintf("Init error: %v", err), http.StatusInternalServerError)
		return
	}

	uninstall := action.NewUninstall(actionConfig)
	_, err = uninstall.Run(releaseName)
	if err != nil {
		http.Error(w, fmt.Sprintf("Uninstall error: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "uninstalled",
		"release": releaseName,
	})
}
