from qxf2_scheduler import app
#import qxf2_scheduler.seeder as seeders
if __name__ == '__main__':
    #seeders.run()
    app.run(debug=True,port=6464)