from application import create_app

application = app = create_app()

# for development only
# if __name__ == '__main__':
#     app.run(host="192.168.1.100", port=5000, debug=True)
