from FlaskBlog import create_app
#from os import  environ


application = create_app()

if __name__ == '__main__':
    # HOST = environ.get( 'SERVER_HOST','localhost' )
    # try :
    #     PORT = int( environ.get( 'SERVER_PORT','8000' ) )
    # except ValueError :
    #     PORT = 8000
    # print(HOST)
    # application.run( HOST,PORT )
    application.run(debug = True)
