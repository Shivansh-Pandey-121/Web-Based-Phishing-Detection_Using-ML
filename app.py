# import os
# import base64
# import re
# import urllib.parse
# import socket
# import ssl
# import requests
# from flask import Flask, request, jsonify, render_template
# from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
# from google import genai
# from dotenv import load_dotenv

# # 1. Load the environment parameters first
# load_dotenv()

# # 2. Extract and verify the API key availability
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     print("🚨 SEVERE CRITICAL: 'GEMINI_API_KEY' was not found by Flask app.py!")
#     print("Ensure your .env file is in the root directory alongside app.py.")
# else:
#     print(f"🔒 App initialized using API Key: {api_key[:8]}...[Redacted]")

# # 3. Instantiate engine structures
# client = genai.Client(api_key=api_key)
# app = Flask(__name__)

# # Local BERT model configuration
# model_path = "./my_phishing_model"
# model      = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=2)
# tokenizer  = AutoTokenizer.from_pretrained(model_path)
# phishing_detector = pipeline("text-classification", model=model, tokenizer=tokenizer)

# UNICODE_HOMOGLYPHS = {
#     '\u0430': ('а', 'a',   'Cyrillic'),
#     '\u0435': ('е', 'e',   'Cyrillic'),
#     '\u043e': ('о', 'o',   'Cyrillic'),
#     '\u0440': ('р', 'p',   'Cyrillic'),
#     '\u0441': ('с', 'c',   'Cyrillic'),
#     '\u0445': ('х', 'x',   'Cyrillic'),
#     '\u0455': ('ѕ', 's',   'Cyrillic'),
#     '\u0456': ('і', 'i',   'Cyrillic'),
#     '\u0406': ('І', 'I/l', 'Cyrillic'),
#     '\u04cf': ('ӏ', 'l',   'Cyrillic'),
#     '\u0458': ('ј', 'j',   'Cyrillic'),
#     '\u0501': ('ԁ', 'd',   'Cyrillic'),
#     '\u0410': ('А', 'A',   'Cyrillic'),
#     '\u0412': ('В', 'B',   'Cyrillic'),
#     '\u0421': ('С', 'C',   'Cyrillic'),
#     '\u0415': ('Е', 'E',   'Cyrillic'),
#     '\u041a': ('К', 'K',   'Cyrillic'),
#     '\u041c': ('М', 'M',   'Cyrillic'),
#     '\u041d': ('Н', 'H',   'Cyrillic'),
#     '\u041e': ('О', 'O',   'Cyrillic'),
#     '\u0420': ('Р', 'P',   'Cyrillic'),
#     '\u0422': ('Т', 'T',   'Cyrillic'),
#     '\u0425': ('Х', 'X',   'Cyrillic'),
#     '\u03bf': ('ο', 'o',   'Greek'),
#     '\u03c1': ('ρ', 'p',   'Greek'),
#     '\u03b1': ('α', 'a',   'Greek'),
#     '\u0391': ('Α', 'A',   'Greek'),
#     '\u0392': ('Β', 'B',   'Greek'),
#     '\u0395': ('Ε', 'E',   'Greek'),
#     '\u039a': ('Κ', 'K',   'Greek'),
#     '\u039c': ('М', 'M',   'Greek'),
#     '\u039d': ('Ν', 'N',   'Greek'),
#     '\u039f': ('Ο', 'O',   'Greek'),
#     '\u03a1': ('Ρ', 'P',   'Greek'),
#     '\u03a4': ('Т', 'T',   'Greek'),
#     '\u03a7': ('Χ', 'X',   'Greek'),
#     '\u0261': ('ɡ', 'g',   'IPA'),
#     '\u1d0f': ('ᴏ', 'o',   'Small-caps'),
#     '\u2113': ('ℓ', 'l',   'Letterlike'),
# }

# BRAND_SPOOFS = {
#     'paypal':     ['paypa1', 'paypaI', 'paypai', 'pay-pal', 'paypаl'],
#     'amazon':     ['arnazon', 'amaz0n', 'amazom', 'amаzon', 'amazon-secure'],
#     'google':     ['g00gle',  'googIe', 'googlе', 'google-verify'],
#     'microsoft':  ['micros0ft','microsofl','mlcrosoft','micrоsoft'],
#     'apple':      ['app1e',   'appIe',  'аpple',  'apple-id'],
#     'netflix':    ['netfl1x', 'netfIix','netfl1ix'],
#     'facebook':   ['faceb00k','fаcebook','faceb0ok'],
#     'instagram':  ['lnstagram','Instаgram','instagr4m'],
#     'twitter':    ['tvvitter','twltter','twittеr'],
#     'linkedin':   ['llnkedin','linkedln','lInkedin'],
#     'wellsfargo': ['vvellsfargo','we11sfargo','wellsf4rgo'],
#     'chase':      ['chas3',   'chаse',  'chase-bank'],
#     'hdfc':       ['hdfc-bank-secure','hdfcbank-verify'],
#     'sbi':        ['sbi-secure','sbionline-verify'],
#     'icici':      ['icici-secure','icicibankverify'],
#     'fedex':      ['fed3x',   'fedеx',  'fedex-delivery'],
#     'dhl':        ['dhl-delivery','dhl-tracking-secure'],
#     'ups':        ['ups-delivery','ups-tracking-secure'],
#     'dropbox':    ['dr0pbox', 'dropb0x'],
#     'icloud':     ['icl0ud',  'iclоud', 'icloud-verify'],
#     'outlook':    ['outl00k', 'outIook','outlook-verify'],
#     'yahoo':      ['yah00',   'yahoо'],
# }
# ALL_BRANDS = list(BRAND_SPOOFS.keys())

# SUSPICIOUS_TLDS = {
#     '.xyz','.top','.click','.loan','.work','.gq','.ml','.cf',
#     '.tk','.pw','.info','.biz','.cc','.su','.party','.racing',
#     '.win','.download','.stream',
# }

# TRUSTED_DOMAINS = {
#     'hdfcbank.com','sbi.co.in','icicibank.com','axisbank.com',
#     'kotak.com','pnb.co.in','bankofbaroda.in','canarabank.in',
#     'unionbankofindia.co.in','yesbank.in','indusind.com',
#     'paytm.com','phonepe.com','gpay.com','razorpay.com',
#     'paypal.com','stripe.com','visa.com','mastercard.com',
#     'chase.com','wellsfargo.com','bankofamerica.com','citibank.com',
#     'amazon.com','amazon.in','flipkart.com','myntra.com','meesho.com',
#     'snapdeal.com','nykaa.com','tatacliq.com','reliancedigital.in',
#     'google.com','gmail.com','youtube.com','googlemail.com',
#     'microsoft.com','outlook.com','hotmail.com','live.com',
#     'apple.com','icloud.com','yahoo.com','ymail.com',
#     'linkedin.com','twitter.com','facebook.com','instagram.com',
#     'coursera.org','udemy.com','edx.org','nptel.ac.in',
#     'khanacademy.org','skillshare.com','udacity.com',
#     'unacademy.com','byju.com','vedantu.com','upgrad.com',
#     'fedex.com','dhl.com','ups.com','indiapost.gov.in',
#     'bluedart.com','delhivery.com','ecomexpress.com',
#     'netflix.com','spotify.com','adobe.com','dropbox.com',
#     'slack.com','zoom.us','github.com','stackoverflow.com',
# }

# DOMAIN_RE = re.compile(
#     r'https?://[^\s<>"\'\]]+|'
#     r'www\.[a-zA-Z0-9\-\.]+[a-zA-Z0-9]|'
#     r'\b([a-zA-Z][a-zA-Z0-9\-]*)\.(com|net|org|io|in|co|xyz|top|click|info|biz|cc|tk|pw|gq|ml|cf)\b'
# )

# SAFE_CONTEXT_PATTERNS = [
#     r'your (transaction|payment|transfer|order|purchase|bill|statement|invoice) (of|for|worth|amount)',
#     r'(successfully|has been) (debited|credited|processed|completed|confirmed)',
#     r'(account|card) (statement|summary|balance|number ending)',
#     r'otp (for|to|is|:)',
#     r'one.?time.?password',
#     r'(upi|neft|rtgs|imps) (transaction|transfer|payment)',
#     r'(your|the) (order|shipment|parcel|package|delivery) (has|is|will)',
#     r'track your (order|shipment|package|delivery)',
#     r'(estimated|expected) delivery',
#     r'(unsubscribe|manage (your )?preferences|view (in|this) browser|email preferences)',
#     r'(you (are|were) (subscribed|signed up|enrolled)|subscription (confirmed|activated))',
#     r'(weekly|monthly|daily) (newsletter|digest|update|roundup)',
#     r'(exclusive|special) (offer|deal|discount) for (you|our (members|subscribers|customers))',
#     r'(course|class|lesson|module|lecture|assignment|quiz|certificate) (enrolled|started|completed|available|due|reminder)',
#     r'(welcome to|you(\'ve| have) (enrolled|joined|registered for))',
#     r'(your|the) (certificate|completion|progress|score|grade)',
#     r'(instructor|mentor|tutor) (message|reply|feedback)',
#     r'(live (session|class|webinar)|office hours|q&a)',
# ]

# PHISHING_SIGNALS = [
#     r'(verify|confirm|update|validate).{0,30}(account|identity|information|details|credentials)',
#     r'(account|password|credential).{0,20}(suspended|locked|disabled|compromised|expired|unauthorized)',
#     r'(click|tap|open).{0,20}(link|button|here).{0,30}(immediately|now|urgent|within \d+)',
#     r'(enter|provide|submit).{0,20}(password|pin|otp|cvv|card number|social security|aadhaar)',
#     r'(won|winner|selected|chosen|congratulations).{0,40}(prize|lottery|reward|gift card|\$[\d,]+|₹[\d,]+)',
#     r'(invoice|payment|amount).{0,30}(overdue|past due|immediately|pending|unpaid).{0,20}(click|pay|open)',
#     r'(irs|income tax|it department).{0,30}(refund|notice|penalty|legal action)',
#     r'(unusual|suspicious|unauthorized).{0,20}(activity|login|access|transaction).{0,30}(verify|confirm|click)',
#     r'your (account|card|access).{0,20}will be (terminated|closed|suspended|deleted).{0,20}(unless|if not)',
# ]

# def _is_from_trusted_domain(text):
#     text_lower = text.lower()
#     return any(domain in text_lower for domain in TRUSTED_DOMAINS)

# def _has_safe_context(text):
#     text_lower = text.lower()
#     return any(re.search(pattern, text_lower) for pattern in SAFE_CONTEXT_PATTERNS)

# def _count_phishing_signals(text):
#     text_lower = text.lower()
#     return sum(1 for pattern in PHISHING_SIGNALS if re.search(pattern, text_lower))

# def _parse_domains(text):
#     out = []
#     for m in DOMAIN_RE.finditer(text):
#         raw = m.group(0)
#         orig = re.sub(r'^https?://', '', raw, flags=re.I).split('/')[0].split('?')[0].strip()
#         if '.' in orig:
#             out.append((raw, orig, orig.lower()))
#     return out

# def _check_l_vs_I(root_orig, root_lc):
#     findings = []
#     if 'I' in root_orig:
#         with_l = root_orig.replace('I', 'l').lower()
#         if any(b == with_l or b in with_l for b in ALL_BRANDS):
#             findings.append({
#                 'type': 'capital_I_as_l', 'severity': 'critical',
#                 'char': 'I (capital-I)', 'looks_like': 'l (lowercase-L)',
#                 'script': 'ASCII', 'context': root_orig,
#                 'message': f'🔴 I → l TRICK: "{root_orig}" uses capital "I" that looks like lowercase "l" → reads as "{with_l}"',
#             })
#         else:
#             findings.append({
#                 'type': 'capital_I_in_domain', 'severity': 'high',
#                 'char': 'I (capital-I)', 'looks_like': 'l (lowercase-L)',
#                 'script': 'ASCII', 'context': root_orig,
#                 'message': f'⚠️ CAPITAL-I IN DOMAIN: "{root_orig}" — uppercase characters should not be inside normal active web strings.',
#             })
#     if root_lc.startswith('l') and len(root_lc) > 3:
#         rest = root_lc[1:]
#         for brand in ALL_BRANDS:
#             if len(brand) > 1 and rest == brand[1:]:
#                 findings.append({
#                     'type': 'l_as_capital_I', 'severity': 'critical',
#                     'char': 'l (lowercase-L)', 'looks_like': 'I (capital-I)',
#                     'script': 'ASCII', 'context': root_orig,
#                     'message': f'🔴 l → I TRICK: "{root_orig}" starts with lowercase "l" that mimics uppercase "I" for brand "{brand.capitalize()}"',
#                 })
#                 break
#     return findings

# def detect_homoglyphs(text):
#     findings = []
#     seen_unicode = set()
#     for i, char in enumerate(text):
#         if char in UNICODE_HOMOGLYPHS:
#             info = UNICODE_HOMOGLYPHS[char]
#             key  = (char, info[1])
#             if key not in seen_unicode:
#                 seen_unicode.add(key)
#                 ctx = text[max(0, i-12): min(len(text), i+12)].replace('\n', ' ')
#                 findings.append({
#                     'type': 'unicode_homoglyph', 'severity': 'high',
#                     'char': info[0], 'looks_like': info[1], 'script': info[2],
#                     'context': ctx,
#                     'message': f'🔴 UNICODE SPOOF: "{info[0]}" ({info[2]}) resembles Latin "{info[1]}" — context: "...{ctx}..."',
#                 })

#     for raw_url, orig, lc in _parse_domains(text):
#         base = lc.replace('www.', '')
#         if any(base == td or base.endswith('.' + td) for td in TRUSTED_DOMAINS):
#             continue

#         root_orig = orig.replace('www.', '').split('.')[0]
#         root_lc   = lc.replace('www.', '').split('.')[0]
#         findings.extend(_check_l_vs_I(root_orig, root_lc))

#         if 'rn' in root_lc:
#             candidate = root_lc.replace('rn', 'm')
#             if any(b == candidate or b in candidate for b in ALL_BRANDS):
#                 findings.append({
#                     'type': 'rn_as_m', 'severity': 'critical',
#                     'char': 'rn', 'looks_like': 'm', 'script': 'ASCII', 'context': lc,
#                     'message': f'🔴 rn → m TRICK: "{lc}" — characters "rn" visually merge to mimic "m"',
#                 })

#         if 'vv' in root_lc:
#             candidate = root_lc.replace('vv', 'w')
#             if any(b in candidate for b in ALL_BRANDS):
#                 findings.append({
#                     'type': 'vv_as_w', 'severity': 'critical',
#                     'char': 'vv', 'looks_like': 'w', 'script': 'ASCII', 'context': lc,
#                     'message': f'🔴 vv → w TRICK: "{lc}" — sequential symbols "vv" emulate "w"',
#                 })

#         if '0' in root_lc:
#             candidate = root_lc.replace('0', 'o')
#             if any(b in candidate for b in ALL_BRANDS):
#                 findings.append({
#                     'type': 'zero_as_o', 'severity': 'critical',
#                     'char': '0 (zero)', 'looks_like': 'O (letter)', 'script': 'ASCII', 'context': lc,
#                     'message': f'🔴 0 → O TRICK: "{lc}" — zero digit replaces vowel "O"',
#                 })

#         if '1' in root_lc:
#             cand_l  = root_lc.replace('1', 'l')
#             cand_i  = root_lc.replace('1', 'i')
#             match_l = any(b in cand_l for b in ALL_BRANDS)
#             match_i = any(b in cand_i for b in ALL_BRANDS)
#             if match_l or match_i:
#                 sub_char = 'i' if match_i else 'l'
#                 findings.append({
#                     'type': 'one_as_l', 'severity': 'critical',
#                     'char': '1 (one)', 'looks_like': f'{sub_char} (letter)',
#                     'script': 'ASCII', 'context': lc,
#                     'message': f'🔴 1 → {sub_char} TRICK: "{lc}" — numeric digit "1" replaces standard alpha characters',
#                 })

#         for tld in SUSPICIOUS_TLDS:
#             if lc.endswith(tld):
#                 findings.append({
#                     'type': 'suspicious_tld', 'severity': 'medium',
#                     'char': tld, 'looks_like': '', 'script': 'TLD', 'context': lc,
#                     'message': f'🟡 SUSPICIOUS TLD: "{lc}" runs on a high-risk registration zone TLD variant string "{tld}"',
#                 })
#                 break

#         for brand, variants in BRAND_SPOOFS.items():
#             if any(v in root_lc for v in variants):
#                 matched_v = next(v for v in variants if v in root_lc)
#                 findings.append({
#                     'type': 'known_spoof', 'severity': 'critical',
#                     'char': matched_v, 'looks_like': brand, 'script': 'ASCII', 'context': lc,
#                     'message': f'🔴 KNOWN PHISHING STRING: "{lc}" contains unauthorized mutation "{matched_v}" targeted at impersonating "{brand}"',
#                 })
#                 break
#             else:
#                 if brand in root_lc:
#                     legit = [f"{brand}.com", f"{brand}.net", f"{brand}.org", f"www.{brand}.com", f"{brand}.co.uk", f"{brand}.in"]
#                     if not any(lc == d or lc.endswith(f'.{brand}.com') for d in legit):
#                         if not any(f.get('context','') == lc and brand in f.get('message','') for f in findings):
#                             findings.append({
#                                 'type': 'brand_in_domain', 'severity': 'high',
#                                 'char': brand, 'looks_like': f'{brand}.com', 'script': 'Domain',
#                                 'context': lc,
#                                 'message': f'⚠️ BRAND IMPERSONATION: Domain "{lc}" includes trademarked phrase "{brand}" but resolves outside verified channels.',
#                             })
#                     break

#     if re.search(r'p@y|@m@z|@pp1e', text, re.I):
#         findings.append({
#             'type': 'at_trick', 'severity': 'high',
#             'char': '@', 'looks_like': 'a', 'script': 'ASCII', 'context': '',
#             'message': '🔴 OBFUSCATION ATTEMPT: Symbol "@" injected to mask automated pattern tracking.',
#         })

#     seen, unique = set(), []
#     for f in findings:
#         if f['message'] not in seen:
#             seen.add(f['message'])
#             unique.append(f)
#     return unique

# def findings_to_warnings(findings):
#     return [f['message'] for f in findings]

# def _gemini_call(model_name, contents):
#     return client.models.generate_content(model=model_name, contents=contents)

# def _gemini_error_msg(e):
#     err = str(e)
#     if '429' in err or 'RESOURCE_EXHAUSTED' in err:
#         return "⚠️ Quota threshold reached on current API provisioning configurations."
#     elif '403' in err or 'API_KEY_INVALID' in err or 'PERMISSION_DENIED' in err:
#         return "⚠️ Gemini Identity Authentication rejected: Key structure invalid or revoked."
#     else:
#         return f"⚠️ Cloud Endpoint Unreachable. Local mitigation metrics deployed. ({err[:60]})"

# def check_url_safety(url):
#     result = {
#         'url': url, 'risk_level': 'safe', 'risk_score': 0,
#         'findings': [], 'ssl_valid': None,
#         'redirect_chain': [], 'domain': '', 'ip_address': '',
#     }
#     if not url.startswith('http'):
#         url = 'https://' + url
#     parsed = urllib.parse.urlparse(url)
#     domain = parsed.netloc or parsed.path.split('/')[0]
#     result['domain'] = domain
#     lc = domain.replace('www.', '').lower()

#     if any(lc == td or lc.endswith('.' + td) for td in TRUSTED_DOMAINS):
#         result['findings'].append("✅ Domain confirmed via global trusted authority channels.")
#         result['risk_level'] = 'safe'
#         return result

#     SUSP_KW = ['verify','secure','login','update','confirm','account','banking','signin','password','credential','unlock','suspend','recover','validate','authenticate','urgent','alert','free','winner','prize','claim','reward','refund']
#     hits = [k for k in SUSP_KW if k in url.lower()]
#     if hits:
#         result['risk_score'] += min(len(hits) * 8, 40)
#         result['findings'].append(f"🔴 Suspicious keywords detected in endpoint context: {', '.join(hits)}")

#     for tld in SUSPICIOUS_TLDS:
#         if lc.endswith(tld):
#             result['risk_score'] += 30
#             result['findings'].append(f"🔴 high-risk registration zone TLD variant string '{tld}' detected.")
#             break

#     if re.match(r'^\d{1,3}(\.\d{1,3}){3}', domain):
#         result['risk_score'] += 40
#         result['findings'].append("🔴 Endpoint bypasses DNS translation using raw target IP notation.")

#     if len(lc.split('.')) > 4:
#         result['risk_score'] += 20
#         result['findings'].append("Subdomain levels exceed traditional operational deep-nest configurations.")

#     glyph_findings = detect_homoglyphs(url)
#     if glyph_findings:
#         result['risk_score'] += min(25 * len(glyph_findings), 50)
#         result['findings'].extend(findings_to_warnings(glyph_findings))

#     try:
#         hostname = domain.split(':')[0]
#         ctx = ssl.create_default_context()
#         with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
#             s.settimeout(2); s.connect((hostname, 443))
#             result['ssl_valid'] = True
#             result['findings'].append("✅ TLS Handshake validates correctly against host infrastructure.")
#     except Exception:
#         result['ssl_valid'] = False
#         result['findings'].append("⚠️ Encryption Layer verification handshake timed out or failed.")

#     score = min(result['risk_score'], 100)
#     result['risk_score'] = score
#     result['risk_level'] = ('phishing' if score >= 60 else 'suspicious' if score >= 30 else 'safe')
#     return result

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     data = request.json or {}
#     email_text = data.get('email', '')
#     if not email_text:
#         return jsonify({'error': 'No content strings submitted.'})

#     result      = phishing_detector(email_text, truncation=True, max_length=512)[0]
#     local_score = round(result['score'] * 100, 2)
#     gf          = detect_homoglyphs(email_text)
#     hw          = findings_to_warnings(gf)

#     trusted_sender  = _is_from_trusted_domain(email_text)
#     has_safe_ctx    = _has_safe_context(email_text)
#     phishing_hits   = _count_phishing_signals(email_text)

#     prompt = f"""You are a Level 3 SOC Analyst. Analyze this data.
# ALWAYS declare SAFE if transactional from verified bank engines, normal newsletter footprints, standard educational modules.
# ONLY flag PHISHING if clear credential harvest hooks, artificial expiration context traps, homoglyphs.
# Text: '{email_text}'
# Respond EXACTLY in this format:
# FINAL_VERDICT: [SAFE or PHISHING]
# EXPLANATION: [1 sentence analysis]"""

#     try:
#         gr     = _gemini_call('gemini-2.5-flash', prompt)
#         rt     = gr.text
#         status = "safe" if "FINAL_VERDICT: SAFE" in rt.upper() else "phishing"
#         try:    explanation = rt.split("EXPLANATION:")[1].strip()
#         except: explanation = rt

#         if status == "phishing" and trusted_sender and phishing_hits == 0:
#             status      = "safe"
#             explanation = "Verified alignment configuration confirms signature legitimacy traits."

#     except Exception as e:
#         print(f"HYBRID ROUTING FAIL: {e}")
#         explanation = _gemini_error_msg(e)

#         bert_says_malicious = (result['label'] == "LABEL_1" and local_score > 75)

#         if hw:
#             status = "phishing"
#             explanation += " Local Engine Override: Active target homoglyph markers identified in string."
#         elif phishing_hits >= 1 and not trusted_sender:
#             status = "phishing"
#             explanation += " Local Engine Override: High core heuristics threat indicators triggered."
#         elif bert_says_malicious and not trusted_sender:
#             status = "phishing"
#             explanation += " Local Engine Override: High vector weight classification classification matching."
#         else:
#             status = "safe"

#     if hw and status == 'safe' and not trusted_sender:
#         status      = 'suspicious'
#         explanation += " Lookalike structural notation characters found within processing logs."

#     return jsonify({
#         'status':             status,
#         'confidence':         local_score,
#         'explanation':        explanation,
#         'homoglyph_warnings': hw,
#         'homoglyph_details':  gf,
#     })


# # ─── REINSTATED AND UPDATED URL SANDBOX ROUTE ─────────────────────
# @app.route('/check-url', methods=['POST'])
# def check_url():
#     data = request.json or {}
#     url  = data.get('url', '').strip()
#     if not url:
#         return jsonify({'error': 'No URL provided'})

#     # Run structural security sandboxing checks
#     result = check_url_safety(url)
    
#     try:
#         prompt = f"""Cybersecurity expert: is this URL safe to open or is it deceptive/phishing? URL: {url}
# Respond EXACTLY in this format:
# FINAL_VERDICT: [SAFE or SUSPICIOUS or PHISHING]
# EXPLANATION: [1-2 sentences overview]"""
        
#         gr    = _gemini_call('gemini-2.5-flash', prompt)
#         gtext = gr.text
        
#         gv = ('phishing'   if 'PHISHING'   in gtext.upper() else
#               'suspicious' if 'SUSPICIOUS' in gtext.upper() else 'safe')
              
#         try:    ge = gtext.split("EXPLANATION:")[1].strip()
#         except: ge = gtext
        
#     except Exception as e:
#         print(f"GEMINI ERROR (check-url): {e}")
#         gv = 'error'
#         ge = _gemini_error_msg(e)

#     result['gemini_verdict']     = gv
#     result['gemini_explanation'] = ge
    
#     # Calculate unified verdict parameters
#     levels = {'safe': 0, 'suspicious': 1, 'phishing': 2, 'error': 0}
#     result['final_verdict'] = max(result['risk_level'], gv, key=lambda x: levels.get(x, 0))
    
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)






import os
import base64
import re
import urllib.parse
import socket
import ssl
import requests
from flask import Flask, request, jsonify, render_template
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from google import genai
from dotenv import load_dotenv

# 1. Load the environment parameters first
load_dotenv()

# 2. Extract and verify the API key availability
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("🚨 SEVERE CRITICAL: 'GEMINI_API_KEY' was not found by Flask app.py!")
    print("Ensure your .env file is in the root directory alongside app.py.")
else:
    print(f"🔒 App initialized using API Key: {api_key[:8]}...[Redacted]")

# 3. Instantiate engine structures
client = genai.Client(api_key=api_key)
app = Flask(__name__)

# Local BERT model configuration
model_path = "./my_phishing_model"
model      = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=2)
tokenizer  = AutoTokenizer.from_pretrained(model_path)
phishing_detector = pipeline("text-classification", model=model, tokenizer=tokenizer)

UNICODE_HOMOGLYPHS = {
    '\u0430': ('а', 'a',   'Cyrillic'),
    '\u0435': ('е', 'e',   'Cyrillic'),
    '\u043e': ('о', 'o',   'Cyrillic'),
    '\u0440': ('р', 'p',   'Cyrillic'),
    '\u0441': ('с', 'c',   'Cyrillic'),
    '\u0445': ('х', 'x',   'Cyrillic'),
    '\u0455': ('ѕ', 's',   'Cyrillic'),
    '\u0456': ('і', 'i',   'Cyrillic'),
    '\u0406': ('І', 'I/l', 'Cyrillic'),
    '\u04cf': ('ӏ', 'l',   'Cyrillic'),
    '\u0458': ('ј', 'j',   'Cyrillic'),
    '\u0501': ('ԁ', 'd',   'Cyrillic'),
    '\u0410': ('А', 'A',   'Cyrillic'),
    '\u0412': ('В', 'B',   'Cyrillic'),
    '\u0421': ('С', 'C',   'Cyrillic'),
    '\u0415': ('Е', 'E',   'Cyrillic'),
    '\u041a': ('К', 'K',   'Cyrillic'),
    '\u041c': ('М', 'M',   'Cyrillic'),
    '\u041d': ('Н', 'H',   'Cyrillic'),
    '\u041e': ('О', 'O',   'Cyrillic'),
    '\u0420': ('Р', 'P',   'Cyrillic'),
    '\u0422': ('Т', 'T',   'Cyrillic'),
    '\u0425': ('Х', 'X',   'Cyrillic'),
    '\u03bf': ('ο', 'o',   'Greek'),
    '\u03c1': ('ρ', 'p',   'Greek'),
    '\u03b1': ('α', 'a',   'Greek'),
    '\u0391': ('Α', 'A',   'Greek'),
    '\u0392': ('Β', 'B',   'Greek'),
    '\u0395': ('Ε', 'E',   'Greek'),
    '\u039a': ('Κ', 'K',   'Greek'),
    '\u039c': ('М', 'M',   'Greek'),
    '\u039d': ('Ν', 'N',   'Greek'),
    '\u039f': ('Ο', 'O',   'Greek'),
    '\u03a1': ('Ρ', 'P',   'Greek'),
    '\u03a4': ('Т', 'T',   'Greek'),
    '\u03a7': ('Χ', 'X',   'Greek'),
    '\u0261': ('ɡ', 'g',   'IPA'),
    '\u1d0f': ('ᴏ', 'o',   'Small-caps'),
    '\u2113': ('ℓ', 'l',   'Letterlike'),
}

BRAND_SPOOFS = {
    'paypal':     ['paypa1', 'paypaI', 'paypai', 'pay-pal', 'paypаl'],
    'amazon':     ['arnazon', 'amaz0n', 'amazom', 'amаzon', 'amazon-secure'],
    'google':     ['g00gle',  'googIe', 'googlе', 'google-verify'],
    'microsoft':  ['micros0ft','microsofl','mlcrosoft','micrоsoft'],
    'apple':      ['app1e',   'appIe',  'аpple',  'apple-id'],
    'netflix':    ['netfl1x', 'netfIix','netfl1ix'],
    'facebook':   ['faceb00k','fаcebook','faceb0ok'],
    'instagram':  ['lnstagram','Instаgram','instagr4m'],
    'twitter':    ['tvvitter','twltter','twittеr'],
    'linkedin':   ['llnkedin','linkedln','lInkedin'],
    'wellsfargo': ['vvellsfargo','we11sfargo','wellsf4rgo'],
    'chase':      ['chas3',   'chаse',  'chase-bank'],
    'hdfc':       ['hdfc-bank-secure','hdfcbank-verify'],
    'sbi':        ['sbi-secure','sbionline-verify'],
    'icici':      ['icici-secure','icicibankverify'],
    'fedex':      ['fed3x',   'fedеx',  'fedex-delivery'],
    'dhl':        ['dhl-delivery','dhl-tracking-secure'],
    'ups':        ['ups-delivery','ups-tracking-secure'],
    'dropbox':    ['dr0pbox', 'dropb0x'],
    'icloud':     ['icl0ud',  'iclоud', 'icloud-verify'],
    'outlook':    ['outl00k', 'outIook','outlook-verify'],
    'yahoo':      ['yah00',   'yahoо'],
}
ALL_BRANDS = list(BRAND_SPOOFS.keys())

SUSPICIOUS_TLDS = {
    '.xyz','.top','.click','.loan','.work','.gq','.ml','.cf',
    '.tk','.pw','.info','.biz','.cc','.su','.party','.racing',
    '.win','.download','.stream',
}

TRUSTED_DOMAINS = {
    'hdfcbank.com','sbi.co.in','icicibank.com','axisbank.com',
    'kotak.com','pnb.co.in','bankofbaroda.in','canarabank.in',
    'unionbankofindia.co.in','yesbank.in','indusind.com',
    'paytm.com','phonepe.com','gpay.com','razorpay.com',
    'paypal.com','stripe.com','visa.com','mastercard.com',
    'chase.com','wellsfargo.com','bankofamerica.com','citibank.com',
    'amazon.com','amazon.in','flipkart.com','myntra.com','meesho.com',
    'snapdeal.com','nykaa.com','tatacliq.com','reliancedigital.in',
    'google.com','gmail.com','youtube.com','googlemail.com',
    'microsoft.com','outlook.com','hotmail.com','live.com',
    'apple.com','icloud.com','yahoo.com','ymail.com',
    'linkedin.com','twitter.com','facebook.com','instagram.com',
    'coursera.org','udemy.com','edx.org','nptel.ac.in',
    'khanacademy.org','skillshare.com','udacity.com',
    'unacademy.com','byju.com','vedantu.com','upgrad.com',
    'fedex.com','dhl.com','ups.com','indiapost.gov.in',
    'bluedart.com','delhivery.com','ecomexpress.com',
    'netflix.com','spotify.com','adobe.com','dropbox.com',
    'slack.com','zoom.us','github.com','stackoverflow.com',
}

DOMAIN_RE = re.compile(
    r'https?://[^\s<>"\'\]]+|'
    r'www\.[a-zA-Z0-9\-\.]+[a-zA-Z0-9]|'
    r'\b([a-zA-Z][a-zA-Z0-9\-]*)\.(com|net|org|io|in|co|xyz|top|click|info|biz|cc|tk|pw|gq|ml|cf)\b'
)

SAFE_CONTEXT_PATTERNS = [
    r'your (transaction|payment|transfer|order|purchase|bill|statement|invoice) (of|for|worth|amount)',
    r'(successfully|has been) (debited|credited|processed|completed|confirmed)',
    r'(account|card) (statement|summary|balance|number ending)',
    r'otp (for|to|is|:)',
    r'one.?time.?password',
    r'(upi|neft|rtgs|imps) (transaction|transfer|payment)',
    r'(your|the) (order|shipment|parcel|package|delivery) (has|is|will)',
    r'track your (order|shipment|package|delivery)',
    r'(estimated|expected) delivery',
    r'(unsubscribe|manage (your )?preferences|view (in|this) browser|email preferences)',
    r'(you (are|were) (subscribed|signed up|enrolled)|subscription (confirmed|activated))',
    r'(weekly|monthly|daily) (newsletter|digest|update|roundup)',
    r'(exclusive|special) (offer|deal|discount) for (you|our (members|subscribers|customers))',
    r'(course|class|lesson|module|lecture|assignment|quiz|certificate) (enrolled|started|completed|available|due|reminder)',
    r'(welcome to|you(\'ve| have) (enrolled|joined|registered for))',
    r'(your|the) (certificate|completion|progress|score|grade)',
    r'(instructor|mentor|tutor) (message|reply|feedback)',
    r'(live (session|class|webinar)|office hours|q&a)',
]

PHISHING_SIGNALS = [
    r'(verify|confirm|update|validate).{0,30}(account|identity|information|details|credentials)',
    r'(account|password|credential).{0,20}(suspended|locked|disabled|compromised|expired|unauthorized)',
    r'(click|tap|open).{0,20}(link|button|here).{0,30}(immediately|now|urgent|within \d+)',
    r'(enter|provide|submit).{0,20}(password|pin|otp|cvv|card number|social security|aadhaar)',
    r'(won|winner|selected|chosen|congratulations).{0,40}(prize|lottery|reward|gift card|\$[\d,]+|₹[\d,]+)',
    r'(invoice|payment|amount).{0,30}(overdue|past due|immediately|pending|unpaid).{0,20}(click|pay|open)',
    r'(irs|income tax|it department).{0,30}(refund|notice|penalty|legal action)',
    r'(unusual|suspicious|unauthorized).{0,20}(activity|login|access|transaction).{0,30}(verify|confirm|click)',
    r'your (account|card|access).{0,20}will be (terminated|closed|suspended|deleted).{0,20}(unless|if not)',
]

def _is_from_trusted_domain(text):
    text_lower = text.lower()
    return any(domain in text_lower for domain in TRUSTED_DOMAINS)

def _has_safe_context(text):
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in SAFE_CONTEXT_PATTERNS)

def _count_phishing_signals(text):
    text_lower = text.lower()
    return sum(1 for pattern in PHISHING_SIGNALS if re.search(pattern, text_lower))

def _parse_domains(text):
    out = []
    for m in DOMAIN_RE.finditer(text):
        raw = m.group(0)
        orig = re.sub(r'^https?://', '', raw, flags=re.I).split('/')[0].split('?')[0].strip()
        if '.' in orig:
            out.append((raw, orig, orig.lower()))
    return out

def _check_l_vs_I(root_orig, root_lc):
    findings = []
    if 'I' in root_orig:
        with_l = root_orig.replace('I', 'l').lower()
        if any(b == with_l or b in with_l for b in ALL_BRANDS):
            findings.append({
                'type': 'capital_I_as_l', 'severity': 'critical',
                'char': 'I (capital-I)', 'looks_like': 'l (lowercase-L)',
                'script': 'ASCII', 'context': root_orig,
                'message': f'🔴 I → l TRICK: "{root_orig}" uses capital "I" that looks like lowercase "l" → reads as "{with_l}"',
            })
        else:
            findings.append({
                'type': 'capital_I_in_domain', 'severity': 'high',
                'char': 'I (capital-I)', 'looks_like': 'l (lowercase-L)',
                'script': 'ASCII', 'context': root_orig,
                'message': f'⚠️ CAPITAL-I IN DOMAIN: "{root_orig}" — uppercase characters should not be inside normal active web strings.',
            })
    if root_lc.startswith('l') and len(root_lc) > 3:
        rest = root_lc[1:]
        for brand in ALL_BRANDS:
            if len(brand) > 1 and rest == brand[1:]:
                findings.append({
                    'type': 'l_as_capital_I', 'severity': 'critical',
                    'char': 'l (lowercase-L)', 'looks_like': 'I (capital-I)',
                    'script': 'ASCII', 'context': root_orig,
                    'message': f'🔴 l → I TRICK: "{root_orig}" starts with lowercase "l" that mimics uppercase "I" for brand "{brand.capitalize()}"',
                })
                break
    return findings

def detect_homoglyphs(text):
    findings = []
    seen_unicode = set()
    for i, char in enumerate(text):
        if char in UNICODE_HOMOGLYPHS:
            info = UNICODE_HOMOGLYPHS[char]
            key  = (char, info[1])
            if key not in seen_unicode:
                seen_unicode.add(key)
                ctx = text[max(0, i-12): min(len(text), i+12)].replace('\n', ' ')
                findings.append({
                    'type': 'unicode_homoglyph', 'severity': 'high',
                    'char': info[0], 'looks_like': info[1], 'script': info[2],
                    'context': ctx,
                    'message': f'🔴 UNICODE SPOOF: "{info[0]}" ({info[2]}) resembles Latin "{info[1]}" — context: "...{ctx}..."',
                })

    for raw_url, orig, lc in _parse_domains(text):
        base = lc.replace('www.', '')
        if any(base == td or base.endswith('.' + td) for td in TRUSTED_DOMAINS):
            continue

        root_orig = orig.replace('www.', '').split('.')[0]
        root_lc   = lc.replace('www.', '').split('.')[0]
        findings.extend(_check_l_vs_I(root_orig, root_lc))

        if 'rn' in root_lc:
            candidate = root_lc.replace('rn', 'm')
            if any(b == candidate or b in candidate for b in ALL_BRANDS):
                findings.append({
                    'type': 'rn_as_m', 'severity': 'critical',
                    'char': 'rn', 'looks_like': 'm', 'script': 'ASCII', 'context': lc,
                    'message': f'🔴 rn → m TRICK: "{lc}" — characters "rn" visually merge to mimic "m"',
                })

        if 'vv' in root_lc:
            candidate = root_lc.replace('vv', 'w')
            if any(b in candidate for b in ALL_BRANDS):
                findings.append({
                    'type': 'vv_as_w', 'severity': 'critical',
                    'char': 'vv', 'looks_like': 'w', 'script': 'ASCII', 'context': lc,
                    'message': f'🔴 vv → w TRICK: "{lc}" — sequential symbols "vv" emulate "w"',
                })

        if '0' in root_lc:
            candidate = root_lc.replace('0', 'o')
            if any(b in candidate for b in ALL_BRANDS):
                findings.append({
                    'type': 'zero_as_o', 'severity': 'critical',
                    'char': '0 (zero)', 'looks_like': 'O (letter)', 'script': 'ASCII', 'context': lc,
                    'message': f'🔴 0 → O TRICK: "{lc}" — zero digit replaces vowel "O"',
                })

        if '1' in root_lc:
            cand_l  = root_lc.replace('1', 'l')
            cand_i  = root_lc.replace('1', 'i')
            match_l = any(b in cand_l for b in ALL_BRANDS)
            match_i = any(b in cand_i for b in ALL_BRANDS)
            if match_l or match_i:
                sub_char = 'i' if match_i else 'l'
                findings.append({
                    'type': 'one_as_l', 'severity': 'critical',
                    'char': '1 (one)', 'looks_like': f'{sub_char} (letter)',
                    'script': 'ASCII', 'context': lc,
                    'message': f'🔴 1 → {sub_char} TRICK: "{lc}" — numeric digit "1" replaces standard alpha characters',
                })

        for tld in SUSPICIOUS_TLDS:
            if lc.endswith(tld):
                findings.append({
                    'type': 'suspicious_tld', 'severity': 'medium',
                    'char': tld, 'looks_like': '', 'script': 'TLD', 'context': lc,
                    'message': f'🟡 SUSPICIOUS TLD: "{lc}" runs on a high-risk registration zone TLD variant string "{tld}"',
                })
                break

        for brand, variants in BRAND_SPOOFS.items():
            if any(v in root_lc for v in variants):
                matched_v = next(v for v in variants if v in root_lc)
                findings.append({
                    'type': 'known_spoof', 'severity': 'critical',
                    'char': matched_v, 'looks_like': brand, 'script': 'ASCII', 'context': lc,
                    'message': f'🔴 KNOWN PHISHING STRING: "{lc}" contains unauthorized mutation "{matched_v}" targeted at impersonating "{brand}"',
                })
                break
            else:
                if brand in root_lc:
                    legit = [f"{brand}.com", f"{brand}.net", f"{brand}.org", f"www.{brand}.com", f"{brand}.co.uk", f"{brand}.in"]
                    if not any(lc == d or lc.endswith(f'.{brand}.com') for d in legit):
                        if not any(f.get('context','') == lc and brand in f.get('message','') for f in findings):
                            findings.append({
                                'type': 'brand_in_domain', 'severity': 'high',
                                'char': brand, 'looks_like': f'{brand}.com', 'script': 'Domain',
                                'context': lc,
                                'message': f'⚠️ BRAND IMPERSONATION: Domain "{lc}" includes trademarked phrase "{brand}" but resolves outside verified channels.',
                            })
                    break

    if re.search(r'p@y|@m@z|@pp1e', text, re.I):
        findings.append({
            'type': 'at_trick', 'severity': 'high',
            'char': '@', 'looks_like': 'a', 'script': 'ASCII', 'context': '',
            'message': '🔴 OBFUSCATION ATTEMPT: Symbol "@" injected to mask automated pattern tracking.',
        })

    seen, unique = set(), []
    for f in findings:
        if f['message'] not in seen:
            seen.add(f['message'])
            unique.append(f)
    return unique

def findings_to_warnings(findings):
    return [f['message'] for f in findings]

def _gemini_call(model_name, contents):
    return client.models.generate_content(model=model_name, contents=contents)

def _gemini_error_msg(e):
    err = str(e)
    if '429' in err or 'RESOURCE_EXHAUSTED' in err:
        return "⚠️ Quota threshold reached on current API provisioning configurations."
    elif '403' in err or 'API_KEY_INVALID' in err or 'PERMISSION_DENIED' in err:
        return "⚠️ Gemini Identity Authentication rejected: Key structure invalid or revoked."
    else:
        return f"⚠️ Cloud Endpoint Unreachable. Local mitigation metrics deployed. ({err[:60]})"

# ───────────────────────────────────────────────────────────────────
#  IMAGE ANALYZER BACKEND IMPLEMENTATION
# ───────────────────────────────────────────────────────────────────
def analyze_image_for_phishing(image_b64, mime_type="image/jpeg"):
    prompt = """You are a Level 3 Cybersecurity SOC Analyst with expert vision skills.
Analyze this screenshot/image for ALL phishing indicators:
1. OCR: Extract EVERY piece of text (email body, subject, sender, footer, URLs, buttons)
2. URL/Domain Check: List every URL/domain visible. For each one check lookalike traits.
3. Urgency: "Act Now", "Account Suspended", "Verify Immediately"
4. Visual tricks: fake logos, low-quality copied branding

Respond EXACTLY in this format:
FINAL_VERDICT: [SAFE or PHISHING or SUSPICIOUS]
RISK_SCORE: [0-100]
EXTRACTED_TEXT: [all visible text verbatim]
DETECTED_URLS: [every URL seen, comma-separated, or NONE]
HOMOGLYPH_WARNINGS: [specific character tricks found, or NONE]
URGENCY_PHRASES: [urgent phrases found, or NONE]
EXPLANATION: [2-3 sentences on your verdict]"""

    try:
        response = _gemini_call(
            'gemini-2.5-flash',
            [{"parts": [
                {"inline_data": {"mime_type": mime_type, "data": image_b64}},
                {"text": prompt}
            ]}]
        )
        t = response.text

        def _field(name, content):
            m = re.search(rf'{name}:\s*(.+?)(?=\n[A-Z_]+:|$)', content, re.DOTALL | re.I)
            return m.group(1).strip() if m else ''

        verdict  = _field('FINAL_VERDICT', t).upper()
        risk_raw = _field('RISK_SCORE', t)
        ocr_text = _field('EXTRACTED_TEXT', t)
        urls     = _field('DETECTED_URLS', t)
        hw_raw   = _field('HOMOGLYPH_WARNINGS', t)
        urgency  = _field('URGENCY_PHRASES', t)
        explain  = _field('EXPLANATION', t)

        status = ('phishing'   if 'PHISHING'   in verdict else
                  'suspicious' if 'SUSPICIOUS' in verdict else 'safe')
        try:    risk = int(re.search(r'\d+', risk_raw).group())
        except: risk = {'phishing':80,'suspicious':50,'safe':10}.get(status, 50)

        combined     = (ocr_text or '') + ' ' + (urls or '')
        our_findings = detect_homoglyphs(combined)
        gemini_hw    = [f'🤖 Gemini Vision: {hw_raw}'] if hw_raw and hw_raw.upper() != 'NONE' else []
        all_warnings = gemini_hw + findings_to_warnings(our_findings)

        return {
            'status': status, 'risk_score': risk,
            'extracted_text': ocr_text, 'detected_urls': urls,
            'homoglyph_warnings': all_warnings,
            'urgency_phrases': urgency, 'explanation': explain,
        }
    except Exception as e:
        print(f"GEMINI IMAGE ERROR: {e}")
        return {
            'status': 'error', 'risk_score': 0,
            'extracted_text': '', 'detected_urls': '',
            'homoglyph_warnings': [], 'urgency_phrases': '',
            'explanation': _gemini_error_msg(e),
        }

def check_url_safety(url):
    result = {
        'url': url, 'risk_level': 'safe', 'risk_score': 0,
        'findings': [], 'ssl_valid': None,
        'redirect_chain': [], 'domain': '', 'ip_address': '',
    }
    if not url.startswith('http'):
        url = 'https://' + url
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc or parsed.path.split('/')[0]
    result['domain'] = domain
    lc = domain.replace('www.', '').lower()

    if any(lc == td or lc.endswith('.' + td) for td in TRUSTED_DOMAINS):
        result['findings'].append("✅ Domain confirmed via global trusted authority channels.")
        result['risk_level'] = 'safe'
        return result

    SUSP_KW = ['verify','secure','login','update','confirm','account','banking','signin','password','credential','unlock','suspend','recover','validate','authenticate','urgent','alert','free','winner','prize','claim','reward','refund']
    hits = [k for k in SUSP_KW if k in url.lower()]
    if hits:
        result['risk_score'] += min(len(hits) * 8, 40)
        result['findings'].append(f"🔴 Suspicious keywords detected in endpoint context: {', '.join(hits)}")

    for tld in SUSPICIOUS_TLDS:
        if lc.endswith(tld):
            result['risk_score'] += 30
            result['findings'].append(f"🔴 high-risk registration zone TLD variant string '{tld}' detected.")
            break

    if re.match(r'^\d{1,3}(\.\d{1,3}){3}', domain):
        result['risk_score'] += 40
        result['findings'].append("🔴 Endpoint bypasses DNS translation using raw target IP notation.")

    if len(lc.split('.')) > 4:
        result['risk_score'] += 20
        result['findings'].append("Subdomain levels exceed traditional operational deep-nest configurations.")

    glyph_findings = detect_homoglyphs(url)
    if glyph_findings:
        result['risk_score'] += min(25 * len(glyph_findings), 50)
        result['findings'].extend(findings_to_warnings(glyph_findings))

    try:
        hostname = domain.split(':')[0]
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(2); s.connect((hostname, 443))
            result['ssl_valid'] = True
            result['findings'].append("✅ TLS Handshake validates correctly against host infrastructure.")
    except Exception:
        result['ssl_valid'] = False
        result['findings'].append("⚠️ Encryption Layer verification handshake timed out or failed.")

    score = min(result['risk_score'], 100)
    result['risk_score'] = score
    result['risk_level'] = ('phishing' if score >= 60 else 'suspicious' if score >= 30 else 'safe')
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    email_text = data.get('email', '')
    if not email_text:
        return jsonify({'error': 'No content strings submitted.'})

    result      = phishing_detector(email_text, truncation=True, max_length=512)[0]
    local_score = round(result['score'] * 100, 2)
    gf          = detect_homoglyphs(email_text)
    hw          = findings_to_warnings(gf)

    trusted_sender  = _is_from_trusted_domain(email_text)
    has_safe_ctx    = _has_safe_context(email_text)
    phishing_hits   = _count_phishing_signals(email_text)

    prompt = f"""You are a Level 3 SOC Analyst. Analyze this data.
ALWAYS declare SAFE if transactional from verified bank engines, normal newsletter footprints, standard educational modules.
ONLY flag PHISHING if clear credential harvest hooks, artificial expiration context traps, homoglyphs.
Text: '{email_text}'
Respond EXACTLY in this format:
FINAL_VERDICT: [SAFE or PHISHING]
EXPLANATION: [1 sentence analysis]"""

    try:
        gr     = _gemini_call('gemini-2.5-flash', prompt)
        rt     = gr.text
        status = "safe" if "FINAL_VERDICT: SAFE" in rt.upper() else "phishing"
        try:    explanation = rt.split("EXPLANATION:")[1].strip()
        except: explanation = rt

        if status == "phishing" and trusted_sender and phishing_hits == 0:
            status      = "safe"
            explanation = "Verified alignment configuration confirms signature legitimacy traits."

    except Exception as e:
        print(f"HYBRID ROUTING FAIL: {e}")
        explanation = _gemini_error_msg(e)

        bert_says_malicious = (result['label'] == "LABEL_1" and local_score > 75)

        if hw:
            status = "phishing"
            explanation += " Local Engine Override: Active target homoglyph markers identified in string."
        elif phishing_hits >= 1 and not trusted_sender:
            status = "phishing"
            explanation += " Local Engine Override: High core heuristics threat indicators triggered."
        elif bert_says_malicious and not trusted_sender:
            status = "phishing"
            explanation += " Local Engine Override: High vector weight classification classification matching."
        else:
            status = "safe"

    if hw and status == 'safe' and not trusted_sender:
        status      = 'suspicious'
        explanation += " Lookalike structural notation characters found within processing logs."

    return jsonify({
        'status':             status,
        'confidence':         local_score,
        'explanation':        explanation,
        'homoglyph_warnings': hw,
        'homoglyph_details':  gf,
    })

@app.route('/check-url', methods=['POST'])
def check_url():
    data = request.json or {}
    url  = data.get('url', '').strip()
    if not url:
        return jsonify({'error': 'No URL provided'})

    result = check_url_safety(url)
    try:
        prompt = f"""Cybersecurity expert: is this URL safe to open or is it deceptive/phishing? URL: {url}
Respond EXACTLY in this format:
FINAL_VERDICT: [SAFE or SUSPICIOUS or PHISHING]
EXPLANATION: [1-2 sentences overview]"""
        gr    = _gemini_call('gemini-2.5-flash', prompt)
        gtext = gr.text
        gv = ('phishing'   if 'PHISHING'   in gtext.upper() else
              'suspicious' if 'SUSPICIOUS' in gtext.upper() else 'safe')
        try:    ge = gtext.split("EXPLANATION:")[1].strip()
        except: ge = gtext
    except Exception as e:
        print(f"GEMINI ERROR (check-url): {e}")
        gv = 'error'
        ge = _gemini_error_msg(e)

    result['gemini_verdict']     = gv
    result['gemini_explanation'] = ge
    levels = {'safe': 0, 'suspicious': 1, 'phishing': 2, 'error': 0}
    result['final_verdict'] = max(result['risk_level'], gv, key=lambda x: levels.get(x, 0))
    return jsonify(result)

# ─── REINSTATED ROUTES FOR IMAGE ANALYSIS AND GLYPH ROUTING ───────
@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    if 'image' in request.files:
        f         = request.files['image']
        mime_type = f.content_type or 'image/jpeg'
        image_b64 = base64.b64encode(f.read()).decode('utf-8')
    else:
        data      = request.json or {}
        image_b64 = data.get('image_base64', '')
        mime_type = data.get('mime_type', 'image/jpeg')
        if not image_b64:
            return jsonify({'error': 'No image provided'})
    return jsonify(analyze_image_for_phishing(image_b64, mime_type))

@app.route('/check-homoglyphs', methods=['POST'])
def check_homoglyphs_route():
    image_b64 = None
    mime_type = 'image/jpeg'
    text      = ''

    if request.content_type and 'multipart' in request.content_type:
        text = request.form.get('text', '')
        if 'image' in request.files:
            f         = request.files['image']
            mime_type = f.content_type or 'image/jpeg'
            image_b64 = base64.b64encode(f.read()).decode('utf-8')
    else:
        data      = request.json or {}
        text      = data.get('text', '')
        image_b64 = data.get('image_base64', '')
        mime_type = data.get('mime_type', 'image/jpeg')

    if not text and not image_b64:
        return jsonify({'error': 'Provide text and/or image_base64'})

    all_findings = []
    image_result = None

    if text:
        all_findings.extend(detect_homoglyphs(text))

    if image_b64:
        image_result = analyze_image_for_phishing(image_b64, mime_type)
        for w in (image_result.get('homoglyph_warnings') or []):
            all_findings.append({
                'type': 'image_detected', 'severity': 'high',
                'char': '', 'looks_like': '', 'script': 'Image/OCR',
                'context': '', 'message': w,
            })
        if image_result.get('extracted_text'):
            all_findings.extend(detect_homoglyphs(image_result['extracted_text']))
        if image_result.get('detected_urls'):
            all_findings.extend(detect_homoglyphs(image_result['detected_urls']))

    seen, unique = set(), []
    for f in all_findings:
        m = f.get('message', '')
        if m not in seen:
            seen.add(m); unique.append(f)

    overall = ('phishing'   if any(f.get('severity') == 'critical' for f in unique) else
               'suspicious' if unique else 'safe')

    resp = {
        'text': text, 'warnings': findings_to_warnings(unique),
        'findings': unique, 'is_suspicious': bool(unique),
        'warning_count': len(unique), 'overall_verdict': overall,
    }
    if image_result:
        resp.update({
            'image_ocr_text':      image_result.get('extracted_text', ''),
            'image_detected_urls': image_result.get('detected_urls', ''),
            'image_urgency':       image_result.get('urgency_phrases', ''),
            'image_status':        image_result.get('status', ''),
            'image_risk_score':    image_result.get('risk_score', 0),
            'image_explanation':   image_result.get('explanation', ''),
        })
    return jsonify(resp)

if __name__ == '__main__':
    app.run(debug=True)