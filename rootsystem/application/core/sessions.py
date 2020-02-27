#-*- coding: utf-8 -*-
from http.cookies import SimpleCookie
from hashlib import new
from logging import basicConfig, WARNING, warning
from os import environ, mkdir, unlink
from os.path import isfile
from shelve import open as shopen
from subprocess import Popen, PIPE
from sys import version_info as v
from time import asctime, localtime, time
from uuid import uuid4

from core.headers import Header
from trbconf import TRB_LOGIN_PAGE, TRB_RESTRICTED_PAGE, TRB_DEFAULT_RESOURCE,\
    TRB_SESS_DIR

TRB_URI = environ['REQUEST_URI'] if 'REQUEST_URI' in environ else '/'
TRB_SERVER_NAME = "{}://{}".format(
    environ['REQUEST_SCHEME'],
    environ['SERVER_NAME']
)


class Sessions(object):

    @staticmethod
    def set(varname, value):
        """
        Sets a new session variable
        """
        sess_file = SessionsHelper.get_filename()
        if not isfile(sess_file):
            raise UserWarning("'set' called before create session")
        sess_file = Sessions.get_all()
        sess_file[varname] = value
        sess_file.close

    @staticmethod
    def get_all():
        """
        Returns all variable sessions
        """
        sid = SessionsHelper.get_sid()
        session = shopen('{}/sess_{}'.format(TRB_SESS_DIR, sid))
        return session

    @staticmethod
    def get(varname):
        """
        Returns a single variable session
        """
        shelf = Sessions.get_all()
        value = shelf[varname] if varname in shelf else ''
        shelf.close()
        return value

    @staticmethod
    def start(tls=False):
        """
        Starts a cookie SID

        Arguments:
        tls -- Set secure argument for HTTPS

        This function destroys the previous SID and
        makes a new cookie file with a new SID
        """
        active_session = Sessions.is_active_session()

        if not active_session:
            sid = SessionsHelper.set_sid()
            Cookies.create(sid, tls=tls)
        else:
            Sessions.update()

    @staticmethod
    def create():
        """
        Creates the session file by using the shelve library
        """
        sid = SessionsHelper.get_sid()
        if sid == 0: SessionsHelper.redirect()
        sess_file = SessionsHelper.get_filename()
        cookie_file = sess_file.replace('sess_', '')
        if not isfile(cookie_file): SessionsHelper.redirect()
        command = ['rm', '-f', cookie_file]
        Popen(command, stdout=PIPE, stderr=PIPE)
        s = shopen(sess_file)
        Sessions.set_session_vars()
        s.close()

    @staticmethod
    def destroy():
       """
       Destroys the session file and the SID cookie
       """
       sid = SessionsHelper.get_sid()
       sess_file = '{}/sess_{}'.format(TRB_SESS_DIR, sid)
       if isfile(sess_file): unlink(sess_file)
       Cookies.destroy()

    @staticmethod
    def is_active_session():
        """
        Verifies if the session file exists.
        Returns False if the session file doesn't exists
        """
        cache_control = "Cache-Control: no-cache,no-store"
        pragma = "Pragma: no-cache"
        headers = SessionHeaders()
        headers.append(cache_control)
        headers.append(pragma)
        headers.send()
        sid = SessionsHelper.get_sid()
        if SessionAnomalyChecker.is_sid_modified(sid):
            SessionsHelper.redirect()
        sess_file = '{}/sess_{}'.format(TRB_SESS_DIR, sid)
        return False if not isfile(sess_file) else True

    @staticmethod
    def check():
        """
        If the session file doesn't exists, this function
        redirects to the login page.

        By the other hand, checks if the session has any anomaly
        """
        if not Sessions.is_active_session():
            SessionsHelper.redirect()

        se2 = SessionAnomalyChecker.has_too_many_cookies()
        se4 = SessionAnomalyChecker.has_sid_substituted()

        if se2 or se4:
            SessionsHelper.redirect()


    @staticmethod
    def check_level(level):
        """
         Veriefies the user access level

        Arguments:
        level -- Integer that represents the level required for the resource

        If the session level if not less or equal than the requerid level, this
        function redirects to the restricted message page.
        The restricted message page is provided by a resource that's defined in
        the TRB_RESTRICTED_PAGE constant.
        """
        session_level = Sessions.get('LEVEL')
        if not session_level <= level:
            SessionsHelper.redirect(TRB_RESTRICTED_PAGE)

    @staticmethod
    def update():
        """
        Updates the access time to the current time on the session and cookie
        files.
        """
        if Sessions.is_active_session():
            sess_file = SessionsHelper.get_filename()
            command = ['touch', sess_file]
            Popen(command, stdout=PIPE, stderr=PIPE)
            sid = SessionsHelper.get_sid()
            Cookies.update(sid)
            Sessions.check_authentication()

    @staticmethod
    def check_authentication():
        """
        Avoids the access to the login page when the user has a valid session
        initialized.
        """
        if TRB_URI == TRB_LOGIN_PAGE:
            SessionsHelper.redirect(TRB_DEFAULT_RESOURCE)

    @staticmethod
    def set_session_vars():
        """
        Automatically sets the following two session variables for a valid
        session:

        REMOTE_ADDR:    The user's IP
        IDENTIFICATOR:  An unique value to avoid the user agent anomaly
        """
        remote_addr = environ.get('REMOTE_ADDR', '')
        identificator = SessionsHelper.get_identificator()
        Sessions.set('REMOTE_ADDR', remote_addr)
        Sessions.set('IDENTIFICATOR', identificator)


class SessionsHelper(object):
    """Helper for Sessions class"""

    @staticmethod
    def clear(sid):
        """
        Deletes of any non-alphanumeric character of the SID
        and verifies if the length of the SID is equal to 32 characters
        """
        lista = [char for char in sid if char.isalnum()]
        sid = ''.join(lista)
        return sid if len(sid) == 32 else '0'

    @staticmethod
    def redirect(page=TRB_LOGIN_PAGE):
        """
        Redirects to the login page

        the resource used to redirect user

        page:  the resource used to redirect user
               the default value is TRB_LOGIN_PAGE
        """
        print("Location: {}{}\n".format(TRB_SERVER_NAME, page))
        exit()

    @staticmethod
    def get_sid():
        """
        Returns the real SID value
        """
        cookie = SimpleCookie()
        cookie_string = environ.get('HTTP_COOKIE', '')
        cookie.load(cookie_string)
        sid = 0 if not SessionAnomalyChecker.is_not_sid else cookie.get('__PYSESSION__SID')
        sid = cookie['__PYSESSION__SID'].value if '__PYSESSION__SID' in cookie else '0'
        return SessionsHelper.clear(sid)

    @staticmethod
    def get_filename():
        """
        Returns the pathname of the session file
        """
        sid = SessionsHelper.get_sid()
        sess_file = '{}/sess_{}'.format(TRB_SESS_DIR, sid)
        return sess_file

    @staticmethod
    def set_sid():
        """
        Sets the session ID
        """
        random_num = SessionsHelper.get_hash('md5', str(uuid4()))
        user_ip = SessionsHelper.get_hash('sha224', environ.get('REMOTE_ADDR'))
        hour = SessionsHelper.get_hash('sha512', asctime(localtime(time())))
        sid = SessionsHelper.get_hash('md5', '{}{}{}'.format(random_num, user_ip, hour))
        return sid

    @staticmethod
    def get_identificator():
        """
        Returns an unique user identification hash
        """
        user_agent = environ.get('HTTP_USER_AGENT', '')
        accept_encoding = environ.get('HTTP_ACCEPT_ENCODING')
        identificator = SessionsHelper.get_hash('md5', '{}{}'.format(user_agent, accept_encoding))
        return identificator

    @staticmethod
    def get_hash(algorithm, string):
        """
        Function that allow use hashlib no matter python version.

        algorithm:  (string) The name of algorithm hash to use
                    for example ('md5')
        string:     (string) String to hash
        """
        if v.major == 2:
            h = new(algorithm, memoryview(string).tobytes())
        else:
            h = new(algorithm, bytes(string, encoding="utf8"))

        return h.hexdigest()


class Cookies(object):
    """Helper for managing cookies: create, destroy and get"""

    @staticmethod
    def create(sid, expires=1800, tls=False):
        """
        Creates a cookie called __PYSESSION_SID

        sid:     (string) the value for the session ID cookie

        expires: (int)    This value represents the Max-Age of the cookie
                          expressed in seconds.
                          Default: 1800

        tls:     (bool)   True for use TLS protocol.
                          Default: False
        """
        tls = 'secure' if tls else ''
        cookie = "Set-Cookie: __PYSESSION__SID={}; Max-Age={};".format(sid, expires)
        cookie += " Path=/; HttpOnly; SameSite=Strict; {}".format(tls)
        headers = SessionHeaders()
        headers.append(cookie)
        headers.send()
        # TODO Refactoring cookies create temp file
        command = ["touch", "{}/{}".format(TRB_SESS_DIR, sid)]
        Popen(command, stdout=PIPE, stderr=PIPE)

    @staticmethod
    def update(name):
        """
        Updates Max-Age of the __PYSESSION__SID cookie
        """
        cookie = "Set-Cookie: __PYSESSION__SID={}; Max-Age=1800;".format(name)
        cookie += " Path=/; HttpOnly; SameSite=Strict;"
        print(cookie)

    @staticmethod
    def destroy():
        """
        Modifies the __PYSESSION_SID cookie by setting the value in 0 and
        expiring it in 1 second
        """
        cookie = "Set-Cookie: __PYSESSION__SID=0; Max-Age=1;"
        cookie += " Path=/; HttpOnly; SameSite=Strict;"
        print(cookie)


    @staticmethod
    def get(name):
        """
        Return the cookie value

        name:   The cookie name that you want to read.
        """
        cookie = SimpleCookie()
        cookie_string = environ.get('HTTP_COOKIE', '')
        cookie.load(cookie_string)
        return cookie[name].value if name in cookie else ''


class SessionHeaders(Header):
    """
    This class allows to manage the HTTP Headers for the Sessions class

    Requires:
        headers.py module
    """

    def send(self):
        """
        Sends HTTP headers to the client
        """
        print('\n'.join(self))
        self[:] = []


class SessionAnomalyChecker:

    @staticmethod
    def is_sid_modified(sid):
        """
        Verifies is the Session ID was modified

        View C. Watson, «Part VI» in AppSensor Guide. OWASP Foundation: USA,
        2015. pp. 136. Online in
        https://www.owasp.org/images/0/02/Owasp-appsensor-guide-v2.pdf
        """
        array = [char for char in sid if char.isalnum()]
        clean_sid = ''.join(array)
        hashed_clean_sid = SessionsHelper.get_hash('sha1', clean_sid)
        hashed_sid = SessionsHelper.get_hash('sha1' , sid)
        if not hashed_sid == hashed_clean_sid:
            return True

    @staticmethod
    def has_too_many_cookies():
        """
        Verifies if there is more than one expected cookie

        Ref. SE2: Part VI: Reference Materials in OWASP AppSensor Guide v2,
        pag. 136 https://www.owasp.org/images/0/02/Owasp-appsensor-guide-v2.pdf
        """
        cookies = environ.get('HTTP_COOKIE', '').count('__PYSESSION__')
        if cookies > 1: return True

    @staticmethod
    def is_not_sid():
        """
        Verifies if is not the expected SID

        Ref. SE3: Part VI: Reference Materials in OWASP AppSensor Guide v2,
        pag. 136 https://www.owasp.org/images/0/02/Owasp-appsensor-guide-v2.pdf
        """
        if not Cookies.get('__PYSESSION__SID'): return True

    @staticmethod
    def has_sid_substituted():
        """
        Verifies if there is any anomaly in a valid SID or cookie

        Ref. SE4: Part VI: Reference Materials in OWASP AppSensor Guide v2,
        pag. 136 https://www.owasp.org/images/0/02/Owasp-appsensor-guide-v2.pdf
        """
        ip_anomaly = SessionAnomalyChecker.has_ip_anomaly()
        user_agent_anomaly = SessionAnomalyChecker.has_user_agent_anomaly()

        if ip_anomaly and user_agent_anomaly:
            return True

    @staticmethod
    def has_ip_anomaly():
        """
        Verifies if there is any anomaly in the IP

        Ref. SE5: Part VI: Reference Materials in OWASP AppSensor Guide v2,
        pag. 137 https://www.owasp.org/images/0/02/Owasp-appsensor-guide-v2.pdf
        """
        if not environ['REMOTE_ADDR'] == Sessions.get('REMOTE_ADDR'):
            return True

    @staticmethod
    def has_user_agent_anomaly():
        """
        Verifies if there is any anomaly in the User Agent mid session

        Ref. SE6: Part VI: Reference Materials in OWASP AppSensor Guide v2,
        pag. 137 https://www.owasp.org/images/0/02/Owasp-appsensor-guide-v2.pdf
        """
        user_identificator = SessionsHelper.get_identificator()
        sess_identificator = Sessions.get('IDENTIFICATOR')
        if not user_identificator == sess_identificator:
            return True

