from opsclient import opsclient

ops_server = '<put your server address>'
client = opsclient.OPSClient(ops_server)

print client.server

client.getJobTypes()
jobId = client.createJob(18, 'test', 'test', 'test')
storeUrls = client.getUploadUrls(jobId, 1)
client.postInputFile('sample.png', storeUrls[0])
request_values = ( {
                'CompletionNotifications' : [{
                        'AuthenticationHeader': None,
                        'CertificateSubject' : None,
                        'Parameters': None,
                        'ServiceUrl' : 'http://<put your client address>:8000/Success'
                }],
                'FailureNotifications' : [{
                        'AuthenticationHeader': None,
                        'CertificateSubject' : None,
                        'Parameters': None,
                        'ServiceUrl' : 'http://<put your client address>:8000/Failed'
                }]
                }
            )
client.configureJobNotification(jobId, request_values)
conversionParams = ('<ConversionParameters xmlns="http://www.nuance.com/2011/ConversionParameters">'
'<ImageQuality>Better</ImageQuality>'
'<LogicalFormRecognition>No</LogicalFormRecognition>'
'<Language>LANG_JPN</Language>'
'<Rotation>Auto</Rotation>'
'<Deskew>No</Deskew>'
'<TradeOff>Balanced</TradeOff>'
'<LayoutTradeOff>Accuracy</LayoutTradeOff>'
'<PDFCompatibility>PDF1.6</PDFCompatibility>'
'<CacheInputForReuse>True</CacheInputForReuse>'
'</ConversionParameters>')
client.startJob(jobId, conversionParams)
client.startLocalNotificationServer(8000, 3)
downloadUrls = client.getDownloadUrls(jobId)
client.downloadFile(downloadUrls[0], 'test0000.pdf')
