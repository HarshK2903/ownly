import subprocess,json,sys,pathlib,hashlib
root=pathlib.Path('/home/bugulnoz/research/ownly')
out=root/'analysis/hermes/mcp';out.mkdir(exist_ok=True)
p=subprocess.Popen([str(root/'tools/hermes/hermes-mcp')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
counter=0
def rpc(method,params):
 global counter
 counter+=1;p.stdin.write(json.dumps(dict(jsonrpc='2.0',id=counter,method=method,params=params))+'\n');p.stdin.flush()
 while True:
  line=p.stdout.readline()
  if not line: raise RuntimeError('MCP stopped')
  r=json.loads(line)
  if r.get('id')==counter:return r
def call(name,args):
 key=name+'-'+hashlib.sha256(json.dumps(args,sort_keys=True).encode()).hexdigest()[:12]
 path=out/(key+'.json')
 if path.exists(): r=json.loads(path.read_text())
 else:
  r=rpc('tools/call',{'name':name,'arguments':args});path.write_text(json.dumps({'tool':name,'arguments':args,'response':r},indent=2));r=json.loads(path.read_text())
 content=r['response'].get('result',{}).get('content',[])
 text='\n'.join(x.get('text','') for x in content)
 (out/(key+'.txt')).write_text(text)
 print(json.dumps({'tool':name,'args':args,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'text':text[:int(__import__('os').environ.get('PREVIEW','18000'))]}),flush=True)
try:
 rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'ownly-research','version':'1'}})
 rpc('tools/call',{'name':'load_file','arguments':{'path':str(root/'analysis/hermes/ownly.hbc')}})
 for item in json.loads(sys.argv[1]):call(item[0],item[1])
finally:
 p.terminate();p.wait()
