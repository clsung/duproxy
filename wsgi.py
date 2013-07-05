from duproxy import api

if __name__ == "__main__":
    api.create_app().run('0.0.0.0', debug=True)
