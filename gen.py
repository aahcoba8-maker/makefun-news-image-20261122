#!/usr/bin/env python3
"""Deterministic one-page newspaper illustration for 22 November 2026."""
import struct
import zlib

W = H = 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (31, 58, 95)
OCEAN = (220, 230, 238)
LAND = (232, 220, 195)

STORIES = [
(1,'MIDDLE EAST',29.38,47.98,'Iran strikes US air base in Kuwait','Tehran hits Kuwait base, targets Bahrain too.'),
(2,'SOUTH AMERICA',-13.53,-71.97,'Peru quake shakes the Andes','Magnitude 6.9 quake; 152 homes uninhabitable.'),
(3,'N. AMERICA',38.90,-77.04,'Hegseth limits US-Canada defence ties','Pentagon curbs informal military socialising.'),
(4,'N. AMERICA',38.95,-95.25,'BYU outlasts Kansas in triple overtime','No. 10 BYU wins 31-29, playoff hopes alive.'),
(5,'N. AMERICA',33.21,-87.55,'Alabama blanks Chattanooga 47-0','Crimson Tide seal first shutout of the season.'),
(6,'N. AMERICA',40.00,-83.02,'Nebraska upsets No. 14 Ohio State','Huskers win 31-27 in Columbus.'),
(7,'N. AMERICA',41.81,-72.25,'UConn reaches bowl eligibility','Huskies beat Old Dominion 29-21.'),
(8,'N. AMERICA',38.90,-77.04,'FBI crime database breached again','Second breach in days amid system failures.'),
(9,'N. AMERICA',37.77,-122.42,'Anthropic shares fall after IPO','Stock drops a day after record debut.'),
(10,'N. AMERICA',38.90,-77.04,'Trump eyes Democrats on rate cap','Open to a 10% credit-card cap for one year.'),
(11,'SOUTH AMERICA',-13.53,-71.97,'Peru counts quake damage','Revised toll: 152 homes uninhabitable.'),
(12,'EUROPE',59.44,24.75,'Estonia to shut Russia border',"Moscow decries a 'new Iron Curtain'."),
(13,'EUROPE',59.90,24.90,'Drones hit Russian freighter','Strike in the Gulf of Finland, vessel adrift.'),
(14,'EUROPE',36.90,30.71,'COP31 still without a deal','Climate talks in overtime; fossil-fuel row.'),
(15,'EUROPE',36.90,30.71,'Panama threatens to block COP31 deal','Draft drops fossil fuels; Panama objects.'),
(16,'EUROPE',59.91,10.75,'Trafalgar tree leaves Oslo','Christmas tree sets off for London.'),
(17,'EUROPE',5.36,-4.01,'Steinmeier flies to West Africa','German president starts five-day tour.'),
(18,'EUROPE',51.50,-0.12,"UK-EU deal 'won't cut prices'",'Cost-cutting pact, no relief for shoppers.'),
(19,'EUROPE',50.45,30.52,'SBU urges MPs on transparency','Ukraine security service opposes new law.'),
(20,'ASIA',25.61,85.14,'Modi opens Nitish Setu bridge','New bridge links Patna and Vaishali.'),
(21,'ASIA',23.34,85.32,'Cyclone Akvan cancels Ranchi flights','14 flights cancelled as storm nears.'),
(22,'ASIA',28.61,77.21,'Japan to train in India first','Japanese forces use Indian live-fire ranges.'),
(23,'ASIA',19.08,72.88,'Air India extends Jeddah halt','Suspension runs till 24 November.'),
(24,'ASIA',37.57,126.98,'South Korea offers exam bounty','$75,000 for reporting exam cheating.'),
(25,'ASIA',30.90,75.86,'India hockey coach Bhangu dies','Former coach dies aged 86.'),
(26,'ASIA',19.08,72.88,'Sensex ends two-day rally','Profit booking drags Indian markets lower.'),
(27,'ASIA',28.61,77.21,'ICMR signs 20 licences','100 tech transfers at health summit.'),
(28,'ASIA',27.72,85.32,'Nepal PM to meet Modi',"Balendra Shah's first bilateral visit."),
(29,'MIDDLE EAST',26.23,50.59,'Bahrain reports industrial fire','Ministry blames an Iranian strike.'),
(30,'MIDDLE EAST',26.20,56.25,'ADNOC vessel attacked in Hormuz','One crew member missing.'),
(31,'MIDDLE EAST',29.38,47.98,'Crude futures fall over 3%','Oil drops to Rs 7,842 a barrel.'),
(32,'AFRICA',-26.20,28.05,'South Africa local elections','ANC fights to keep control of cities.'),
(33,'AFRICA',13.45,-16.58,'Gambia intercepts 491 migrants','Would-be irregular migrants stopped.'),
(34,'AFRICA',9.06,7.49,'ECOWAS backs women leaders','Regional green-transition programme launches.'),
(35,'AFRICA',32.90,13.19,'Libya fine arts show opens','National exhibition opens in Tripoli.'),
(36,'AFRICA',-4.26,15.29,'Congo summit gathers four presidents','Oyo mini-summit tackles DRC-Kenya rift.'),
(37,'AFRICA',-1.66,29.22,'DR Congo deadline for fighters','UN has a week to fly out 750 South Sudanese.'),
(38,'OCEANIA',-33.87,151.21,'Cummins keeps Test captaincy',"'Unanimous support' from Cricket Australia."),
(39,'OCEANIA',-33.87,151.21,'Australia ends England T20 streak','Hosts win by 3 wickets, 1 ball left.'),
(40,'OCEANIA',-41.29,174.78,'Gill, Pant pass 3,000 WTC runs','First Indians to reach the mark together.'),
(41,'OCEANIA',-41.29,174.78,'India fight back in Wellington',"Rahul's 136 lifts India to 486/4."),
(42,'SPACE',0,0,'SpaceX launches NROL-136','Falcon 9 lifts off; booster lands at LZ-4.'),
]

# The fallback bitmap is intentionally small; PIL is imported only on demand.
FONT5 = {
'A':('01110','10001','10001','11111','10001','10001','10001'),'B':('11110','10001','10001','11110','10001','10001','11110'),
'C':('01111','10000','10000','10000','10000','10000','01111'),'D':('11110','10001','10001','10001','10001','10001','11110'),
'E':('11111','10000','10000','11110','10000','10000','11111'),'F':('11111','10000','10000','11110','10000','10000','10000'),
'G':('01111','10000','10000','10111','10001','10001','01111'),'H':('10001','10001','10001','11111','10001','10001','10001'),
'I':('11111','00100','00100','00100','00100','00100','11111'),'J':('00111','00010','00010','00010','10010','10010','01100'),
'K':('10001','10010','10100','11000','10100','10010','10001'),'L':('10000','10000','10000','10000','10000','10000','11111'),
'M':('10001','11011','10101','10101','10001','10001','10001'),'N':('10001','11001','10101','10011','10001','10001','10001'),
'O':('01110','10001','10001','10001','10001','10001','01110'),'P':('11110','10001','10001','11110','10000','10000','10000'),
'Q':('01110','10001','10001','10001','10101','10010','01101'),'R':('11110','10001','10001','11110','10100','10010','10001'),
'S':('01111','10000','10000','01110','00001','00001','11110'),'T':('11111','00100','00100','00100','00100','00100','00100'),
'U':('10001','10001','10001','10001','10001','10001','01110'),'V':('10001','10001','10001','10001','10001','01010','00100'),
'W':('10001','10001','10001','10101','10101','10101','01010'),'X':('10001','10001','01010','00100','01010','10001','10001'),
'Y':('10001','10001','01010','00100','00100','00100','00100'),'Z':('11111','00001','00010','00100','01000','10000','11111'),
'0':('01110','10001','10011','10101','11001','10001','01110'),'1':('00100','01100','00100','00100','00100','00100','01110'),
'2':('01110','10001','00001','00010','00100','01000','11111'),'3':('11110','00001','00001','01110','00001','00001','11110'),
'4':('00010','00110','01010','10010','11111','00010','00010'),'5':('11111','10000','10000','11110','00001','00001','11110'),
'6':('01110','10000','10000','11110','10001','10001','01110'),'7':('11111','00001','00010','00100','01000','01000','01000'),
'8':('01110','10001','10001','01110','10001','10001','01110'),'9':('01110','10001','10001','01111','00001','00001','01110'),
' ':('00000',)*7,'.':('00000','00000','00000','00000','00000','00110','00110'),',':('00000','00000','00000','00000','00110','00110','00100'),
':':('00000','00110','00110','00000','00110','00110','00000'),';':('00000','00110','00110','00000','00110','00110','00100'),
'-':('00000','00000','00000','11111','00000','00000','00000'),"'":('00100','00100','00000','00000','00000','00000','00000'),
'!':('00100','00100','00100','00100','00100','00000','00100'),'?':('01110','10001','00001','00010','00100','00000','00100'),
'+':('00000','00100','00100','11111','00100','00100','00000'),'/':('00001','00010','00010','00100','01000','01000','10000'),
'%':('11001','11010','00100','01000','10110','00110','00000'),'(':('00010','00100','01000','01000','01000','00100','00010'),
')':('01000','00100','00010','00010','00010','00100','01000'),'$':('00100','01111','10100','01110','00101','11110','00100'),
'&':('01100','10010','10100','01000','10101','10010','01101'),'#':('01010','11111','01010','01010','11111','01010','00000'),
'·':('00000','00000','00100','00100','00100','00000','00000'),'—':('00000','00000','00000','11111','00000','00000','00000'),
}

def pil_page():
    from PIL import Image, ImageDraw, ImageFont
    image = Image.new('RGB', (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    fontdir = '/usr/share/fonts/truetype/dejavu/'
    try:
        regular = lambda size: ImageFont.truetype(fontdir+'DejaVuSans.ttf', size)
        bold = lambda size: ImageFont.truetype(fontdir+'DejaVuSans-Bold.ttf', size)
        regular(12); bold(12)
    except OSError:
        regular = lambda size: ImageFont.load_default()
        bold = regular
    def text(x,y,s,size=12,color=INK,b=False):
        draw.text((int(x),int(y)),s,font=(bold if b else regular)(size),fill=color)
    def rect(box,color): draw.rectangle(tuple(map(int,box)),fill=color)
    def line(points,color,width=1): draw.line(points,fill=color,width=width)
    def circle(x,y,r,color,outline=None,width=1): draw.ellipse((x-r,y-r,x+r,y+r),fill=color,outline=outline,width=width)
    def polygon(points,color): draw.polygon(points,fill=color)
    def measure(s,size,b=False):
        f=(bold if b else regular)(size)
        return draw.textbbox((0,0),s,font=f)[2]
    def wrap(s,maxw,size,b=False):
        words=s.split(); out=[]; cur=''
        for word in words:
            test=(cur+' '+word).strip()
            if cur and measure(test,size,b)>maxw: out.append(cur); cur=word
            else: cur=test
        if cur: out.append(cur)
        return out
    def textfit(x,y,s,maxw,size,minsize=8,b=False,color=INK):
        while size>minsize and measure(s,size,b)>maxw: size-=1
        text(x,y,s,size,color,b)
        return size

    # Masthead
    text((W-measure('THE WORLD IN ONE DAY',52,True))/2,17,'THE WORLD IN ONE DAY',52,b=True)
    text((W-measure('SUNDAY, 22 NOVEMBER 2026',27,True))/2,72,'SUNDAY, 22 NOVEMBER 2026',27,b=True)
    text((W-measure('42 STORIES · 7 REGIONS + SPACE',15))/2,105,'42 STORIES · 7 REGIONS + SPACE',15)
    text(28,30,'42 STORIES',11,b=True); text(877,30,'7 REGIONS + SPACE',11,b=True)
    rect((28,126,996,128),RED)

    # Lead boxes
    for idx, story in enumerate(STORIES[:2]):
        n,region,lat,lon,head,summary=story
        x=28+idx*486; boxw=470
        text(x,137,region,12,RED,True)
        hs=wrap(head,boxw,24,True)
        for j,s in enumerate(hs[:2]): textfit(x,153+j*27,s,boxw,24,19,True)
        yy=153+len(hs[:2])*27
        for j,s in enumerate(wrap(summary,boxw,15)[:2]): text(x,yy+j*18,s,15)
    textfit(28,222,'IN BRIEF — COP31 overtime · Gulf attacks widen · Peru M6.9 quake · NROL-136 lifts off · Anthropic falls',968,13,11)

    # Simplified equirectangular world map.
    rect((28,260,996,428),OCEAN)
    def xy(lon,lat): return (28+(lon+180)*968/360,260+(75-lat)*168/135)
    land_shapes=[
      [(-168,70),(-145,70),(-130,58),(-124,48),(-117,32),(-105,22),(-98,18),(-83,9),(-77,8),(-81,25),(-97,29),(-105,45),(-122,50),(-130,60),(-150,62)],
      [(-81,12),(-70,10),(-50,-2),(-45,-15),(-52,-30),(-68,-55),(-76,-42),(-80,-10)],
      [(-10,72),(25,70),(45,60),(35,50),(25,42),(10,36),(-5,42),(-10,55)],
      [(-17,35),(5,37),(32,30),(42,12),(35,-5),(20,-35),(5,-34),(-5,-15),(-15,5)],
      [(30,70),(60,72),(90,70),(120,65),(150,60),(170,50),(155,42),(135,35),(120,20),(105,5),(80,8),(60,25),(45,35),(35,50)],
      [(112,-11),(130,-10),(150,-18),(153,-25),(145,-39),(128,-35),(115,-25)],
      [(45,-13),(50,-15),(49,-25),(45,-24)],
      [(-180,-65),(180,-65),(180,-75),(-180,-75)],
    ]
    # Correct Australia outline separately (kept as numeric polygon coordinates).
    land_shapes[5]=[(112,-11),(130,-10),(150,-18),(153,-25),(145,-39),(128,-35),(115,-25)]
    for shp in land_shapes: polygon([xy(lon,lat) for lon,lat in shp],LAND)
    # Pin collision placement: process stories in order, down then right, bounded to 32 px.
    placed=[]
    for n,region,lat,lon,head,summary in STORIES[:41]:
        tx,ty=xy(lon,lat); px,py=tx,ty
        collides=lambda x,y: any((x-ox)**2+(y-oy)**2<14**2 for ox,oy,_ in placed)
        shifts=0
        if collides(px,py):
            qx,qy=px,py+16
            if 28<=qx<=996 and 260<=qy<=428 and (qx-tx)**2+(qy-ty)**2<=32**2:
                px,py=qx,qy; shifts+=1
        if collides(px,py) and shifts<2:
            qx,qy=px+16,py
            if 28<=qx<=996 and 260<=qy<=428 and (qx-tx)**2+(qy-ty)**2<=32**2:
                px,py=qx,qy; shifts+=1
        placed.append((px,py,n))
        circle(px,py,11,RED,'white',2)
        label=str(n); tw=measure(label,10,True)
        text(px-tw/2,py-7,label,10,(255,255,255),True)

    # Three compact columns, fixed item pitch and explicit story ranges.
    starts=[3,17,30]; ends=[16,29,42]; colw=312; top=442; pitch=36
    for c,(start,end) in enumerate(zip(starts,ends)):
        x=28+c*328
        for i in range(start,end+1):
            n,region,lat,lon,head,summary=STORIES[i-1]
            y=top+(i-start)*pitch
            text(x,y,str(n),14,RED,True)
            rx=x+24
            tag=region
            tagw=measure(tag,9,True)
            text(rx,y+1,tag,7,NAVY,True)
            hx=rx+measure(tag,7,True)+4; avail=x+colw-hx
            lines=wrap(head,avail,10,True)
            for j,s in enumerate(lines[:2]): textfit(hx,y+j*11,s,avail,10,8,True)
            # Fixed 36 px pitch: two headline lines plus one summary line.
            textfit(rx,y+24,summary,colw-24,9,7,False)
        if c<2: rect((28+(c+1)*328-8,442,29+(c+1)*328-8,948), (190,184,168))

    # Footer and markets line.
    rect((28,952,996,953),RED)
    textfit(28,956,'Sources: Reuters · AP · BBC · Al Jazeera · Bloomberg · The Guardian · ESPNcricinfo — every story first reported on 22 November 2026.',968,11,8)
    textfit(28,978,"MARKETS — Friday's close · S&P 500 -3.7% · Nasdaq -5.28% · NIFTY 50 +1.12% · DAX -2.60% · FTSE 100 -1.02% · Gold -4.62% · Bitcoin +2.35% · EUR/USD 1.0990",968,11,8,True)
    image.save('/output/entry.png',format='PNG',optimize=False,compress_level=9)

def fallback_page():
    # Pure stdlib raster backend; BMP glyphs are rendered uppercase and 5 by 7.
    from array import array
    pixels=bytearray(bytes(PAPER)*W*H)
    def put(x,y,color):
        x=int(x); y=int(y)
        if 0<=x<W and 0<=y<H:
            k=(y*W+x)*3; pixels[k:k+3]=bytes(color)
    def rect(box,color):
        x0,y0,x1,y1=map(int,box)
        for y in range(max(0,y0),min(H,y1+1)):
            a=(y*W+max(0,x0))*3; b=(y*W+min(W,x1+1))*3
            if a<b: pixels[a:b]=bytes(color)*((b-a)//3)
    def circle(x,y,r,color,outline=None,width=1):
        x=int(x); y=int(y); r=int(r)
        for yy in range(y-r,y+r+1):
            for xx in range(x-r,x+r+1):
                d=(xx-x)**2+(yy-y)**2
                if d<=r*r and (outline is None or d>=(r-width)**2): put(xx,yy,color if outline is None or d>=(r-width)**2 else outline)
        if outline:
            for yy in range(y-r,y+r+1):
                for xx in range(x-r,x+r+1):
                    d=(xx-x)**2+(yy-y)**2
                    if d<=r*r and d>=(r-width)**2: put(xx,yy,outline)
    def polygon(points,color):
        pts=[(int(x),int(y)) for x,y in points]
        if not pts:return
        lo=max(0,min(y for x,y in pts)); hi=min(H-1,max(y for x,y in pts))
        for y in range(lo,hi+1):
            xs=[]
            for (x1,y1),(x2,y2) in zip(pts,pts[1:]+pts[:1]):
                if y1==y2: continue
                if min(y1,y2)<=y<max(y1,y2): xs.append(int(x1+(y-y1)*(x2-x1)/(y2-y1)))
            xs.sort()
            for a,b in zip(xs[::2],xs[1::2]):
                for x in range(max(0,a),min(W,b+1)): put(x,y,color)
    def line(points,color,width=1):
        for (x0,y0),(x1,y1) in zip(points,points[1:]):
            dx=abs(int(x1)-int(x0)); dy=abs(int(y1)-int(y0)); sx=1 if x0<x1 else -1; sy=1 if y0<y1 else -1; err=dx-dy
            x=int(x0); y=int(y0)
            while True:
                rect((x-width//2,y-width//2,x+width//2,y+width//2),color)
                if x==int(x1) and y==int(y1): break
                e=2*err
                if e>-dy: err-=dy; x+=sx
                if e<dx: err+=dx; y+=sy
    def text(x,y,s,size=12,color=INK,b=False):
        # The fallback font has fixed cell metrics; size controls integer scale.
        scale=max(1,int(size/8)); xx=int(x); yy=int(y)
        for ch in s.upper():
            glyph=FONT5.get(ch,FONT5[' '])
            for gy,row in enumerate(glyph):
                for gx,on in enumerate(row):
                    if on=='1': rect((xx+gx*scale,yy+gy*scale,xx+(gx+1)*scale-1,yy+(gy+1)*scale-1),color)
            xx+=6*scale
    def measure(s,size,b=False): return len(s)*6*max(1,int(size/8))
    def wrap(s,maxw,size,b=False):
        words=s.split(); out=[]; cur=''
        for word in words:
            test=(cur+' '+word).strip()
            if cur and measure(test,size,b)>maxw: out.append(cur); cur=word
            else: cur=test
        if cur: out.append(cur)
        return out
    def textfit(x,y,s,maxw,size,minsize=8,b=False,color=INK):
        while size>minsize and measure(s,size,b)>maxw:size-=1
        text(x,y,s,size,color,b); return size
    draw_page(text,rect,circle,polygon,line,wrap,measure,textfit)
    raw=bytearray()
    stride=W*3
    for y in range(H): raw.append(0); raw.extend(pixels[y*stride:(y+1)*stride])
    import struct,zlib
    def chunk(tag,data): return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>2I5B',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(bytes(raw),9))+chunk(b'IEND',b'')
    with open('/output/entry.png','wb') as f:f.write(png)
def draw_page(text,rect,circle,polygon,line,wrap,measure,textfit):
    # Layout shared by the fallback renderer; bitmap text uses uppercase glyphs.
    text(285,24,'THE WORLD IN ONE DAY',48,INK,True)
    text(356,80,'SUNDAY, 22 NOVEMBER 2026',24,INK,True)
    text(389,116,'42 STORIES · 7 REGIONS + SPACE',12)
    text(28,30,'42 STORIES',10,INK,True); text(870,30,'7 REGIONS + SPACE',10,INK,True)
    rect((28,126,996,128),RED)
    for idx,st in enumerate(STORIES[:2]):
        n,reg,lat,lon,head,summ=st; x=28+idx*486
        text(x,138,reg,10,RED,True)
        for j,s in enumerate(wrap(head,470,20,True)[:2]): text(x,158+j*24,s,20,INK,True)
        for j,s in enumerate(wrap(summ,470,12)[:2]): text(x,208+j*15,s,12)
    textfit(28,224,'IN BRIEF — COP31 overtime · Gulf attacks widen · Peru M6.9 quake · NROL-136 lifts off · Anthropic falls',968,10,8)
    rect((28,260,996,428),OCEAN)
    def xy(lon,lat):return (28+(lon+180)*968/360,260+(75-lat)*168/135)
    shapes=[[(-168,70),(-130,58),(-122,45),(-105,22),(-80,8),(-78,25),(-100,30),(-125,50)], [(-81,12),(-50,-2),(-45,-15),(-68,-55),(-80,-10)], [(-10,70),(35,65),(45,50),(25,40),(-10,45)], [(-17,35),(35,30),(42,12),(20,-35),(5,-34),(-15,5)], [(30,70),(80,72),(125,65),(170,50),(135,20),(100,5),(60,25)], [(112,-11),(150,-18),(145,-39),(115,-25)]]
    for shp in shapes: polygon([xy(lon,lat) for lon,lat in shp],LAND)
    placed=[]
    for n,reg,lat,lon,head,summ in STORIES[:41]:
        x,y=xy(lon,lat)
        for step in range(3):
            if all((x-a)**2+(y-b)**2>=14**2 for a,b in placed):break
            if step%2==0:y+=16
            else:x+=16
        x=max(39,min(985,x));y=max(271,min(417,y));placed.append((x,y))
        circle(x,y,11,RED,(255,255,255),2);textfit(x-7,y-5,str(n),14,9,8,True,(255,255,255))
    starts=[3,17,30]; ends=[16,29,42]
    for c,(start,end) in enumerate(zip(starts,ends)):
        x=28+c*328
        for i in range(start,end+1):
            n,reg,lat,lon,head,summ=STORIES[i-1]; y=442+(i-start)*36
            text(x,y,str(n),12,RED,True); text(x+24,y+1,reg,7,NAVY,True)
            hx=x+24+measure(reg,7,True)+4; avail=x+312-hx
            for j,s in enumerate(wrap(head,avail,11,True)[:2]):textfit(hx,y+j*13,s,avail,11,8,True)
            textfit(x+24,y+23,summ,288,8,7)
        if c<2:rect((28+(c+1)*328-8,442,29+(c+1)*328-8,948),(190,184,168))
    rect((28,952,996,953),RED)
    textfit(28,957,'Sources: Reuters · AP · BBC · Al Jazeera · Bloomberg · The Guardian · ESPNcricinfo — every story first reported on 22 November 2026.',968,8,7)
    textfit(28,980,"MARKETS — Friday's close · S&P 500 -3.7% · Nasdaq -5.28% · NIFTY 50 +1.12% · DAX -2.60% · FTSE 100 -1.02% · Gold -4.62% · Bitcoin +2.35% · EUR/USD 1.0990",968,8,7,True)

def main():
    try:
        import PIL  # noqa: F401
    except ImportError:
        fallback_page()
    else:
        pil_page()

if __name__=='__main__':
    main()
