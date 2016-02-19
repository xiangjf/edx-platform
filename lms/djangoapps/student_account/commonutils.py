#syw
import httplib
import xml.etree.ElementTree as ET


loginUrl = 'https://am.fnst.cn.fujitsu.com/amauth?goto=http://mooc.fnst.cn.fujitsu.com/ssologin'
fnstssourl = 'sso.fnst.cn.fujitsu.com'
cookieNameForTokenXMLUrl = '/fnstsso/identity/xml/getCookieNameForToken'
tokenValidXMLUrl = '/fnstsso/identity/xml/isTokenValid?tokenid='
attributesXMLUrl = '/fnstsso/identity/xml/attributes?subjectid='
attrNameDict = {
    'mail': 'mail',
    'sn': 'sn',
    'manager': 'manager',
    'useraccountcontrol': 'useraccountcontrol',
    'department': 'department',
    'givenname': 'givenname',
    'telephonenumber': 'telephonenumber',
    'distinguishedname': 'distinguishedname',
    'employeenumber': 'employeenumber',
    'cn': 'cn',
    'name': 'name',
    'departmentnumber': 'departmentnumber',
    'samaccountname': 'samaccountname',
    'inetuserstatus': 'inetuserstatus',
    'dn': 'dn',
    'userprincipalname': 'userprincipalname',
    'objectclass': 'objectclass',
    'displayname': 'displayname',
}

def getRESTAPIContent(API_URL):
    conn = None
    try:
        conn = httplib.HTTPConnection(fnstssourl)
        conn.request("POST", API_URL)
        res = conn.getresponse()
        data = res.read()
        return data
    except Exception as e:
        print e
        return None
    finally:
        if conn:
            conn.close()



def getTokenInCookie(request):
    cookieNameForToken = getCookieNameForToken()
    try:
        return request.COOKIES[cookieNameForToken]
    except KeyError:
        return None


def getCookieNameForToken():
    cookieNameForTokenXml = getRESTAPIContent(cookieNameForTokenXMLUrl)
    try:
        document = ET.fromstring(cookieNameForTokenXml)
        cookieNameForToken = document.get('string')
    except Exception as e:
        return None
    return cookieNameForToken


def isTokenValid(tokenid):
    tokenValidUrl = tokenValidXMLUrl + tokenid
    validXml = getRESTAPIContent(tokenValidUrl)
    try:
        document = ET.fromstring(validXml)
        booleanvalue = document.get('boolean')
        if booleanvalue == 'true':
            return True
        else:
            return False
    except Exception as e:
        return False


def getAttrByToken(tokenid):
    attributesUrl = attributesXMLUrl + tokenid
    attributesAllXml = getRESTAPIContent(attributesUrl)
    attributes = '</br>'
    try:
        document = ET.fromstring(attributesAllXml)
        for attributeelement in document.findall('attribute'):
            name = attributeelement.get('name')
            values = attributeelement.find('value').text
            attributes += name + ' : ' + values + '</br>'
    except Exception:
        return None
    return attributes


def getAttrByAttrName(tokenid, attrName):
    attributesUrl = attributesXMLUrl + tokenid
    attributesAllXml = getRESTAPIContent(attributesUrl)
    try:
        document = ET.fromstring(attributesAllXml)
        for attributeelement in document.findall('attribute'):
            name = attributeelement.get('name')
            values = attributeelement.find('value').text
            if name == attrName:
                return values
    except Exception as e:
        print e
        return None
    return None


def getmail(tokenid):
    attrname = attrNameDict['mail']
    mail = getAttrByAttrName(tokenid, attrname)
    return mail if mail else ''

def getsn(tokenid):
    attrname = attrNameDict['sn']
    sn = getAttrByAttrName(tokenid, attrname)
    return sn if sn else ''

def getmanager(tokenid):
    attrname = attrNameDict['manager']
    manager = getAttrByAttrName(tokenid, attrname)
    return manager if manager else ''

def getuseraccountcontrol(tokenid):
    attrname = attrNameDict['useraccountcontrol']
    useraccountcontrol = getAttrByAttrName(tokenid, attrname)
    return useraccountcontrol if useraccountcontrol else ''

def getdepartment(tokenid):
    attrname = attrNameDict['department']
    department = getAttrByAttrName(tokenid, attrname)
    return department if department else ''

def getgivenname(tokenid):
    attrname = attrNameDict['givenname']
    givenname = getAttrByAttrName(tokenid, attrname)
    return givenname if givenname else ''

def gettelephonenumber(tokenid):
    attrname = attrNameDict['telephonenumber']
    telephonenumber = getAttrByAttrName(tokenid, attrname)
    return telephonenumber if telephonenumber else ''

def getdistinguishedname(tokenid):
    attrname = attrNameDict['distinguishedname']
    distinguishedname = getAttrByAttrName(tokenid, attrname)
    return distinguishedname if distinguishedname else ''

def getemployeenumber(tokenid):
    attrname = attrNameDict['employeenumber']
    employeenumber = getAttrByAttrName(tokenid, attrname)
    return employeenumber if employeenumber else ''

def getcn(tokenid):
    attrname = attrNameDict['cn']
    cn = getAttrByAttrName(tokenid, attrname)
    return cn if cn else ''

def getname(tokenid):
    attrname = attrNameDict['name']
    name = getAttrByAttrName(tokenid, attrname)
    return name if name else ''

def getdepartmentnumber(tokenid):
    attrname = attrNameDict['departmentnumber']
    departmentnumber = getAttrByAttrName(tokenid, attrname)
    return departmentnumber if departmentnumber else ''

def getsamaccountname(tokenid):
    attrname = attrNameDict['samaccountname']
    samaccountname = getAttrByAttrName(tokenid, attrname)
    return samaccountname if samaccountname else ''

def getinetuserstatus(tokenid):
    attrname = attrNameDict['inetuserstatus']
    inetuserstatus = getAttrByAttrName(tokenid, attrname)
    return inetuserstatus if inetuserstatus else ''

def getdn(tokenid):
    attrname = attrNameDict['dn']
    dn = getAttrByAttrName(tokenid, attrname)
    return dn if dn else ''

def getuserprincipalname(tokenid):
    attrname = attrNameDict['userprincipalname']
    userprincipalname = getAttrByAttrName(tokenid, attrname)
    return userprincipalname if userprincipalname else ''

def getobjectclass(tokenid):
    attrname = attrNameDict['objectclass']
    objectclass = getAttrByAttrName(tokenid, attrname)
    return objectclass if objectclass else ''

def getdisplayname(tokenid):
    attrname = attrNameDict['objectclass']
    displayname = getAttrByAttrName(tokenid, attrname)
    return displayname if displayname else ''
#syw