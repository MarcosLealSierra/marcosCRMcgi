class Header(list):

    ST = "Status: "
    CT = "Content-Type: "

    HTML = "{}text/html; charset=utf-8".format(CT)
    JSON = "{}application/json".format(CT)

    NOTFOUND = "{}404 Not Found".format(ST)
    BAD_REQUEST = "{}400 Bad Request".format(ST)

    def send(self):
        print('\n'.join(self), '\n')
        self[:] = []

header = Header()
