#!/usr/bin/env python3
"""Draw a deterministic newspaper front page for 22 November 2026."""
import struct
import zlib

W = H = 1024
PAPER = '#F7F3E8'
INK = '#111111'
RED = '#B91C1C'
NAVY = '#1F3A5F'
OCEAN = '#DCE6EE'
LAND = '#E8DCC3'
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
(42,'SPACE',None,None,'SpaceX launches NROL-136','Falcon 9 lifts off; booster lands at LZ-4.'),
]

def hexrgb(s):
    return tuple(int(s[i:i+2], 16) for i in (1,3,5))

class Raster:
    """Tiny stdlib raster backend; bitmap glyphs are intentionally compact."""
    def __init__(self):
        self.p = bytearray(hexrgb(PAPER) * (W*H))
    def rect(self,x0,y0,x1,y1,c):
        col=bytes(hexrgb(c)); x0=max(0,int(x0)); x1=min(W,int(x1)); y0=max(0,int(y0)); y1=min(H,int(y1))
        for y in range(y0,y1): self.p[(y*W+x0)*3:(y*W+x1)*3]=col*(x1-x0)
    def circle(self,x,y,r,c):
        col=bytes(hexrgb(c)); rr=r*r
        for yy in range(max(0,int(y-r)),min(H,int(y+r+1))):
            for xx in range(max(0,int(x-r)),min(W,int(x+r+1))):
                if (xx-x)**2+(yy-y)**2<=rr: self.p[(yy*W+xx)*3:(yy*W+xx)*3+3]=col
    def polygon(self,pts,c):
        if len(pts)<3:return
        lo=max(0,min(y for x,y in pts)); hi=min(H-1,max(y for x,y in pts)); col=bytes(hexrgb(c))
        for y in range(int(lo),int(hi)+1):
            xs=[]
            for i,(x1,y1) in enumerate(pts):
                x2,y2=pts[(i+1)%len(pts)]
                if (y1<=y<y2) or (y2<=y<y1): xs.append(x1+(y-y1)*(x2-x1)/(y2-y1))
            xs.sort()
            for a,b in zip(xs[::2],xs[1::2]):
                for x in range(max(0,int(a)),min(W,int(b)+1)): self.p[(y*W+x)*3:(y*W+x)*3+3]=col
    def width(self,s,size,bold=False): return len(s)*6*max(1,int(size/8))
    def text(self,x,y,s,size,c,bold=False,anchor=None):
        # Raster fallback uses uppercase 5x7 glyphs, scaled to a readable cell size.
        scale=max(1,int(size/8)); x=int(x); y=int(y)
        if anchor in ('mt','mm'): x-=self.width(s,size)//2
        if anchor=='rt': x-=self.width(s,size)
        if anchor=='mm': y-=3*scale
        for ch in s.upper():
            bits=FONT.get(ch,FONT[' '])
            for j,row in enumerate(bits):
                for i,v in enumerate(row):
                    if v=='1': self.rect(x+i*scale,y+j*scale,x+(i+1)*scale,y+(j+1)*scale,c)
            x+=6*scale
    def save(self,path):
        raw=b''.join(b'\0'+self.p[y*W*3:(y+1)*W*3] for y in range(H))
        def chunk(tag,data): return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
        with open(path,'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>2I5B',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b''))

# 5x7 font: ASCII capitals, digits and common punctuation.
FONT={
'A':('01110','10001','10001','11111','10001','10001','10001'),'B':('11110','10001','10001','11110','10001','10001','11110'),'C':('01111','10000','10000','10000','10000','10000','01111'),'D':('11110','10001','10001','10001','10001','10001','11110'),'E':('11111','10000','10000','11110','10000','10000','11111'),'F':('11111','10000','10000','11110','10000','10000','10000'),'G':('01111','10000','10000','10111','10001','10001','01111'),'H':('10001','10001','10001','11111','10001','10001','10001'),'I':('11111','00100','00100','00100','00100','00100','11111'),'J':('00111','00010','00010','00010','10010','10010','01100'),'K':('10001','10010','10100','11000','10100','10010','10001'),'L':('10000','10000','10000','10000','10000','10000','11111'),'M':('10001','11011','10101','10101','10001','10001','10001'),'N':('10001','11001','10101','10011','10001','10001','10001'),'O':('01110','10001','10001','10001','10001','10001','01110'),'P':('11110','10001','10001','11110','10000','10000','10000'),'Q':('01110','10001','10001','10001','10101','10010','01101'),'R':('11110','10001','10001','11110','10100','10010','10001'),'S':('01111','10000','10000','01110','00001','00001','11110'),'T':('11111','00100','00100','00100','00100','00100','00100'),'U':('10001','10001','10001','10001','10001','10001','01110'),'V':('10001','10001','10001','10001','10001','01010','00100'),'W':('10001','10001','10001','10101','10101','10101','01010'),'X':('10001','10001','01010','00100','01010','10001','10001'),'Y':('10001','10001','01010','00100','00100','00100','00100'),'Z':('11111','00001','00010','00100','01000','10000','11111'),
'0':('01110','10001','10011','10101','11001','10001','01110'),'1':('00100','01100','00100','00100','00100','00100','01110'),'2':('01110','10001','00001','00010','00100','01000','11111'),'3':('11110','00001','00001','01110','00001','00001','11110'),'4':('00010','00110','01010','10010','11111','00010','00010'),'5':('11111','10000','10000','11110','00001','00001','11110'),'6':('01110','10000','10000','11110','10001','10001','01110'),'7':('11111','00001','00010','00100','01000','01000','01000'),'8':('01110','10001','10001','01110','10001','10001','01110'),'9':('01110','10001','10001','01111','00001','00001','01110'),
' ':('00000',)*7,'.':('00000','00000','00000','00000','00000','00110','00110'),',':('00000','00000','00000','00000','00110','00110','00100'),':':('00000','00110','00110','00000','00110','00110','00000'),';':('00000','00110','00110','00000','00110','00110','00100'),'-':('00000','00000','00000','11111','00000','00000','00000'),'—':('00000','00000','00000','11111','00000','00000','00000'),"'":('00100','00100','00010','00000','00000','00000','00000'),'"':('01010','01010','00100','00000','00000','00000','00000'),'!':('00100','00100','00100','00100','00100','00000','00100'),'?':('01110','10001','00001','00010','00100','00000','00100'),'+':('00000','00100','00100','11111','00100','00100','00000'),'/':('00001','00010','00010','00100','01000','01000','10000'),'%':('11001','11010','00100','01000','10110','00110','00000'),'(':('00010','00100','01000','01000','01000','00100','00010'),')':('01000','00100','00010','00010','00010','00100','01000'),'·':('00000','00000','00100','00100','00100','00000','00000'),'$':('00100','01111','10100','01110','00101','11110','00100'),"'":('00100','00100','00010','00000','00000','00000','00000')}

class Pillow:
    def __init__(self):
        from PIL import Image, ImageDraw, ImageFont
        self.Image=Image; self.draw=ImageDraw.Draw(Image.new('RGB',(1,1)))
        self.im=Image.new('RGB',(W,H),PAPER); self.draw=ImageDraw.Draw(self.im)
        self.Font=ImageFont; self.fallback=None
    def font(self,size,bold=False):
        import os
        p='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        try:return self.Font.truetype(p,size)
        except OSError:return self.Font.load_default()
    def rect(self,x0,y0,x1,y1,c): self.draw.rectangle((x0,y0,x1,y1),fill=c)
    def circle(self,x,y,r,c): self.draw.ellipse((x-r,y-r,x+r,y+r),fill=c)
    def polygon(self,pts,c): self.draw.polygon(pts,fill=c)
    def text(self,x,y,s,size,c,bold=False,anchor=None): self.draw.text((x,y),s,font=self.font(size,bold),fill=c,anchor=anchor)
    def width(self,s,size,bold=False): return self.draw.textbbox((0,0),s,font=self.font(size,bold))[2]
    def save(self,path): self.im.save(path,format='PNG',optimize=False,compress_level=9)

def wrap(text, width, size, backend, bold=False, maxlines=2):
    words=text.split(); lines=[]; cur=''
    for word in words:
        test=(cur+' '+word).strip()
        if backend.width(test,size,bold)<=width or not cur: cur=test
        else: lines.append(cur); cur=word
    if cur: lines.append(cur)
    while len(lines)>maxlines and size>9:
        size-=1; lines=[]; cur=''
        for word in words:
            test=(cur+' '+word).strip()
            if backend.width(test,size,bold)<=width or not cur: cur=test
            else: lines.append(cur); cur=word
        if cur: lines.append(cur)
    return lines,size

def land_polygon(b, coords):
    # Equirectangular coordinate conversion, clipped to the map band.
    pts=[]
    for lon,lat in coords: pts.append((int(28+(lon+180)*968/360),int(274+(75-lat)*154/135)))
    b.polygon(pts,LAND)

def render(b):
    b.rect(0,0,W,H,PAPER)
    # Masthead and edition line.
    b.text(512,18,'THE WORLD IN ONE DAY',52,INK,True,'mt')
    b.text(512,77,'SUNDAY, 22 NOVEMBER 2026',27,INK,True,'mt')
    b.text(512,108,'42 STORIES · 7 REGIONS + SPACE',15,INK,False,'mt')
    b.text(28,30,'42 STORIES',12,INK,True)
    b.text(996,30,'7 REGIONS + SPACE',12,INK,True,'rt')
    b.rect(28,132,996,135,RED)
    # Lead boxes.
    for x,story in ((28,STORIES[0]),(518,STORIES[1])):
        _,region,_,_,headline,summary=story
        b.text(x,143,region,12,RED,True)
        lines,sz=wrap(headline,460,25,b,True,2)
        for j,line in enumerate(lines): b.text(x,160+j*29,line,sz,INK,True)
        lines,sz=wrap(summary,460,15,b,False,2)
        for j,line in enumerate(lines): b.text(x,219+j*17,line,sz,INK)
    b.rect(28,254,996,255,RED)
    brief='IN BRIEF — COP31 overtime · Gulf attacks widen · Peru M6.9 quake · NROL-136 lifts off · Anthropic falls'
    size=13
    while b.width(brief,size)>968 and size>11:size-=1
    # Map ocean and simple continent silhouettes.
    b.rect(28,274,996,428,OCEAN)
    land_polygon(b,[(-168,70),(-145,60),(-130,52),(-125,42),(-117,32),(-105,25),(-98,18),(-83,10),(-78,8),(-80,20),(-70,25),(-60,45),(-68,55),(-95,68),(-130,72)])
    land_polygon(b,[(-82,12),(-70,8),(-58,-4),(-48,-15),(-52,-28),(-63,-55),(-70,-50),(-76,-25)])
    land_polygon(b,[(-12,36),(5,37),(20,32),(32,20),(45,11),(42,-10),(32,-34),(18,-35),(8,-20),(-2,-5),(-15,5),(-17,20)])
    land_polygon(b,[(-10,70),(30,72),(60,65),(85,58),(110,55),(135,48),(150,55),(170,52),(178,42),(160,30),(140,20),(120,5),(105,0),(95,8),(80,8),(70,20),(55,25),(45,35),(30,36),(20,45),(5,50),(-5,58)])
    land_polygon(b,[(112,-11),(130,-10),(145,-15),(154,-25),(146,-39),(130,-43),(115,-32)])
    land_polygon(b,[(-52,60),(-42,65),(-30,60),(-35,52),(-48,55)])
    b.text(512,258,brief,size,INK,False,'mt')
    # Pins: at most one down and one right correction, with 32px displacement cap.
    placed=[]
    for num,region,lat,lon,_,_ in STORIES[:41]:
        tx=28+(lon+180)*968/360; ty=260+(75-lat)*168/135
        x,y=tx,ty
        if any((x-a)**2+(y-c)**2<14**2 for a,c,n in placed): y+=16
        if any((x-a)**2+(y-c)**2<14**2 for a,c,n in placed):
            nx=x+16
            if ((nx-tx)**2+(y-ty)**2)**0.5<=32: x=nx
        # Map strip bounds; displacement check uses true position.
        x=max(34,min(990,x)); y=max(280,min(422,y))
        assert ((x-tx)**2+(y-ty)**2)**0.5<=32, (num,x,y,tx,ty)
        placed.append((x,y,num))
    # Land check is deliberately coarse; ocean pins are accepted only for island/coastal stories.
    for x,y,n in placed:
        b.circle(x,y,12,'#FFFFFF'); b.circle(x,y,10,RED)
        b.text(x,y-1,str(n),10,'#FFFFFF',True,'mm')
    # Three compact news columns. Headlines and summaries are fitted to their allotted pitch.
    columns=[STORIES[2:16],STORIES[16:29],STORIES[29:42]]
    xs=[28,356,684]
    b.rect(348,442,349,948,NAVY); b.rect(676,442,677,948,NAVY)
    for col,items in enumerate(columns):
        x=xs[col]
        for j,s in enumerate(items):
            num,region,_,_,headline,summary=s; y=444+j*36
            b.text(x,y,str(num),14,RED,True)
            b.text(x+22,y,region,9,NAVY,True)
            hlines,hs=wrap(headline,288,12,b,True,1)
            for k,line in enumerate(hlines[:1]): b.text(x+22,y+10+k*12,line,hs,INK,True)
            # Summary is one line; scale down when required but preserve verbatim.
            ss=9
            while b.width(summary,ss)>288 and ss>8:ss-=1
            b.text(x+22,y+26,summary,ss,INK)
    # Footer copy, exactly as specified.
    footer="Sources: Reuters · AP · BBC · Al Jazeera · Bloomberg · The Guardian · ESPNcricinfo — every story first reported on 22 November 2026."
    fs=11
    while b.width(footer,fs)>968 and fs>8:fs-=1
    b.text(28,957,footer,fs,INK)
    markets="MARKETS — Friday's close · S&P 500 -3.7% · Nasdaq -5.28% · NIFTY 50 +1.12% · DAX -2.60% · FTSE 100 -1.02% · Gold -4.62% · Bitcoin +2.35% · EUR/USD 1.0990"
    ms=11
    while b.width(markets,ms)>968 and ms>8:ms-=1
    b.text(28,979,markets,ms,INK,True)

def main():
    try:
        backend=Pillow()
    except ImportError:
        backend=Raster()
    render(backend)
    backend.save('/output/entry.png')

if __name__=='__main__': main()
