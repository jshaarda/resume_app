from django.shortcuts import render
from django.views import generic
from .models import Job, Skill, Project
from django.shortcuts import HttpResponse
from reportlab.platypus.flowables import HRFlowable
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from functools import partial
import sys, copy, os
import reportlab.rl_config
import datetime
import io

DIRNAME = os.path.dirname(__file__)

# Create your views here.
def index(request):
    """View function for home page of site."""
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={},
    )
 
class JobView(generic.ListView):
    """Generic class-based view for the Jobs list."""
    model = Job
    paginate_by = 20
    template_name = 'resume/job_list.html'

class JobDetailView(generic.DetailView):
    """Generic class-based view for the Job detail."""
    model = Job
    template_name = 'resume/job_detail.html'
    
class SkillView(generic.ListView):
    """Generic class-based view for the Jobs list."""
    model = Skill
    template_name = 'resume/skill_list.html'
    
class ProjectView(generic.ListView):
    """Generic class-based view for the Jobs list."""
    model = Project
    template_name = 'resume/project_list.html'

class ProjectDetailView(generic.DetailView):
    """Generic class-based view for the Jobs list."""
    model = Project
    template_name = 'resume/project_detail.html'
        
def print_view(request):
    def header(canvas, doc):
        canvas.saveState()
        content = Paragraph("<b>JIM SHAARDA</b>", styleCentered)
        w, h = content.wrap(doc.width, doc.topMargin)
        content.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
        content = Paragraph("North Royalton, OH 44133 | 440-263-6971 | jshaarda1162@gmail.com", styleCentered)
        w, h = content.wrap(doc.width, doc.topMargin)
        content.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 2 * h)
        canvas.setFont('Times-Roman',9)
        pgnum = canvas.getPageNumber()
        canvas.drawString(4 * inch, 0.5 * inch, "Page %s" % pgnum)
        canvas.restoreState()

    def mainText(L):
        while L:
            E=[]
            while L and L[0]:
                E.append(L.pop(0))
            P.append(E)
            if L:
                while not L[0]: L.pop(0)

    def getLineLength(line):
        ratios ={'a': 60, 'b': 60, 'c': 52, 'd': 60, 'e': 60, 'f': 30, 'g': 60, 'h': 60, 'i': 25, 'j': 25, 'k': 52,'l': 25, 'm': 87, 'n': 60, 'o': 60, 'p': 60, 'q': 60, 'r': 35, 's': 52, 't': 30, 'u': 60, 'v': 52, 'w': 77,'x': 52, 'y': 52, 'z': 52, 'A': 70, 'B': 70, 'C': 77, 'D': 77, 'E': 70, 'F': 65, 'G': 82, 'H': 77, 'I': 30,'J': 55, 'K': 70, 'L': 60, 'M': 87, 'N': 77, 'O': 82, 'P': 70, 'Q': 82, 'R': 77, 'S': 70, 'T': 65, 'U': 77,'V': 70, 'W': 100, 'X': 70, 'Y': 70, 'Z': 65, ',': 25, '(': 25, ')': 25, ' ': 35, '0': 75, '1': 50, '2': 50, '3': 70, '4': 50, '5': 65, '6': 65, '7': 50, '8': 70, '9': 70, '-': 70, '/': 70}
        linelen = 0
        line = line.replace('<b>','')
        line = line.replace('</b>','')
        for i in line:
            v = ratios.get(i, 0)
            v = round(v/100*.125, 5)
            linelen = linelen + v
        return linelen

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    Story = [Spacer(1,0*inch)]
    P = []
    reportlab.rl_config.invariant = 1
    DIRNAME = os.path.dirname(__file__)
    PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
    styles = getSampleStyleSheet()
    styleCentered = ParagraphStyle(name="centeredStyle", alignment=TA_CENTER)
    styleFontsize = ParagraphStyle(name="fontStyle", fontSize=9)
    files = ["part1.txt", "dbjobs", "part2.txt"]
    title1 = Paragraph("<b>JIM SHAARDA</b>", styleCentered)
    title2 = Paragraph("North Royalton, OH 44133 | 440-263-6971 | jshaarda1162@gmail.com", styleCentered)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-0.5*inch, id='normal')
    template1 = PageTemplate(id='header1', frames=frame, onPage=partial(header))
    doc.addPageTemplates([template1])
    Story.append(NextPageTemplate(['header1']))
   
    for fn in files:
        L = []
        if fn == "dbjobs":
            jobs = Job.objects.all().order_by('-start_date')
            now = datetime.datetime.now()
            for job in jobs:
                if int(now.year) - 15 > job.start_date.year:  
                    break 
                sdate = job.start_date.strftime("%m/%Y")
                if job.end_date is None:
                    edate = "Present"
                else:
                    edate = job.end_date.strftime("%m/%Y")
                line = "<b>" + job.name + ", </b>" + job.client + " (" + sdate + " - " + edate + ")"
                ll = getLineLength(line)
                s = round((5 - ll)/0.044)
                if s > 30:
                    s += 5
                q = ll + s*0.044
                while s >= 1:
                    line = line + "&nbsp;"
                    s -= 1
                line = line + job.company
                L.append(line)
                line = job.description
                L.append(line)
                line = "<b>Key Contributions:</b>"
                L.append(line)
                jobcons = job.get_contribution()
                con_list = jobcons.split("| ")
                for con in con_list:
                    line = '    • ' + con
                    L.append(line)
                line = 'blank line'
                L.append(line)
            mainText(L)
        else:
            fin = open(os.path.join(DIRNAME, fn),"r")
            while True:
                line = fin.readline()
                if line == '':
                    break
                else:
                    line = line.replace("\n", "")
                    L.append(line)
        for line in L:
            mainText(L)
    for x in P:
        Story.append(Spacer(1,0.2*inch))
        for line in x:
            if '-------' in line:
                Story.append(HRFlowable(width='100%', thickness=0.5, color=colors.black))
            elif line == '' or line == 'blank line':
                Story.append(Spacer(1,0.2*inch))
            elif '•' in line:
                line = line.replace("•", "")
                Story.append(Paragraph(line, styleFontsize, bulletText='•'))
            else:
                p = Paragraph(line, styleFontsize)
                Story.append(p)
    doc.allowSplitting = not 'nosplitting' in sys.argv
    doc.build(Story, onFirstPage=header, onLaterPages=header)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=resume.pdf'
    response.write(buffer.getvalue())
    buffer.close()
    return response
