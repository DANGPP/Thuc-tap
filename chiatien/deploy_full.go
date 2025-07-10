package main

import (
	"fmt"
	"log"
	"os"

	"helm.sh/helm/v3/pkg/action"
	"helm.sh/helm/v3/pkg/chart"
	"helm.sh/helm/v3/pkg/chart/loader"
	"helm.sh/helm/v3/pkg/cli"
)

var (
	namespace   = "chiatien-ver2-hehe"
	releaseName = "chiatien"
	chartPath   = "./chiatien-chart"
	kubeContext = "docker-desktop"
)

var values = map[string]interface{}{
	"backend": map[string]interface{}{
		"image": "harbor.local:8080/dangdangtest/chiatien-backend-v2:latest",
		"env": map[string]interface{}{
			"POSTGRES_USER":         "postgres",
			"POSTGRES_PASSWORD":     "1",
			"POSTGRES_DB":           "postgres",
			"DB_HOST":               "flask-db",
			"DB_PORT":               "5432",
			"DB_USER":               "postgres",
			"DB_PASSWORD":           "1",
			"DB_NAME":               "postgres",
			"CELERY_BROKER_URL":     "redis://redis:6379/0",
			"CELERY_RESULT_BACKEND": "redis://redis:6379/1",
			"MAIL_SERVER":           "smtp.gmail.com",
			"MAIL_PORT":             "587",
			"MAIL_USE_TLS":          "True",
			"MAIL_USERNAME":         "maitiandewd@gmail.com",
			"MAIL_PASSWORD":         "brzo hedf veiy jksi",
			"MAIL_DEFAULT_SENDER":   "maitiandewd@gmail.com",
		},
		"ports": map[string]interface{}{
			"container": 5000,
			"service":   30101,
		},
	},
	"frontend": map[string]interface{}{
		"image": "harbor.local:8080/dangdangtest/chiatien-frontend-v2:latest",
		"ports": map[string]interface{}{
			"container": 3000,
			"service":   30100,
		},
	},
	"postgres": map[string]interface{}{
		"image": "postgres:16",
		"ports": map[string]interface{}{
			"container": 5432,
			"service":   5433,
		},
		"env": map[string]interface{}{
			"POSTGRES_USER":     "postgres",
			"POSTGRES_PASSWORD": "1",
			"POSTGRES_DB":       "postgres",
		},
	},
	"redis": map[string]interface{}{
		"image": "redis:7-alpine",
		"ports": map[string]interface{}{
			"container": 6379,
			"service":   6380,
		},
	},
	"celery": map[string]interface{}{
		"command": []interface{}{"celery", "-A", "celery_worker.celery", "worker", "--loglevel=info"},
	},
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("❗ Dùng: go run main.go [install|upgrade|delete]")
		os.Exit(1)
	}
	cmd := os.Args[1]

	settings := cli.New()
	settings.KubeContext = kubeContext

	actionConfig := new(action.Configuration)
	if err := actionConfig.Init(settings.RESTClientGetter(), namespace, os.Getenv("HELM_DRIVER"), log.Printf); err != nil {
		log.Fatalf("❌ Lỗi init Helm SDK: %v", err)
	}

	switch cmd {
	case "install":
		runInstall(actionConfig)
	case "upgrade":
		runUpgrade(actionConfig)
	case "delete":
		runDelete(actionConfig)
	case "list":
		runList(actionConfig)
	case "manifest":
		runGetManifest(actionConfig)
	case "history":
		runHistory(actionConfig)
	case "rollback":
		if len(os.Args) < 3 {
			log.Fatal("❗ Vui lòng truyền thêm version rollback: go run main.go rollback <version>")
		}
		version := os.Args[2]
		var rev int
		fmt.Sscanf(version, "%d", &rev)
		runRollback(actionConfig, rev)
	default:
		fmt.Println("❗ Câu lệnh không hợp lệ. Dùng: install | upgrade | delete")
	}
}

func loadChart() *chart.Chart {
	chart, err := loader.Load(chartPath)
	if err != nil {
		log.Fatalf("❌ Lỗi load chart: %v", err)
	}
	return chart
}

func runInstall(cfg *action.Configuration) {
	chart := loadChart()
	install := action.NewInstall(cfg)
	install.ReleaseName = releaseName
	install.Namespace = namespace
	install.CreateNamespace = true

	rel, err := install.Run(chart, values)
	if err != nil {
		log.Fatalf("❌ Install thất bại: %v", err)
	}
	fmt.Printf("✅ Đã install thành công: %s\n", rel.Name)
}

func runUpgrade(cfg *action.Configuration) {
	chart := loadChart()
	upgrade := action.NewUpgrade(cfg)
	upgrade.Namespace = namespace

	rel, err := upgrade.Run(releaseName, chart, values)
	if err != nil {
		log.Fatalf("❌ Upgrade thất bại: %v", err)
	}
	fmt.Printf("🔄 Đã upgrade: %s\n", rel.Name)
}

func runDelete(cfg *action.Configuration) {
	uninstall := action.NewUninstall(cfg)
	_, err := uninstall.Run(releaseName)
	if err != nil {
		log.Fatalf("❌ Delete thất bại: %v", err)
	}
	fmt.Println("🧹 Đã xóa release thành công.")
}

func runList(cfg *action.Configuration) {
	list := action.NewList(cfg)
	list.AllNamespaces = true
	releases, err := list.Run()
	if err != nil {
		log.Fatalf("❌ Lỗi khi lấy danh sách release: %v", err)
	}
	fmt.Println("📦 Danh sách release:")
	for _, rel := range releases {
		fmt.Printf("- %s (Namespace: %s, Status: %s, Chart: %s,  Version: %d)\n",
			rel.Name, rel.Namespace, rel.Info.Status, rel.Chart.Name(), rel.Version)
	}
}

func runGetManifest(cfg *action.Configuration) {
	get := action.NewGet(cfg)
	rel, err := get.Run(releaseName)
	if err != nil {
		log.Fatalf("❌ Lỗi khi lấy manifest: %v", err)
	}
	fmt.Println("📜 Manifest:")
	fmt.Println(rel.Manifest)
}

func runHistory(cfg *action.Configuration) {
	history := action.NewHistory(cfg)
	entries, err := history.Run(releaseName)
	if err != nil {
		log.Fatalf("❌ Lỗi khi lấy history: %v", err)
	}
	fmt.Println("📚 Lịch sử release:")
	for _, entry := range entries {
		fmt.Printf("- Version: %d, Status: %s, Updated: %v, Description: %s\n",
			entry.Version, entry.Info.Status, entry.Info.LastDeployed, entry.Info.Description)
	}
}

func runRollback(cfg *action.Configuration, revision int) {
	rollback := action.NewRollback(cfg)
	rollback.Version = revision
	if err := rollback.Run(releaseName); err != nil {
		log.Fatalf("❌ Rollback thất bại: %v", err)
	}
	fmt.Printf("⏪ Đã rollback release %s về version %d\n", releaseName, revision)
}