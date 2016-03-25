# Create Searchable PDF

from poster.streaminghttp import register_openers
from twisted.internet import reactor, protocol
import urllib
import urllib2
import json
import base64
import time
import os.path


class OPSClient(object):
    OMNISERVER_SERVICE = '/Nuance.OmniPage.Server.Service'
    def __init__(self, server):
        register_openers()
        self.server = server
        self.JOB_URL_BASE       = "http://"+self.server+self.OMNISERVER_SERVICE+'/api/job/'
        self.STORE_URL = "http://" + self.server + self.OMNISERVER_SERVICE + '/api/storage/'
        self.CREATE_JOB_URL     = self.JOB_URL_BASE + "CreateJob"
        self.GET_UPLOAD_URLS    = self.JOB_URL_BASE + 'GetUploadUrls'
        self.START_JOB_URL      = self.JOB_URL_BASE + 'StartJob'
        self.GET_JOBINFO_URL    = self.JOB_URL_BASE + 'GetJobInfo'
        self.GET_DOWNLOAD_URL   = self.JOB_URL_BASE + 'GetDownloadUrls'
        self.PROCESS_ONCALL_URL = self.JOB_URL_BASE + 'ProcessOnCall'
        self.CONF_NOTIFICATION_URL = self.JOB_URL_BASE + "ConfigureJobNotification"
        self.GET_JOBDATA_DESCRIPTION_URL = self.JOB_URL_BASE + "GetJobDataDescription"
        self.GET_JOB_NOTIFICATION_INFO_URL = self.JOB_URL_BASE + "GetNotificationInfo"
        self.CANCEL_JOB_URL = self.JOB_URL_BASE + "CancelJob"
        self.DELETE_JOB_DATA_URL = self.JOB_URL_BASE + "DeleteJobData"
        self.GET_JOB_TYPES_URL = self.JOB_URL_BASE + "GetJobTypes"

    def __server_request(self, url, requestParams):
        if(requestParams is not None):
            data = urllib.urlencode(requestParams)
            response = urllib2.urlopen(url+'?'+data)
        else :
            response = urllib2.urlopen(url)
        ret = response.read()
        return json.loads(ret)

    def __server_request_post(self, url, requestParams):
        request = urllib2.Request(url, headers={'Content-Type': 'application/json'})
        response = urllib2.urlopen(request, json.dumps(requestParams))

    def __replace_extension(self, filename, extension):
        fileRoot, ext = os.path.splitext(filename)
        return filename.replace(ext, extension)

    # CreateJob
    def createJob(self, jobTypeId, title, description, metadata):
        request_values = {'jobTypeId': jobTypeId, 'title':title, 'description':description, 'metadata': metadata}
        jobId = self.__server_request(self.CREATE_JOB_URL, request_values)
        return jobId

    # GetUploadUrls
    def getUploadUrls(self, jobId, count):
        request_values = {'jobId' : jobId, 'count': count}
        storeUrls = self.__server_request(self.GET_UPLOAD_URLS, request_values)
        #print 'storeUrls :', storeUrls
        return storeUrls

    # Post Original File
    def postInputFile(self, fileName, url):
        from poster.encode import multipart_encode
        datagen, headers = multipart_encode({"image1" : open(fileName, "rb")})
        request = urllib2.Request(url, datagen, headers)
        response = urllib2.urlopen(request)
        responseUrls = json.loads(response.read())

    # Configure Job Notification
    def configureJobNotification(self, jobId, requestValues):
        response = self.__server_request_post(self.CONF_NOTIFICATION_URL+'?jobId='+jobId, requestValues)

    # Start Job
    def startJob(self, jobId, conversionParams):
        request_values = {'jobId':jobId, 'timeToLiveSec': 3600, 'priority': 2, 'conversionParameters': conversionParams}
        self.__server_request(self.START_JOB_URL, request_values)

    # Run Notification Server
    def startLocalNotificationServer(self, port, sleepTime):
        factory = protocol.ServerFactory()
        factory.protocol = NotificationService
        reactor.listenTCP(port, factory)
        reactor.run()
        time.sleep(sleepTime)

    # Get Download URLs
    def getDownloadUrls(self, jobId):
        requestParams = {'jobId': jobId}
        downloadUrls = self.__server_request(self.GET_DOWNLOAD_URL, requestParams)
        return downloadUrls

    # Store Result (PDF)
    def downloadFile(self, url, fileName):
        #output_filename = replace_extension(OUTPUT_DIR + os.path.basename(ORIGINAL_FILE), '.pdf')
        resultFile = urllib.urlopen(url)
        localFile = open(fileName, 'wb')
        localFile.write(resultFile.read())
        resultFile.close()
        localFile.close()

    # Get Job Data Description
    def getJobDataDescription(self, jobId):
        request_values = {'jobId':jobId}
        response =  self.__server_request(self.GET_JOBDATA_DESCRIPTION_URL, request_values)
        print 'GetJobDataDescription Return :', response

    # Get Notification Info
    def getNotificationInfo(self, jobId):
        request_values = {'jobId':jobId}
        response =  self.__server_request(self.GET_JOB_NOTIFICATION_INFO_URL, request_values)
        print 'GetJobNotificationInfo Return :', response

    # Cancel Job
    def cabcelJob(self, jobId):
        request_values = {'jobId':jobId}
        response =  self.__server_request(self.CANCEL_JOB_URL, request_values)

    # Delete Job Data
    def deleteJobData(self, jobId, dataTypeFlag):
        request_values = {'jobId':jobId, 'dataTypeFlag':dataTypeFlag}
        response =  self.__server_request(self.DELETE_JOB_DATA_URL, request_values)

    # Get Job Types
    def getJobTypes(self):
        response =  self.__server_request(self.GET_JOB_TYPES_URL, None)
        #print 'GetJobTypes return :', response
        return response


class NotificationService(protocol.Protocol):
    def connectionMade(self):
        print 'Start Notification Server. Waiting notification from OCS....'
    def connectionLost(self, reason):
        print 'Connection lost with OCS.'
    def dataReceived(self, data):
        print data
        reactor.stop()


if __name__ == '__main__':
    print 'Do not call this module directly. Please use this as a library like:'
    print 'from opsclient import OPSClient'
    print 'client = OPSClient(\'youropsserver\')'
