"""Render slide-ready, original illustrations of the plugin's actual architecture."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1] / "visuals"
ROOT.mkdir(exist_ok=True)
S = 2
FONTS = Path(__file__).resolve().parent / "fonts"
# Mona Sans matches the PowerPoint theme; Hubot Sans (OFL) is its GitHub companion for labels.
FONT = "/Library/Fonts/MonaSans-Regular.ttf"
DISPLAY = "/Library/Fonts/MonaSansDisplay-Bold.ttf"
BOLD = str(FONTS / "HubotSans-Bold.ttf")
MONO = str(FONTS / "HubotSans-SemiBold.ttf")
THEMES = {
    "dark": dict(bg="#090E0C", ink="#F6FFF9", muted="#A1B6AA", surface="#14251D",
                 green="#8BF1A6", line="#3C6350", soft="#1E3A2B"),
    "light": dict(bg="#FFFFFF", ink="#09241A", muted="#52695B", surface="#F0F7F2",
                  green="#0D6836", line="#86AF95", soft="#D8F1E0"),
}


class Canvas:
    def __init__(self, theme):
        self.t = THEMES[theme]
        self.image = Image.new("RGB", (2560, 1440), self.t["bg"])
        self.d = ImageDraw.Draw(self.image)

    def line(self, points, color=None, width=2):
        self.d.line([(x*S, y*S) for x, y in points], fill=color or self.t["line"],
                    width=round(width*S), joint="curve")

    def rect(self, box, fill, radius=20, outline=None):
        self.d.rounded_rectangle(tuple(v*S for v in box), radius=radius*S,
                                 fill=fill, outline=outline, width=2*S)

    def circle(self, x, y, r, fill=None, outline=None, width=2):
        self.d.ellipse(((x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S),
                       fill=fill, outline=outline, width=round(width*S))

    def text(self, x, y, text, size=18, color=None, bold=False, mono=False, center=False, display=False):
        font = ImageFont.truetype(DISPLAY if display else MONO if mono else BOLD if bold else FONT, size*S)
        bbox = self.d.textbbox((0, 0), text, font=font)
        w = (bbox[2]-bbox[0])/S
        if center:
            x -= w/2
        assert x >= 24 and x+w <= 1256, (text, x, w)
        assert y >= 0 and y+(bbox[3]-bbox[1])/S < 720, text
        self.d.text((x*S, y*S), text, font=font, fill=color or self.t["ink"])

    def arrow(self, points, color=None, width=2):
        color = color or self.t["green"]
        self.line(points, color, width)
        x, y = points[-1]
        px, py = points[-2]
        a = math.atan2(y-py, x-px)
        self.d.polygon([(x*S, y*S),
                        ((x-10*math.cos(a-.5))*S, (y-10*math.sin(a-.5))*S),
                        ((x-10*math.cos(a+.5))*S, (y-10*math.sin(a+.5))*S)], fill=color)

    def icon(self, kind, x, y, r=23, color=None):
        g = color or self.t["green"]
        if kind == "outline":
            self.circle(x, y, r, outline=g)
            self.line([(x-r, y), (x+r, y)], g)
            self.line([(x, y-r), (x, y+r)], g)
            self.d.polygon([(x*S, (y-r*.7)*S), ((x+r*.35)*S, (y+r*.35)*S),
                            ((x-r*.35)*S, (y+r*.35)*S)], outline=g, width=2*S)
        elif kind == "build":
            p = [(x,y-r), (x+r,y-r/2), (x+r,y+r/2), (x,y+r),
                 (x-r,y+r/2), (x-r,y-r/2), (x,y-r)]
            self.line(p, g, 2.5)
            self.line([(x-r,y-r/2), (x,y), (x+r,y-r/2)], g, 2.5)
            self.line([(x,y), (x,y+r)], g, 2.5)
        elif kind == "review":
            self.circle(x-4, y-4, r*.72, outline=g, width=3)
            self.line([(x+r*.4,y+r*.4), (x+r,y+r)], g, 4)
            self.line([(x-r*.45,y-4), (x-r*.1,y+3), (x+r*.25,y-10)], g, 2.5)
        elif kind == "publish":
            self.line([(x-12,y+12), (x-12,y-8), (x,y-r), (x+12,y-8),
                       (x+12,y+12), (x-12,y+12)], g, 2.5)
            self.circle(x,y-7,4,outline=g)
            self.line([(x-5,y+17), (x-5,y+r+7)], g, 2)
            self.line([(x+5,y+17), (x+5,y+r+3)], g, 2)
            self.line([(x-12,y+3), (x-21,y+15), (x-12,y+12)], g)
            self.line([(x+12,y+3), (x+21,y+15), (x+12,y+12)], g)
        elif kind == "orchestrate":
            self.line([(x-r,y), (x,y), (x+r,y-r*.7)], g, 3)
            self.line([(x,y), (x+r,y+r*.7)], g, 3)
            for xx, yy in [(x-r,y), (x,y), (x+r,y-r*.7), (x+r,y+r*.7)]:
                self.circle(xx,yy,5,fill=self.t["surface"],outline=g)
        elif kind == "agent":
            self.rect((x-r*1.3,y-r*.8,x+r*1.3,y+r),self.t["surface"],12, g)
            self.line([(x,y-r*.8), (x,y-r*1.3)], g, 2.5)
            self.circle(x,y-r*1.4,3,fill=g)
            for xx in (x-r*.55,x+r*.55):
                self.circle(xx,y,4,fill=g)
            self.line([(x-r*.4,y+r*.5), (x+r*.4,y+r*.5)], g)
        elif kind == "human":
            self.circle(x,y-10,8,outline=g, width=2.5)
            self.d.arc(((x-18)*S,(y+1)*S,(x+18)*S,(y+30)*S),180,360,fill=g,width=3*S)
        elif kind == "approver":
            # Closed head-and-shoulders bust, scaled by r and optically centered.
            self.circle(x,y-r*.42,r*.36,fill=g)
            self.d.chord(((x-r*.78)*S,(y+r*.08)*S,(x+r*.78)*S,(y+r*1.38)*S),180,360,fill=g)

    def header(self, title, subtitle):
        self.text(64, 42, "GH / SKILLS BUILDER", 13, self.t["green"], mono=True)
        self.text(64,82,title,44,bold=True,display=True)
        self.text(66,141,subtitle,19,self.t["muted"])

    def footer(self, text):
        self.text(64,675,text,13,self.t["muted"],mono=True)

    def save(self, name, theme):
        path = ROOT / f"{name}-{theme}.png"
        self.image.save(path)
        return path


def architecture(theme):
    c = Canvas(theme); t = c.t
    c.header("One agent. Five skills.", "One coordinator loads the capability needed for each stage.")
    # Registration pattern echoes the official template's halftone language.
    for x in range(560,730,12):
        for y in range(195,425,12):
            if (x-645)**2+(y-310)**2 < 98**2:
                c.circle(x,y,.9,fill=t["line"])
    c.line([(640,300),(640,243)],t["green"],3)
    c.line([(640,395),(640,400)],t["green"],3)
    c.line([(640,438),(640,454)],t["green"],3)
    c.line([(200,454),(1080,454)],t["green"],3)
    for x in (200,490,790,1080):
        c.line([(x,454),(x,480)],t["green"],3)
        c.circle(x,454,4,fill=t["green"])
    c.rect((466,188,814,244),t["surface"],18)
    c.icon("orchestrate",502,216,14)
    c.text(646,204,"Orchestration skill",20,bold=True,center=True)
    c.circle(640,332,63,fill=t["surface"],outline=t["green"],width=2.5)
    c.icon("agent",640,321,25)
    c.text(640,361,"AGENT",12,t["green"],mono=True,center=True)
    c.text(640,407,"@github-skills-orchestrator",18,bold=True,center=True)
    for x,title,kind,desc in [(200,"Outline","outline","Define the journey"),
                              (490,"Bootstrap","build","Build the exercise"),
                              (790,"Review","review","Report the findings"),
                              (1080,"Publish","publish","Prepare the release")]:
        c.rect((x-118,480,x+118,624),t["surface"])
        c.icon(kind,x,517,20)
        c.text(x,553,title,25,bold=True,center=True)
        c.text(x,589,desc,16,t["muted"],center=True)
    c.footer("AGENT SKILLS ARE AUTOMATED WORKFLOWS / CAPABILITIES FOR AN AGENT — NOT FIVE SEPARATE AGENTS")
    return c.save("01-agent-skill-map",theme)


def lifecycle(theme):
    c=Canvas(theme); t=c.t
    c.header("From idea to exercise.","The skills do the work. People decide when to advance.")
    xs=[190,490,790,1090]
    for a,b in zip(xs,xs[1:]):
        c.arrow([(a+87,348),(b-87,348)],width=3)
        c.circle((a+b)/2,348,36,fill=t["soft"],outline=t["green"],width=2.5)
        c.icon("approver",(a+b)/2,348,24)
    for i,(x,title,kind,result,gate) in enumerate(zip(xs,
        ["Outline","Bootstrap","Review","Publish"],
        ["outline","build","review","publish"],
        ["Learner journey","Repository + checks","Findings + fix plan","Release + handoff"],
        ["Outline approved","Build satisfactory","Review signed off","Publish authorized"])):
        c.circle(x,348,81,fill=t["surface"],outline=t["line"])
        c.icon(kind,x,341,32)
        c.text(x,225,f"0{i+1}",17,t["green"],mono=True,center=True)
        c.text(x,459,title,29,bold=True,center=True)
        c.text(x,501,result,17,t["muted"],center=True)
        c.rect((x-115,553,x+115,605),t["soft"],14)
        c.text(x,569,gate,16,t["green"],bold=True,center=True)
    c.rect((450,180,830,214),t["surface"],12)
    c.text(640,188,"ORCHESTRATOR MAINTAINS THE SEQUENCE",12,t["green"],mono=True,center=True)
    c.footer("FOUR PHASES / EXPLICIT APPROVAL AT EVERY GATE / NO AUTO-PUBLISH")
    return c.save("02-approval-gated-lifecycle",theme)


def feedback(theme):
    c=Canvas(theme); t=c.t
    c.header("Feedback is a circuit.","Report first. Apply approved fixes. Re-review before release.")
    # A deliberately interrupted return path distinguishes approval from automation.
    c.arrow([(282,386),(498,386)],width=3)
    c.arrow([(750,386),(966,386)],width=3)
    c.arrow([(1127,385),(1160,385),(1160,560),(735,560)],width=3)
    c.arrow([(545,560),(130,560),(130,385),(153,385)],width=3)
    for x,title,kind,sub in [(220,"Build round","build","Bootstrap skill"),
                              (625,"Review round","review","Review skill"),
                              (1060,"Human decision","human","Approve fixes or sign off")]:
        c.circle(x,385,67,fill=t["surface"],outline=t["line"])
        c.icon(kind,x,380,29)
        c.text(x,272,title,21,bold=True,center=True)
        c.text(x,468,sub,16,t["muted"],center=True)
    c.rect((309,362,426,410),t["bg"],10)
    c.text(367,365,"Build",14,t["green"],bold=True,center=True)
    c.text(367,386,"approved",14,t["green"],center=True)
    c.rect((798,362,923,410),t["bg"],10)
    c.text(860,365,"Report only",14,t["green"],bold=True,center=True)
    c.text(860,386,"No edits",14,t["green"],center=True)
    c.rect((545,533,735,588),t["soft"],16)
    c.text(640,548,"APPROVED FIXES",15,t["green"],mono=True,center=True)
    c.arrow([(1160,385),(1160,223),(1175,223)],width=3)
    c.text(1060,186,"Sign-off + publish authorization",14,t["muted"],center=True)
    c.icon("publish",1200,220,17)
    c.text(625,621,"Every new build and review round needs a user check-in.",19,center=True)
    c.footer("SAME FINDING AFTER TWO FIX ROUNDS? STOP AND ESCALATE.")
    return c.save("03-review-fix-circuit",theme)


if __name__ == "__main__":
    paths=[]
    for fn in (architecture,lifecycle,feedback):
        for theme in THEMES:
            paths.append(fn(theme))
    thumbs=Image.new("RGB",(1280,1080),"#D3DDD6")
    for i,p in enumerate(paths):
        with Image.open(p) as im:
            thumbs.paste(im.resize((640,360),Image.Resampling.LANCZOS),
                         ((i%2)*640,(i//2)*360))
    thumbs.save(ROOT/"visual-contact-sheet.png")
    for p in paths:
        print(p)
