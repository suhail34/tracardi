<h1>File sending_mail_via_gmail.py file documentation</h1>
<h2>Init</h2>
<h3><p>init={</p>
                <p>'smtp': "smtp.gmail.com", - Choose a smtp server</p>
                <p>'port': 587, - Select the port on which stmp will run</p>
                <p>'username': None, - enter your username</p>
                <p>'password': None, - enter your password</p>
                <p>"to": None, - Choose email recipient</p>
                <p>"from": None, - Choose your email</p>
                <p>"replyTo": None,- Select to whom the reply should be sent </p>
                <p>"title": Select a Title Message,</p>
                <p>"message": Enter your message, HTML is allowed </p>
                    }</h3>

<h2>Most frequent errors</h2>
<div><h4><p>[WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time,
or established connection failed because connected host has failed to respond</p></h4></div>
<h3>Solution - Check the STMP server and port are correct</h3>

<h4>(535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8 https://support.google.com/mail/?p=BadCredentials s7sm108045lfg.297 - gsmtp')</h4>
<h3>Solution - Check the username and password,also look at this https://www.google.com/settings/security/lesssecureapps </h3>
<h4>Validation error for Configuration password field required (type=value_error.missing). This error occurred when initializing node f20bd9f2-a386-48a6-85ce-aa0eea538819.</h4>
<h3>Check the init, for example here smtp is not specified. The data needed are smtp, port, username,password,to,from</h3>
