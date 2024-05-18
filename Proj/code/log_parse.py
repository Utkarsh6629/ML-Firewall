from xml.etree import ElementTree as ET
import urllib
import base64
import csv

log_path = 'good_req1.log'
output_csv_log = 'good1.csv'
class_flag = "good"

class LogParse:
    def parse_log(self, log_path):
        result = {}
        try:
            with open(log_path): pass
        except IOError:
            print "[+] Error!!! ", log_path, "doesn't exist.."
            exit()
        try:
            tree = ET.parse(log_path)
        except Exception as e:
            print '[+] Oops..! Please make sure binary data is not present in Log, Like raw image dump, flash(.swf files) dump etc'
            exit()
        root = tree.getroot()
        for reqs in root.findall('item'):
            raw_req = base64.b64decode(reqs.find('request').text)
            raw_resp = base64.b64decode(reqs.find('response').text)
            result[raw_req] = raw_resp
        return result

    def parseRawHTTPReq(self, rawreq):
        headers = {}
        sp = rawreq.split('\r\n\r\n', 1)
        if len(sp) > 1:
            head, body = sp
        else:
            head = sp[0]
            body = ""
        c1 = head.split('\n')
        method, path, _ = c1[0].split(' ', 2)
        for i in range(1, len(c1)):
            parts = c1[i].split(': ', 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]
        return headers, method, body, path

def ExtractFeatures(method, path_enc, body_enc, headers):
    badwords = ['sleep', 'drop', 'uid', 'select', 'waitfor', 'delay', 'system', 'union', 'order by', 'group by']
    badwords_count = 0
    path = urllib.unquote_plus(path_enc)
    body = urllib.unquote_plus(body_enc)
    single_q = path.count("'") + body.count("'")
    double_q = path.count('"') + body.count('"')
    dashes = path.count("--") + body.count("--")
    braces = path.count("(") + body.count("(")
    spaces = path.count(" ") + body.count(" ")
    for word in badwords:
        badwords_count += path.count(word) + body.count(word)
    for header in headers.values():
        for word in badwords:
            badwords_count += header.count(word)
    return [method, path_enc.encode('utf-8').strip(), body_enc.encode('utf-8').strip(), single_q, double_q, dashes, braces, spaces, badwords_count, class_flag]

f = open(output_csv_log, "wb")
c = csv.writer(f)
c.writerow(["method", "path", "body", "single_q", "double_q", "dashes", "braces", "spaces", "badwords", "class"])
f.close()

lp = LogParse()
result = lp.parse_log(log_path)

with open(output_csv_log, "ab") as f:
    c = csv.writer(f)
    for items in result.items():
        raaw = items[0]  # base64 decoding is already done in parse_log
        headers, method, body, path = lp.parseRawHTTPReq(raaw)
        features = ExtractFeatures(method, path, body, headers)
        c.writerow(features)
