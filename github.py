"""
Depends on httplib2 and xml2dict

    easy_install httplib2
    svn checkout http://xml2dict.googlecode.com/svn/trunk/ xml2dict-read-only

Heavily inspired from Will Larson's Python Brightkite wrapper. Thank you

Usage:
from github import Github
g=Github()
commits = g.get_objects(username='github_username', repo='github_repo')
commit  = g.get_commit(username='github_username', repo='github_repo', commit='XXXXXXXXXXXXXXXXXXXXXXXXXXX')
projects = g.search('project_name')
user_info = g.get_user('github_username')
"""


import httplib2
from urllib import quote
from xml2dict import XML2Dict
from xml.parsers.expat import ExpatError

class Github(object):
    def __init__(self):
        self._xml = None
        self._http = None
        
    def _unescape_uri(self, uri):
        return uri.replace("%3A",":").replace("%3F","?").replace("%26","&").replace("%3D","=")
        
    def _get(self, uri):
        uri = self._unescape_uri(uri)
        header, content = self.http.request(uri, "GET")
        return content
        
    def _convert_xml(self, xml):
        return self.xml.fromstring(xml)
        
    def _get_http(self):
        if self._http == None:
            self._http = httplib2.Http()
        return self._http
        
    def _get_xml(self):
        if self._xml == None:
            self._xml = XML2Dict()
        return self._xml
    
    http = property(_get_http,None,None,"Httplib2 connection object.")
    xml = property(_get_xml,None,None,"Object for converting XML to Python.")
    
    def get_objects(self, username, repo):
        "Returns a python dict of all commits in a project."
        uri ="http://github.com/api/v1/xml/%s/%s/commits/master" % (username, repo)
        return self._convert_xml(self._get(quote(uri)))
        
    def get_commit(self, username, repo, commit):
        "Returns a python dict with all the information of a commit"
        uri ="http://github.com/api/v1/xml/%s/%s/commit/%s" % (username, repo, commit)
        return self._convert_xml(self._get(quote(uri)))
        
    def search(self, query):
        "Returns all project for a search query"
        uri ="http://github.com/api/v1/xml/search/%s" % query
        return self._convert_xml(self._get(quote(uri)))
    
    def get_user(self, username):
        "Returns information regarding a user"
        uri ="http://github.com/api/v1/xml/%s" % username
        return self._convert_xml(self._get(quote(uri)))