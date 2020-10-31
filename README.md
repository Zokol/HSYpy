# HSYpy
**Crawler for HSY web interface**

## Introduction

Helsingin Seudun Ympäristöpalvelut (HSY) offers reliable waste collection.
Unfortunately they don't have a good API or app to figure out when they will collect the trash.

As I found myself looking for this information more than once, opening the site, going to email for the login info and then finding the date for the next trash collection.

I wanted to make this process a bit easier.

## Installation

```
pip3 install -r requirements.txt
```

**Set your credentials to cred.json**
```
palvelutunnus can be found in the HSY contract or your latest bill, under label "Jätepalvelutunnus"
```

```
mv cred.json.template cred.json
vim cred.json
```

## Usage

```
$ python3 hsyapi.py 
['Muovi - maanantai / Seuraava tyhjennys: 14.9.2020', 'Sekajäte - torstai / Seuraava tyhjennys: 17.9.2020', '']
```

## Description

HSY is running ASP.NET aplication at ytvlogistiikka.net

Login requires a POST-request, with service ID and zipcode.
As a response, you get page with list of services you have ordered, as well as prices for them.

Trash collecting dates are listed in pop-up window, which includes a table of dates.

**Example login (cookie and request data is sanitized):**
```
POST /Logica.Ytv.Logistics.Subscription.WebUpdate/fi/Palvelutilaus.aspx/DoLogin/2 HTTP/1.1
Host: www.ytvlogistiikka.net
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.ytvlogistiikka.net/Logica.Ytv.Logistics.Subscription.WebUpdate/
Content-Type: application/x-www-form-urlencoded
X-Requested-With: XMLHttpRequest
Content-Length: 61
Connection: close
Cookie: ASP.NET_SessionId=1v0aqlqweeweqq01gkyggcqz

HakuehtoPalvelutunnus=BB44-010030-1&HakuehtoPostinumero=01000
```

**Snippet of the response:**
```
<td colspan="9">
	<a: id="Tyhjennyspaivat" class="ClueTip" tabindex="-1" href="" title="
		Info - Sijaintipaikka 1 | 
			<table>
				<tr>
					<td>
						Muovi - maanantai / Seuraava tyhjennys: 14.9.2020
					</td>
				</tr>
				<tr>
				<td>
				</td>
				</tr>
				<tr>
					<td>
						Sekajäte - torstai / Seuraava tyhjennys: 17.9.2020
					</td>
				</tr>
				<tr>
				<td>
				</td>
				</tr>
			</table>"
		>
		<label for="Tyhjennyspaivat" class = "modifiedNoWidthBlue">
		Näytä seuraavat tyhjennyspäivät
		</label>     
	</a>
</td>
<td>
</td>
```
