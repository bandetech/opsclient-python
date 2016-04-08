from opsclient import opsclient
import Tkinter
import tkFileDialog

ops_server = '<put your server address>'
client = opsclient.OPSClient(ops_server)

print 'OPS Server', client.server

client.getJobTypes()
jobId = client.createJob(18, 'test', 'test', 'test')
storeUrls = client.getUploadUrls(jobId, 1)

root = Tkinter.Tk()
root.withdraw()
root.update()
in_path = tkFileDialog.askopenfilename(parent=root)

client.postInputFile(in_path, storeUrls[0])
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

baseFileName = in_path
pdfFileName = baseFileName[0:baseFileName.rfind('.')] + '.pdf'
client.downloadFile(downloadUrls[0], pdfFileName)
