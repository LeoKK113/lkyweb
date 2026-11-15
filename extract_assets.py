from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import zipfile,xml.etree.ElementTree as E,io,json,posixpath
root=Path(__file__).resolve().parent
source=root.parent/'个人简历资料'
out=root/'public/assets';out.mkdir(parents=True,exist_ok=True)
z=zipfile.ZipFile(source/'李敏个人项目集.pptx')
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
allpages={}
for i in range(3,83):
 if i in [34,62,78]:continue
 rel=E.fromstring(z.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
 mapping={x.attrib['Id']:posixpath.normpath('ppt/slides/'+x.attrib['Target']) for x in rel}
 slide=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
 imgs=[]
 for b in slide.findall('.//a:blip',ns):
  path=mapping.get(b.attrib.get('{'+ns['r']+'}embed'))
  if not path:continue
  try:
   im=Image.open(io.BytesIO(z.read(path))).convert('RGB')
   if im.width<450 or im.height<250:continue
   imgs.append(im)
  except Exception:pass
 imgs.sort(key=lambda im:im.width*im.height,reverse=True)
 names=[]
 for k,im in enumerate(imgs[:3]):
  im.thumbnail((1920,1400));name=f'p{i:02}-{k}.webp';im.save(out/name,quality=86);names.append('/assets/'+name)
 allpages[i]=names
Image.open(source/'个人头像.png').convert('RGB').resize((800,1000)).save(out/'portrait.webp',quality=90)
(root/'asset-map.json').write_text(json.dumps(allpages),encoding='utf-8')
thumbs=[]
for i in [4,11,14,18,22,27,30,36,40,45,49,54,58,64,70,75,79,80,81,82]:
 if allpages.get(i):
  im=Image.open(root/'public'/allpages[i][0].lstrip('/'));im=ImageOps.fit(im,(256,154));ImageDraw.Draw(im).text((8,8),str(i),fill='red');thumbs.append(im)
sheet=Image.new('RGB',(1024,((len(thumbs)+3)//4)*154))
for k,im in enumerate(thumbs):sheet.paste(im,((k%4)*256,(k//4)*154))
sheet.save(root/'contact-sheet.jpg')
print('Extracted',sum(map(len,allpages.values())),'project images')
