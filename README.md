# MailPitcher
A library simplify file mailing tasks

# Setup
Define your own `pitcher.cfg`, need not to be in a specific directory or name. You can address it with the Pitcher constructor.    
The `pitcher.cfg` will look like the following:
```
[Shot_1]
enabled = True
from = dummy@sunshire.net
to = ire7715@sunshire.net, ire771501@sunshire.net
subject = MailPitcher Test
htmlContent = <h1>MailPitcher</h1><p>test message</p>
plainContent = test message
files[0] = /tmp/mail.log
files[1] = /tmp/mail.pitcher.log
files[2] = /tmp/gloves.pitcher.log

[SMTP]
host = smtp.sunshire.net
port = 25
```

The section "SMTP" is necessary, which addresses the SMTP server and port.    
For other sections, each one documents a pitching(mailing) task.    
You are allow to specify the sender(`from`)/receiver(`to`), aware that `to` field is allow multi-value, so you can mail multiple people.    
    
`enabled` field is optional, default True. Assigning values other than "True" would skip this section.    
`subject` field is plain text.    
`htmlContent` and `plainContent` are mutual exculsive, but if you specified both, htmlContent has a higher priority.    
And the last but not least, `files*`, you are allow to specify variadic quatity of files, as long as they got the correct prefix(`files`).

# Write your own script
An example code is available [here](https://github.com/ire7715/MailPitcher/blob/master/example.py). You may copy it and modify it to your version.    
Or if you are confident enough, you may `from MailPitcher import Pitcher` and apply it in your code.

# The main concept of usage
A code snippet is worth a thousand words.
```
from MailPitcher import Pitcher
pitcher = Pitcher(configFile) # specify the config file of this pitch.
pitcher.pitch(sectionName) # address the task you want to pitch by its section name.
# you may also pass arguments to determine which task to run, imagination is the boundary.
```
