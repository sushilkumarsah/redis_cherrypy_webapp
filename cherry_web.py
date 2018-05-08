import os
import random
import string
import redis
import cherrypy

head_section = """
        <html>
          <head>
            <link href="/static/css/style.css" rel="stylesheet">
          </head>
          <body>
               """

end_section = """
          </body>
        </html>"""
        
table_head_section = """
<center>
<table>
    <thead>
        <tr>
        <th>Name</th>
        <th>Code</th>
        <th>Open</th>
        <th>Low</th>
        <th>High</th>
        <th>Close</th>
        <th>Variation %</th>
        </tr>
    </thead>
    <tbody>
"""

table_end_section = """
    </tbody>
</table>
</center>
"""        


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        
        form = """
            <br /> <br />
            <center>
            <form method="get" action="out">
              Enter the name of the scrip
              <input type="text" value="" name="scrip_name" />
              <button type="submit">Give details</button>
            </form>
            <form method="get" action="out1">
              <button type="submit">Give details of top 10 scrip</button>
            </form>
            <form method="get" action="load">
              <button type="submit">Load latest data in DB</button>
            </form>
            
            </center>
        """
    
        return head_section + form + end_section
    
    @cherrypy.expose
    def out(self, scrip_name):
        scrip_name = scrip_name.upper()
        redis_conn = redis.Redis()
        a = redis_conn.hgetall("scrip:'"+scrip_name+"'")
        
        b = {}
        
        form = """
            <form method="get" action="out">
              Enter the name of the scrip
              <input type="text" value="" name="scrip_name" />
              <button type="submit">Give details</button>
            </form>
            
            <form method="post" action="index">
                <button type="submit">Homepage</button>
            </form>
            """

        if a == b:
            return "<center> <h2> There is no such scrip in DB. Please try again  </h2> " + form + '</center>'
            
            
        else:    
            table_string = head_section + '<center> <h2> Details of the scrip </h2> </center>' + '<br />' + table_head_section 
            
            table_string = table_string + '<tr>' + '<th>'+ scrip_name + '</th>' + '<td>'+ a['code'] +'</td>' + '<td>'+a['open'] +'</td>' + '<td>'+a['low'] +'</td>'+ '<td>'+a['high'] +'</td>'+ '<td>'+a['close'] +'</td>' + '<td>'+a['variation'] +'</td>' + '</tr>'
            
            return table_string + table_end_section + end_section + '<br /> <center>'+ form + '</center>'

            

    @cherrypy.expose
    def out1(self):
    
        form = """
            <center>
            <br />
            <form method="post" action="index">
                <button type="submit">Homepage</button>
            </form> 
            </center>
            """
            
        redis_conn = redis.Redis()
        a = redis_conn.keys("scrip:*")

        if a.__len__() == 0:
            return "<center> <b> There are no items in DB. Load data from homepage </b> </center>" + form
         
        
        l = []

        for i in a:
            b = float(redis_conn.hget(i, 'variation'))
            l.append([b,i])

           
        l.sort(reverse=True)
       
        t = l[0:10]

        table_string =  head_section + '<center> <h2> Top 10 scrips in terms of variation in percentage as compared to previous day closing price </h2> </center> ' + '<br />' + table_head_section 
        
        for i in t:

            x = redis_conn.hgetall(i[1])
            
            table_string = table_string + '<tr>' + '<th>'+ i[1][7:-1] + '</th>' + '<td>' + x['code'] + '</td>' + '<td>' + x['open'] +'</td>' + '<td>' + x['low'] +'</td>'+ '<td>' + x['high'] +'</td>'+ '<td>' + x['close'] +'</td>'   + '<td>' + x['variation'] +'</td>'  + '</tr>'
       
        
        return table_string + table_end_section + end_section + form
        
        
    @cherrypy.expose
    def load(self):
        import download_zip
        import parse_csv
        
        folder_location = "/home/ubuntu/web_app/"

        zip_name = download_zip.download(folder_location)

        parse_csv.parse(zip_name, folder_location)
        
        raise cherrypy.HTTPRedirect("/index")
 
def display(folder_location):
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': folder_location
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.config.update( {'server.socket_host': '0.0.0.0'} ) 
    cherrypy.quickstart(StringGenerator(), '/', conf)

        
if __name__ == '__main__':
    display("/home/ubuntu/web_app")