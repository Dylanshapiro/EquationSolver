from app import app

from waitress import serve

'''
Starts service
'''
SERVER = False
if __name__ == '__main__':
    if SERVER:
        #serve(app, host='0.0.0.0', port=8080)
        print("Make sure that everything is secure before launching this onto the web!")
    else:
        app.run()
