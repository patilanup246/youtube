import requests

import requests
from time import sleep
import random

# Add these values
API_KEY = '106df55668245f161905ecc3f529de5a'  # Your 2captcha API KEY
site_key = '6Lf39AMTAAAAALPbLZdcrWDa8Ygmgk_fmGmrlRog'  # site-key, read the 2captcha docs on how to get this
url = 'https://www.youtube.com/channels_profile_ajax?action_verify_business_email_recaptcha=1'  # example url
proxy_list = ['23.98.156.225:3128','45.55.9.218:8080','138.68.24.145:8080','167.71.161.102:8080'
    ,'159.203.91.6:3128','198.199.120.102:3128','167.71.242.25:3128']  # example proxy

proxy = str(random.choice(proxy_list))

proxy = {'http': 'http://' + proxy, 'https': 'https://' +proxy}
print(proxy)

s = requests.Session()

abc = requests.post('https://2captcha.com/in.php?key=106df55668245f161905ecc3f529de5a&method=userrecaptcha&googlekey=6Lf39AMTAAAAALPbLZdcrWDa8Ygmgk_fmGmrlRog&pageurl=https://www.youtube.com/channels_profile_ajax?action_verify_business_email_recaptcha')
captcha_id = abc.text.split('|')[1]
print(abc.text)

# here we post site key to 2captcha to get captcha ID (and we parse it here too)
# captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, site_key, url), proxies=proxy).text.split('|')[1]
# then we parse gresponse from 2captcha response
proxy = {'http': 'http://' + str(random.choice(proxy_list)), 'https': 'https://' + str(random.choice(proxy_list))}
recaptcha_answer = requests.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
print("solving ref captcha...")
while 'CAPCHA_NOT_READY' in recaptcha_answer:
    sleep(5)
    proxy = str(random.choice(proxy_list))

    proxy = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
    recaptcha_answer = requests.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
recaptcha_answer = recaptcha_answer.split('|')[1]

# we make the payload for the post data here, use something like mitmproxy or fiddler to see what is needed


# headers = {"accept":"*/*",
# "accept-encoding":"gzip, deflate, br",
# "accept-language":"en-GB,en-US;q=0.9,en;q=0.8,ja;q=0.7",
# "content-length":"758",
# "content-type":"application/x-www-form-urlencoded",
# "cookie":"VISITOR_INFO1_LIVE=VvYXoYATp5o; HSID=AkySd1o8U5LByCAjy; SSID=AwHwsvuq2ZkZAG7cL; APISID=7MxZ2byP1qNAEHTu/AwZRSZO4VH4xRdIZZ; SAPISID=bestwtDjPQWeSnxc/ABJw675wkzybesXa6; PREF=f1=50000000&fms1=10000&fms2=10000&al=en-GB&f5=30; SID=nAfTeA-6pCvYJEcHaam-JTrB0ov893z2cV2tMdArOWAsFQ5wee8hkOrCg9YEHGjFhXECAA.; YSC=kacKE5esaao; LOGIN_INFO=AFmmF2swRQIhAL2m3L2tNH2Kbzooo9FlNZqJHQlqas958X_8FmBhhzMYAiAJ-mCU8oLL8eMCYe97N5RZBECe_8CVhoE-Sd6d58YNrg:QUQ3MjNmeGd5b2tTUmNOaU5iZ3BXTzRHOVQzSTJVYnNvTV9VczVVSzZkeTE2UjQ1UFcxZXdOR3ZleEdkbkZvcGczVDNsSWdpZGdVNEtnNERHRGFxLVdQZ2l6amZfOEg3U3NUSkdlZVZSOXdoUHBaVmVxdEVIM09aOXo3aF8xT1hGMWVsdExSMUpNbmxrbzJrRjdLY01NN3V6NkxoOEI4dWNWRmhJemxfRE9LbmRMZ1FnMloySENN; SIDCC=AN0-TYvl5_vbfdzBabBI6AJN8Ia8eKGz4rEe4jYqhFiTPJ9eMVLR33zoduKg8e0yDnoP7ub9Pw",
# "origin":"https://www.youtube.com",
# "referer":"https://www.youtube.com/channel/UCvO6uJUVJQ6SrATfsWR5_aA/about",
# "sec-fetch-mode":"cors",
# "sec-fetch-site":"same-origin",
# "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
# "x-client-data":"CKS1yQEIjrbJAQiktskBCKmdygEIqKPKAQjiqMoBCK+sygEIl63KAQjNrcoBCPKtygEIy67KAQjKr8oB",
# "x-spf-previous":"https://www.youtube.com/channel/UCvO6uJUVJQ6SrATfsWR5_aA/about",
# "x-spf-referer":"https://www.youtube.com/channel/UCvO6uJUVJQ6SrATfsWR5_aA/about",
# "x-youtube-ad-signals":"dt=1567426171646&flash=0&frm&u_tz=330&u_his=2&u_java&u_h=768&u_w=1366&u_ah=720&u_aw=1366&u_cd=24&u_nplug=3&u_nmime=4&bc=31&bih=204&biw=1351&brdim=0%2C24%2C0%2C24%2C1366%2C24%2C1366%2C720%2C1366%2C204&vis=1&wgl=true&ca_type=image&bid=ANyPxKqCZPqNrEhSoECclzAOnRZSFAlXnIzXpEK_wLN1xOCR2McwkdrKbmoZD1e__V1HuliObt6QDcBICk54QEmDXH2gzmH94A",
# "x-youtube-client-name":"1",
# "x-youtube-client-version":"2.20190830.05.01",
# "x-youtube-identity-token":"QUFFLUhqbHFtbzFqck8zN3Z3c3NWV0VZMU01UWRCcktLd3w=",
# "x-youtube-page-cl":"266331450",
# "x-youtube-page-label":"youtube.ytfe.desktop_20190829_5_RC1",
# "x-youtube-utc-offset":"330",
# "x-youtube-variants-checksum":"7919c3ddb007fb03b180a41779472737"}

# youtube = requests.get('https://www.youtube.com/channel/UCvO6uJUVJQ6SrATfsWR5_aA/about')
#
# textyooutube = youtube.text
#
# session_token = textyooutube.split("'XSRF_TOKEN': ")[1]
# session_token = session_token.split('",')[0]
# session_token = session_token.replace('"','')

# VARIANTS_CHECKSUM = textyooutube.split('VARIANTS_CHECKSUM":"')[1]
# VARIANTS_CHECKSUM = VARIANTS_CHECKSUM.split('"')[0]

# PAGE_CL = textyooutube.split('PAGE_CL":"')[1]
# PAGE_CL = PAGE_CL.split('"')[0]



proxy = str(random.choice(proxy_list))

# headers = {'x-youtube-identity-token':token,'x-youtube-page-cl':PAGE_CL,'x-youtube-variants-checksum':VARIANTS_CHECKSUM,
#            }


payload = {
    'channel_id': 'UCvO6uJUVJQ6SrATfsWR5_aA',
    'gresponse': recaptcha_answer,  # This is the response from 2captcha, which is needed for the post request to go through.
    'session_token':"QUFFLUhqbXBtVmpDUFo5WWpFek5Qa2tyTFhfakFicDc3UXxBQ3Jtc0trQU9ya2F1WjNlS3M4OURNc0VCLThGWFdPQkFiSzJfSDVrblZOUFlBcWdINVAzbXpWb2FZRDFwR2t2R1pBS2dRYm9nQWpVZXl1aDIyM1pxd05yS3J2bVBJUlJ5MUpTX3RZRDFFSHhXTVlIdThZMUtWQkdDNEJJWXljVEJtQ1pZaFVlNXlRRmxnQ1owTXEtM0hsU1Z1NXVHWmxwdFE="
    }

proxy = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
# then send the post request to the url
response = requests.post(url, payload)

try:
    print(response.text)
except:
    strhtml = str(response.content).encode('utf-8')
    print(strhtml)


# And that's all there is to it other than scraping data from the website, which is dynamic for every website.