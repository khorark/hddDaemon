

def my_template(freeSpace):
    temp = """<!DOCTYPE html>
                    <html>
                      <head>
                        <meta charset="utf-8">
                        <title></title>
                      </head>
                      <body>
                        <div>
                            <div>
                                 <h2>hddMonitoring</h2>
                                 <h3 style = 'color: red'>На сервере осталось мало свободно места!</h3>
                                  <div>Приблизительное оставшееся место = <b>{} Гб.</b></div>
                            </div>
                        </div>

                      </body>
                    </html>""".format(freeSpace)
    return temp

