import ConfigParser, mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib

class Pitcher(object):
  CONF_SMTP_SECTION = "SMTP"
  CONF_SMTP_HOST = "host"
  CONF_SMTP_PORT = "port"
  CONF_MAIL_FROM = "from"
  CONF_MAIL_TO = "to"
  CONF_MAIL_SUBJECT = "subject"
  CONF_MAIL_HTML_CONTENT = "htmlContent"
  CONF_MAIL_PLAIN_CONTENT = "plainContent"
  CONF_MAIL_FILES = "files"

  smtpInfo = None
  config = None

  @staticmethod
  def hasOptions(config, section, *options):
    for option in options:
      if not config.has_option(section, option):
        return False
    return True

  def __init__(self, configPath):
    self.config = ConfigParser.ConfigParser()
    self.config.read(configPath)

    # if self.config.has_option(self.CONF_SMTP_SECTION, self.CONF_SMTP_HOST) \
    # and self.config.has_option(self.CONF_SMTP_SECTION, self.CONF_SMTP_PORT):
    if Pitcher.hasOptions(self.config, self.CONF_SMTP_SECTION, \
    self.CONF_SMTP_HOST, self.CONF_SMTP_PORT):
      self.smtpInfo = dict(self.config.items(self.CONF_SMTP_SECTION))
    else:
      raise KeyError("There should be SMTP connection Information in config file.")

  def pitch(self, sectionName):
    def getExt(fileName):
      return "." + fileName.split(".")[-1]
    def getMIMEType(fileName):
      return mimetypes.read_mime_types(fileName)[getExt(fileName)].split("/")

    if not Pitcher.hasOptions(self.config, sectionName, \
    self.CONF_MAIL_FROM, self.CONF_MAIL_TO):
      raise KeyError("Cannot find from/to inforation in section(%s)." % sectionName)
    if not Pitcher.hasOptions(self.config, sectionName, self.CONF_MAIL_SUBJECT):
      raise KeyError("Cannot find subject in section(%s)." % sectionName)

    mailInfo = MIMEMultipart()
    mailInfo["From"] = self.config.get(sectionName, self.CONF_MAIL_FROM)
    mailInfo["To"] = self.config.get(sectionName, self.CONF_MAIL_TO)
    mailInfo["Subject"] = self.config.get(sectionName, self.CONF_MAIL_SUBJECT)
    if self.config.has_option(sectionName, self.CONF_MAIL_HTML_CONTENT):
      content = self.config.get(sectionName, self.CONF_MAIL_HTML_CONTENT)
      mailInfo.attach(MIMEText(content, "html", "utf-8"))
    elif self.config.has_option(sectionName, self.CONF_MAIL_PLAIN_CONTENT):
      content = self.config.get(sectionName, self.CONF_MAIL_PLAIN_CONTENT)
      mailInfo.attach(MIMEText(content, "plain", "utf-8"))

    files = filter(lambda option: self.CONF_MAIL_FILES in option, \
      self.config.options(sectionName))
    for file in files:
      filePath = self.config.get(sectionName, file)
      MIMEType, encoding = mimetypes.guess_type(filePath)
      if MIMEType is not None:
        primarytype, subtype = MIMEType.split("/")
      else:
        primarytype, subtype = ("text", "plain")

      if primarytype == "text":
        with open(filePath, "r") as filePointer:
          mime = MIMEText(filePointer.read(), _subtype=subtype)
      elif primarytype == "image":
        with open(filePath, "rb") as filePointer:
          mime = MIMEImage(filePointer.read(), _subtype=subtype)
      elif primarytype == "audio":
        with open(filePath, "rb") as filePointer:
          mime = MIMEImage(filePointer.read(), _subtype=subtype)
      else:
        with open(filePath, "rb") as filePointer:
          mime = MIMEBase(*getMIMEType(filePath))
          mime.set_payload(filePointer.read())
          encoders.encode_base64(attach)
      mime.add_header("Content-Disposition", "attachment", filename=filePath)
      mailInfo.attach(mime)

    smtp = smtplib.SMTP(self.smtpInfo[self.CONF_SMTP_HOST], \
      self.smtpInfo[self.CONF_SMTP_PORT])
    smtp.sendmail(self.mailInfo["From"], self.mailInfo["To"], mailInfo.as_string())
