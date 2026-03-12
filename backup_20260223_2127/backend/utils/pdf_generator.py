import io
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class PremiumPDFGenerator:
    RASI_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    def __init__(self, report_data: dict, filename: str = "Prasna_Report.pdf"):
        self.data = report_data
        self.filename = filename
        self.brand_color_main = colors.HexColor("#0D1B2A") # Deep Navy
        self.brand_color_accent = colors.HexColor("#C29731") # Gold
        self.bg_light = colors.HexColor("#F8F9FA")

    def _draw_border(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(self.brand_color_accent)
        canvas.setLineWidth(2)
        canvas.rect(0.5*inch, 0.5*inch, A4[0]-1*inch, A4[1]-1*inch)
        canvas.restoreState()

    def _create_chart(self):
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
        ax.set_xlim(0, 4); ax.set_ylim(0, 4)
        ax.axis('off')

        # Thicker grid lines for visibility
        for i in range(5):
            ax.plot([i, i], [0, 4], color='#0D1B2A', lw=2.5)
            ax.plot([0, 4], [i, i], color='#0D1B2A', lw=2.5)

        house_coords = {12: (0, 3), 1: (1, 3), 2: (2, 3), 3: (3, 3), 11: (0, 2), 4: (3, 2), 10: (0, 1), 5: (3, 1), 9: (0, 0), 8: (1, 0), 7: (2, 0), 6: (3, 0)}
        positions = self.data.get('positions', {})
        planets_in_houses = {} # {house: [(name, color)]}
        
        for p, h in positions.items():
            if h not in planets_in_houses: planets_in_houses[h] = []
            abbr = p[:2].upper()
            color = 'black'
            
            if "Jama" in p: 
                abbr = "J" + p.split()[-1][:1].upper()
                color = '#B8860B' # Dark Gold for better contrast
            elif p in ["Udayam", "Arudam", "Kavippu"]: 
                abbr = p[:2].upper()
                color = '#CC0000' # Bright Red
            else:
                color = '#006B3C' # Darker Green for better readability
                
            planets_in_houses[h].append((abbr, color))

        for h, (x, y) in house_coords.items():
            p_list = planets_in_houses.get(h, [])
            row_y = y + 0.55
            x_offset = 0.1
            for i, (abbr, color) in enumerate(p_list):
                ax.text(x + x_offset, row_y, abbr, color=color, ha='left', va='center', fontsize=12, fontweight='bold')
                x_offset += 0.3
                if x_offset > 0.85:
                    x_offset = 0.1
                    row_y -= 0.25
                    
            # House number - top right corner, prominent
            ax.text(x + 0.85, y + 0.88, str(h), color='#555555', fontsize=10, fontweight='bold', ha='right', va='top')
            if h == self.data.get('block'):
                ax.add_patch(plt.Rectangle((x, y), 1, 1, color='#FFFACD', alpha=0.3))

        now = datetime.now().strftime("%d.%m.%Y - %H:%M")
        ax.text(2, 2, f"{now}\nRuling: {self.data.get('ruling_planet', '')}", color='#0D1B2A', ha='center', va='center', fontsize=10, fontweight='bold', fontstyle='italic')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0); plt.close()
        return buf

    def _clean_text(self, text):
        """Removes non-ASCII and non-printable characters to avoid black blocks in PDF."""
        if not text: return "N/A"
        return "".join([i if (32 <= ord(i) < 127) else "" for i in str(text)])

    def _make_table(self, data, col_widths, header=True):
        t = Table(data, colWidths=col_widths)
        style = [
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]
        if header:
            style.extend([
                ('BACKGROUND', (0,0), (-1,0), self.brand_color_main),
                ('TEXTCOLOR', (0,0), (-1,0), self.brand_color_accent),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ])
        t.setStyle(TableStyle(style))
        return t

    def generate(self):
        doc = SimpleDocTemplate(self.filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('Title', fontSize=22, textColor=self.brand_color_main, alignment=TA_CENTER, spaceAfter=20, fontName='Helvetica-Bold')
        header_style = ParagraphStyle('Header', fontSize=14, textColor=self.brand_color_accent, spaceBefore=12, spaceAfter=8, fontName='Helvetica-Bold')
        point_style = ParagraphStyle('Point', fontSize=9, leading=13, spaceBefore=4)
        
        story = []
        story.append(Paragraph("JAMAKKAL PRASNA PROFESSIONAL REPORT", title_style))
        
        # User Data & Query
        user_info = f"Name: {self.data.get('name', 'N/A')} | Gender: {self.data.get('gender', 'N/A')}"
        story.append(Paragraph(user_info, ParagraphStyle('User', fontSize=10, textColor=self.brand_color_main, alignment=TA_CENTER)))
        
        if self.data.get('query_text'):
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("QUERY RAISED:", ParagraphStyle('QL', fontSize=9, textColor=self.brand_color_accent, fontName='Helvetica-Bold')))
            story.append(Paragraph(f'"{self.data.get("query_text")}"', ParagraphStyle('QT', fontSize=11, fontName='Helvetica-Oblique', leftIndent=20, textColor=colors.grey)))
            story.append(Spacer(1, 0.2*inch))

        # 1. PANCHANGA TABLE
        story.append(Paragraph("Panchanga & Chart Settings", header_style))
        p = self.data.get('panchanga', {})
        p_data = [
            ["Attribute", "Value", "Attribute", "Value"],
            ["Date/Time", self.data.get('query_time_str', 'N/A'), "Sunrise", self.data.get('sunrise_str', 'N/A')],
            ["Ayanamsa", p.get('Ayanamsa', 'N/A'), "Sidereal Time", p.get('SiderealTime', 'N/A')],
            ["Tithi", p.get('Tithi', 'N/A'), "Nakshatra", p.get('Nakshatra', 'N/A')],
            ["Yoga", p.get('Yoga', 'N/A'), "Hora", p.get('Hora', 'N/A')]
        ]
        story.append(self._make_table(p_data, [1.2*inch, 1.5*inch, 1.2*inch, 1.5*inch]))
        
        # 2. TRANSITS TABLE
        story.append(Paragraph("Planetary Positions (Transits)", header_style))
        t_header = ["Body", "Rasi", "Degree", "Nakshatra (Pada)", "Star Lord"]
        t_data = [t_header]
        transits = self.data.get('transits', {})
        for name, info in transits.items():
            t_data.append([name, info['rasi'], info['degree'], f"{info['nakshatra']} ({info['pada']})", info['star_lord']])
        story.append(self._make_table(t_data, [1*inch, 1*inch, 1.2*inch, 1.5*inch, 1*inch]))

        # 3. CHART & INNER/OUTER
        story.append(PageBreak())
        story.append(Paragraph("Jamakkal Chart & Jama Grahas", header_style))
        img = Image(self._create_chart(), width=5*inch, height=5*inch)
        story.append(img)
        
        # Current Transit Positions Table (outside chart for clarity)
        transits = self.data.get('transits', {})
        if transits:
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("Current Transit Positions", ParagraphStyle('TransitH', fontSize=11, fontName='Helvetica-Bold', textColor=self.brand_color_accent, spaceBefore=6)))
            transit_table = [["Planet", "Rasi", "Degree", "Nakshatra", "Status", "Fruition"]]
            for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                t = transits.get(p_name, {})
                if t:
                    transit_table.append([
                        p_name,
                        t.get("rasi", ""),
                        t.get("degree", ""),
                        t.get("nakshatra", ""),
                        t.get("status", t.get("star_status", "")),
                        t.get("fruition", "-")
                    ])
            if len(transit_table) > 1:
                story.append(self._make_table(transit_table, [0.7*inch, 0.9*inch, 0.8*inch, 1.2*inch, 0.9*inch, 0.7*inch]))
        # Jama Grahas (Outer)
        story.append(Paragraph("Jamakkol Outer Planets", header_style))
        jama_data = [["Planet", "House", "Planet", "House"]]
        jg = list(self.data.get('jama_grahas', {}).items())
        for i in range(0, len(jg), 2):
            row = [jg[i][0], str(jg[i][1])]
            if i+1 < len(jg): row.extend([jg[i+1][0], str(jg[i+1][1])])
            else: row.extend(["", ""])
            jama_data.append(row)
        story.append(self._make_table(jama_data, [1.3*inch, 1*inch, 1.3*inch, 1*inch]))

        # NATAL CHART SECTION (if available)
        if 'natal' in self.data and self.data['natal']:
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("NATIVE BIRTH CHART", header_style))
            
            natal = self.data['natal']
            b_date = natal.get('birth_date', 'N/A')
            b_time = natal.get('birth_time', 'N/A')
            story.append(Paragraph(f"Birth Date/Time: {b_date} at {b_time}", ParagraphStyle('Sub', fontSize=9)))
            story.append(Paragraph(f"Birth Place: {self._clean_text(natal.get('birth_place', 'N/A'))}", ParagraphStyle('Sub', fontSize=9)))
            story.append(Paragraph(f"Lagna: {natal.get('Lagna', 'N/A')}", ParagraphStyle('Sub', fontSize=10, fontName='Helvetica-Bold', textColor=self.brand_color_accent)))
            
            # Planetary Positions Table
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("Planetary Positions (Birth Chart)", ParagraphStyle('SubH', fontSize=10, fontName='Helvetica-Bold')))
            
            natal_data = [["Planet", "Sign", "Degree", "Nakshatra", "Status"]]
            planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Ascendant"]
            
            for p in planets:
                if p in natal.get('Positions', {}):
                    pos = natal['Positions'][p]
                    state = natal.get('PlanetaryStates', {}).get(p, "")
                    natal_data.append([
                        p,
                        self.RASI_NAMES[pos - 1] if isinstance(pos, int) and 1 <= pos <= 12 else str(pos),
                        natal.get('Degrees', {}).get(p, "-"),
                        natal.get('Nakshatras', {}).get(p, "-"),
                        self._clean_text(state)
                    ])
            
            story.append(self._make_table(natal_data, [1*inch, 1.2*inch, 1.1*inch, 1.2*inch, 1.2*inch]))


        # 4. DEEP ANALYSIS (3 Sections)
        story.append(PageBreak())
        for title_base, key in [("I. DIAGNOSTIC ANALYSIS", "diagnostic_analysis"), 
                          ("II. RECOVERY TIMELINE", "recovery_timeline"), 
                          ("III. REMEDIES & GUIDANCE", "remedies")]:
            pts = self.data.get(key, [])
            story.append(Paragraph(f"{title_base} ({len(pts)} Unique Points)", header_style))
            for i, pt in enumerate(pts, 1):
                story.append(Paragraph(f"• {pt}", point_style))

        # 4.5 DETAILED SYNTHESIS ANALYSIS
        story.append(PageBreak())
        has_natal = bool(self.data.get('natal') and self.data['natal'].get('Lagna'))
        synth_mode = "Horary + Birth Chart Logic" if has_natal else "Horary Logic"
        story.append(Paragraph(f"V. DETAILED SYNTHESIS ANALYSIS ({synth_mode})", header_style))
        s_points = self.data.get('synthesis_points', [])
        for pt in s_points:
            story.append(Paragraph(f"• {pt}", point_style))
        
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Synthesis Conclusion:", ParagraphStyle('SubSub', fontSize=11, fontName='Helvetica-Bold', spaceBefore=8, textColor=self.brand_color_accent)))
        story.append(Paragraph(
            self.data.get('synthesis_conclusion', ""),
            ParagraphStyle('SynthC', fontSize=10, fontName='Helvetica', textColor=self.brand_color_main,
                          leftIndent=10, leading=14, spaceBefore=4)
        ))

        # Holistic Categories (Category-wise list)
        story.append(Spacer(1, 0.4*inch))
        story.append(Paragraph("VI. HOLISTIC CATEGORY ANALYSIS", header_style))
        
        cat_title_style = ParagraphStyle('CatTitle', fontSize=12, textColor=self.brand_color_main, fontName='Helvetica-Bold', spaceBefore=10)
        cat_score_style = ParagraphStyle('CatScore', fontSize=10, textColor=self.brand_color_accent, fontName='Helvetica-Bold')
        challenge_style = ParagraphStyle('Chall', fontSize=9, textColor=colors.HexColor("#A83232"), leftIndent=15)
        sol_style = ParagraphStyle('Sol', fontSize=9, textColor=colors.HexColor("#107B4F"), leftIndent=15)

        for cat, data in self.data.get('balance_categories', {}).items():
            story.append(Paragraph(cat, cat_title_style))
            story.append(Paragraph(f"Score: {data.get('score', 0):.1f} / 10 - {data.get('status', '')}", cat_score_style))
            
            story.append(Paragraph("Challenges:", ParagraphStyle('Sub', fontSize=9, fontName='Helvetica-Bold', spaceBefore=4)))
            for chal in data.get('challenges', []):
                story.append(Paragraph(f"• {chal}", challenge_style))
                
            story.append(Paragraph("Pariharam / Recommendations:", ParagraphStyle('Sub', fontSize=9, fontName='Helvetica-Bold', spaceBefore=4)))
            for sol in data.get('solutions', []):
                story.append(Paragraph(f"• {sol}", sol_style))
            
            story.append(Spacer(1, 0.1*inch))

        story.append(PageBreak())
        story.append(Paragraph("FINAL CONCLUSION", header_style))
        story.append(Paragraph(self.data.get('final_conclusion', ""), ParagraphStyle('Final', fontSize=10, fontName='Helvetica', leading=14)))

        # Disclaimer section
        story.append(PageBreak())
        story.append(Paragraph("DISCLAMATORY REMARKS", header_style))
        disclaimer_text = (
            "This astrology report is generated based on the ancient principles of Jamakkal Prasna and sidereal calculations. "
            "Astrology provides insights into probable trends and tendencies; it is not a substitute for professional legal, medical, or financial advice. "
            "The interpretations provided here are meant for spiritual guidance and self-reflection. "
            "The author/developer is not responsible for any decisions made based on this report. "
            "Please use your individual discretion and logic before taking major life actions."
        )
        story.append(Paragraph(disclaimer_text, ParagraphStyle('Disc', fontSize=9, fontName='Helvetica-Oblique', textColor=colors.grey, spaceBefore=10, leading=12)))

        # Footer
        story.append(Spacer(1, 1*inch))
        story.append(Paragraph("Prepared by : RAJAGOPAL KANNAN", ParagraphStyle('F1', fontSize=9, alignment=TA_CENTER, textColor=colors.grey, fontName='Helvetica-Bold')))
        story.append(Paragraph("WhatsApp consultation : 9841033514", ParagraphStyle('F2', fontSize=9, alignment=TA_CENTER, textColor=colors.grey, fontName='Helvetica-Bold')))
        
        doc.build(story, onFirstPage=self._draw_border, onLaterPages=self._draw_border)
        return self.filename
