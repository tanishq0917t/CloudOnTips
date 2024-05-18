import yagmail

class SendMail:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def mail(cls,user,subj,bdy,file=None):
        yag = yagmail.SMTP('EMAIL ID', 'APP PASSWORD')
        recipient = user
        subject = subj
        body = bdy
        if file is not None: 
            attachment = f"pems/{user.split('@')[0]}/{file}"
            yag.send(
                to=recipient,
                subject=subject,
                contents=body,
                attachments=attachment
            )
            return
        else:
            yag.send(
                to=recipient,
                subject=subject,
                contents=body,
            )
        
