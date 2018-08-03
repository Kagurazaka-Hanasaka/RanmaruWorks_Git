import requests, re, json, uuid, glob, sqlite3, time, gc, os, psutil
from bs4 import BeautifulSoup
eoltoken = "null"
merge = []
hlistc = 0
for pgn in range(5):
	cookd = {
		"igneous": "89540adbd",
		"ipb_member_id": "2237746",
		"ipb_pass_hash": "d99e752060d5e11636d7e427f62a3622",
		"lv": "1533216215-1533216236"
	}
	excook = requests.utils.cookiejar_from_dict(cookd, cookiejar=None, overwrite=True)
	exhead = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
		"Connection": "keep-alive",
		"Host": "exhentai.org",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
	}
	eol = []
	hlist = []
	exurl =  "https://exhentai.org/?page="+ str(pgn)+ "&f_doujinshi=on&advsearch=1&f_search=language%3Achinese&f_srdd=5&f_sname=on&f_stags=on&f_sr=on&f_sh=on&f_apply=Apply+Filter"
	orig = requests.get(exurl, headers=exhead, cookies=excook).text
	if "No hits found" in orig:
		print("-----Crawling Queue Ends-----")
		break
	else:
		BSorig = BeautifulSoup(orig)
	table = BSorig.find("table", {"class": "itg"})
	for link in table.findAll("a", href=re.compile("https://exhentai\.org/g/[0-9]{1,8}/[A-Za-z0-9]{10}/")):
		if "href" in link.attrs:
			link2 = link.attrs["href"]
			hlist.append(link2.split("/")[4:6])
	if eoltoken in hlist:
		eol = hlist.index(eoltoken)
		hlist = hlist[eol+1:len(hlist)]
	eoltoken = hlist[-1]
	req = {
		"method": "gdata",
		"gidlist": hlist,
		"namespace": 1
	}
	recl = json.loads(json.dumps(requests.post("https://api.e-hentai.org/api.php", data=json.dumps(req, ensure_ascii=False).encode("utf-8")).json(), ensure_ascii=False))['gmetadata']
	for obj in recl:
		with open(str(uuid.uuid4())+".json", "w", encoding="UTF-8") as f:
			json.dump(obj, f, ensure_ascii=False)
	hlistc = hlistc + 1
	if hlistc >4:
		time.sleep(5)
		hlistc = 0
	print("-----Page "+str(pgn)+" Crawling Ends-----")
	print(psutil.virtual_memory())
	del pgn, exurl, orig, BSorig, table, link, link2, eol, hlist, req, recl, obj, cookd, excook, exhead
	gc.collect()
for f in glob.glob("*.json"):
	with open(f, "rb") as inf:
		merge.append(json.load(inf))
	del f
	gc.collect()
with open("fin.json", "w", encoding="UTF-8") as out:
	json.dump(merge, out, ensure_ascii=False, sort_keys=True)
