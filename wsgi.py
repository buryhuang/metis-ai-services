from metis_ai_services import create_app

if __name__ == "__main__":
    app = create_app("development")
    app.run(host="0.0.0.0")
