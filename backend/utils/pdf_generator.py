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
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
        # Use a larger range to allow for outer labels
        ax.set_xlim(-0.7, 4.7)
        ax.set_ylim(-0.7, 4.7)
        ax.axis('off')

        # Colors from branding
        navy = "#0D1B2A"
        gold = "#C29731"
        red = "#CC0000"
        green = "#006B3C"
        blue = "#003366"
        grey = "#AAAAAA"

        # 1. Draw the main 4x4 grid
        for i in range(5):
            ax.plot([i, i], [0, 4], color=navy, lw=2)
            ax.plot([0, 4], [i, i], color=navy, lw=2)

        # 2. Draw outer border frame
        ax.plot([-0.05, 4.05, 4.05, -0.05, -0.05], [-0.05, -0.05, 4.05, 4.05, -0.05], color=navy, lw=1.5)

        # Rasi coordinate mapping (Absolute: 1=Ari, 12=Pis)
        r_coords = {
            12: (0, 3), 1: (1, 3), 2: (2, 3), 3: (3, 3),
            11: (0, 2),                          4: (3, 2),
            10: (0, 1),                          5: (3, 1),
            9: (0, 0),  8: (1, 0), 7: (2, 0),  6: (3, 0)
        }
        
        # Rasi Names (Abbr)
        r_names = {
            12: "Pis", 1: "Ari", 2: "Tau", 3: "Gem",
            11: "Aqu",                          4: "Can",
            10: "Cap",                          5: "Leo",
            9: "Sag",  8: "Sco", 7: "Lib",  6: "Vir"
        }

        # Data extraction
        jama_grahas = self.data.get('jama_grahas', {})
        inner = self.data.get('inner_planets', {})
        udayam_rasi = inner.get('Udayam', {}).get('rasi_num', 0)
        
        # Mapping for relative house numbers from Udayam
        def get_rel_house(r_num):
            if not udayam_rasi: return None
            return (r_num - udayam_rasi + 12) % 12 + 1

        # 3. Fill Rasi Blocks
        for r_num, (x, y) in r_coords.items():
            # Rasi Name (top left)
            ax.text(x + 0.05, y + 0.95, r_names[r_num], color='#BBBBBB', fontsize=9, ha='left', va='top')
            
            # Rasi Number (bottom right) - Match Website Ref (Rasi Num 1-12)
            ax.text(x + 0.95, y + 0.05, str(r_num), color=gold, fontsize=10, fontweight='bold', ha='right', va='bottom')

            # Internal Planets (Transit + Inner)
            planets_here = []
            
            # Inner Points (Udayam, Arudam, Kavippu)
            for point, p_data in inner.items():
                if p_data.get('rasi_num') == r_num:
                    if point == 'Udayam': planets_here.append(('UD', red, 12))
                    elif point == 'Arudam': planets_here.append(('AR', red, 12))
                    elif point == 'Kavippu': planets_here.append(('(KV)', red, 12))

            # Transits
            transits = self.data.get('transits', {})
            for p_name, p_data in transits.items():
                if p_data.get('rasi_num') == r_num:
                    if p_name == "Ascendant":
                        planets_here.append(('ASC', blue, 12))
                    elif p_name in ["Rahu", "Ketu"]:
                        planets_here.append((f'({p_name[:2].upper()})', green, 11))
                    else:
                        planets_here.append((p_name[:2].upper(), green, 11))

            # Render planets in box
            row_y = y + 0.7
            x_pos = x + 0.3
            for i, (txt, col, sz) in enumerate(planets_here):
                ax.text(x_pos, row_y, txt, color=col, fontsize=sz, fontweight='bold', ha='center', va='center')
                x_pos += 0.4
                if x_pos > x + 0.8:
                    x_pos = x + 0.3
                    row_y -= 0.25

        # 4. Draw Jama Grahas (Outer Markers)
        # Anti-clockwise flow: Top (←), Right (↓), Bottom (→), Left (↑)
        p_name_map = {"Sun": "SN", "Moon": "MO", "Mars": "MA", "Mercury": "ME", "Jupiter": "JU", "Venus": "VE", "Saturn": "SA", "Snake": "SU"}
        
        for p_key, p_data in jama_grahas.items():
            if not isinstance(p_data, dict): continue
            
            p_orig = p_key.replace("Jama ", "")
            p_abbr = p_name_map.get(p_orig, p_orig[:2].upper())
            abbr = f"J.{p_abbr}"
            r_num = p_data.get('rasi_num')
            deg_str = p_data.get('abs_degree_fmt', '')
            label = f"{abbr} {deg_str}"
            
            if r_num in r_coords:
                x, y = r_coords[r_num]
                # Determine placement side and arrows
                if y == 3: # Top row: Flow ←
                    lx, ly = x + 0.5, 4.3
                    ax.text(lx, ly, f"← {label}", color=blue, fontsize=9, ha='center', va='center')
                elif x == 3 and y < 3: # Right side: Flow ↑ (using → rotated 90)
                    lx, ly = 4.3, y + 0.5
                    ax.text(lx, ly, f"{label} →", color=blue, fontsize=9, ha='left', va='center', rotation=90)
                elif y == 0: # Bottom row: Flow →
                    lx, ly = x + 0.5, -0.3
                    ax.text(lx, ly, f"{label} →", color=blue, fontsize=9, ha='center', va='center')
                elif x == 0 and y > 0: # Left side: Flow ↓ (using ← rotated 90)
                    lx, ly = -0.3, y + 0.5
                    ax.text(lx, ly, f"← {label}", color=blue, fontsize=9, ha='right', va='center', rotation=90)

        # 5. Central Metadata Box (Middle 2x2 area)
        ax.add_patch(plt.Rectangle((1, 1), 2, 2, facecolor='#FFFFFF', edgecolor=blue, lw=1.5, zorder=5))
        
        # Branding / Title in Center
        q_time_raw = self.data.get('query_time_str', datetime.now().strftime("%Y-%m-%d %H:%M"))
        jamam_num = self.data.get('block', 1)
        # Weekday from query time
        try:
            wd_name = datetime.strptime(q_time_raw, "%Y-%m-%d %H:%M:%S").strftime("%A")
        except:
            wd_name = ""
            
        lat = self.data.get('lat')
        lon = self.data.get('lon')
        lat_str = f"{lat}" if lat and lat != 0 else "12.97"
        lon_str = f"{lon}" if lon and lon != 0 else "77.59"
        
        prasna_loc = self.data.get('location') or "Unknown"
        birth_loc = self.data.get('birth_place')
        
        header_text = (
            f"JAMAKKOL HORARY, {wd_name} Jamam #{jamam_num}\n"
            f"{wd_name}, {q_time_raw} (UTC+05:30)\n"
            f"Prasna Location: {prasna_loc}\n"
        )
        if birth_loc and birth_loc != "N/A" and birth_loc != prasna_loc:
            header_text += f"Native Birth Place: {birth_loc}\n"
            
        header_text += f"{lat_str} / {lon_str}"
        
        ax.text(2, 2.9, header_text, color=blue, fontsize=8, ha='center', va='top', fontweight='bold', zorder=10)

        # 5.1 Two-column Degree Table in Center
        # Mapped to exact order and labels from reference image
        # Complete Planetary Table in Center (Ordered to match Photo 2)
        left_col = [
            ("ASC", "Ascendant"), ("MO", "Moon"), ("UD", "Udayam"), 
            ("md", "Mandhi"), ("JU", "Jupiter"), ("KE", "Ketu"), ("KV", "Kavippu")
        ]
        right_col = [
            ("AR", "Arudam"), ("MA", "Mars"), ("SU", "Sun"), 
            ("RA", "Rahu"), ("VE", "Venus"), ("ME", "Mercury"), ("SA", "Saturn")
        ]
        
        def get_fmt_deg(p_name):
            d_data = transits.get(p_name) or inner.get(p_name)
            if not d_data: return "000° 00' 00\""
            
            deg = d_data.get("abs_deg", 0)
            d = int(deg)
            m = int((deg % 1) * 60)
            s = int(((deg * 60) % 1) * 60)
            return f"{d:03d}° {m:02d}' {s:02d}\""

        table_y = 2.15
        for i in range(len(left_col)):
            l_abbr, l_full = left_col[i]
            r_abbr, r_full = right_col[i]
            
            l_deg = get_fmt_deg(l_full)
            r_deg = get_fmt_deg(r_full)
            
            # Row string with fixed-width spacing
            # Use smaller fontsize to ensure fit
            row_str = f"{l_abbr:<4} {l_deg}   {r_abbr:<4} {r_deg}"
            ax.text(2, table_y, row_str, color=blue, fontsize=7.5, family='monospace', ha='center', va='top', zorder=10, fontweight='bold')
            table_y -= 0.13

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

    def generate_competition_report(self):
        doc = SimpleDocTemplate(self.filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        # Custom styles for dark theme
        title_style = ParagraphStyle('Title', fontSize=20, leading=26, textColor=colors.HexColor("#D1B2FF"), fontName='Helvetica-Bold')
        prep_style = ParagraphStyle('Prep', fontSize=9, textColor=colors.white, alignment=TA_LEFT)
        prep_gold = ParagraphStyle('PrepGold', fontSize=9, textColor=colors.HexColor("#FFCC00"), alignment=TA_LEFT, fontName="Helvetica-Bold")
        
        story = []
        cd = self.data.get('cricket_data', {})
        team_a = cd.get('team_a', 'Team A')
        team_b = cd.get('team_b', 'Team B')

        def _build_page(is_noray):
            page_story = []
            
            box_style = ParagraphStyle('BoxText', fontSize=10, textColor=colors.white, spaceAfter=8, leading=14)
            box_q = ParagraphStyle('BoxQ', fontSize=11, textColor=colors.HexColor("#FFCC00"), fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)
            logic_style = ParagraphStyle('BoxLogic', fontSize=9, textColor=colors.HexColor("#AAAAAA"), fontName='Helvetica-Oblique', leading=12)
            
            # Title Suffix
            suffix = "<br/><font size=12 color='#AAAAAA'>(Without Planetary Rays Considered)</font>" if is_noray else "<br/><font size=12 color='#AAAAAA'>(With Planetary Rays Considered)</font>"
            header_data = [
                [Paragraph(f"<b>Sports Match Prediction Report</b>{suffix}", title_style), 
                 Paragraph("<font color='#FFCC00'>Prepared by:</font> RAJAGOPAL KANNAN<br/><font color='#FFCC00'>WhatsApp:</font> +91 98410 33514", ParagraphStyle('Prep', textColor=colors.white, alignment=2, fontSize=10))],
                [Paragraph("<i>This report is for informational purposes based on astrological readings.</i>", ParagraphStyle('Info', textColor=colors.HexColor("#AAAAAA"), alignment=TA_CENTER, fontSize=9)), ""]
            ]
            
            t_header = Table(header_data, colWidths=[4.6*inch, 2.7*inch])
            t_header.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1A1A1D")),
                ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#8C52FF")),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('SPAN', (0,1), (1,1)),
                ('LINEBELOW', (0,0), (1,0), 1, colors.HexColor("#8C52FF")),
                ('TOPPADDING', (0,0), (-1,-1), 12),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                ('LEFTPADDING', (0,0), (-1,-1), 12),
                ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ]))
            page_story.append(t_header)
            page_story.append(Spacer(1, 0.4*inch))
            
            # 2. Main Title - Final Prediction
            page_story.append(Paragraph("Predicted Match Winner", ParagraphStyle('MainWin', fontSize=18, textColor=colors.HexColor("#FFCC00"), alignment=TA_CENTER, fontName='Helvetica-Bold')))
            page_story.append(Spacer(1, 0.15*inch))
            winner_txt = cd.get('predicted_winner', 'Unknown')
            page_story.append(Paragraph(f"{winner_txt}", ParagraphStyle('MainWinBig', fontSize=26, textColor=colors.white, alignment=TA_CENTER, fontName='Helvetica-Bold')))
            
            # Dashed line
            page_story.append(Spacer(1, 0.3*inch))
            dash_data = [[Paragraph("<font color='#444444'>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -</font>", ParagraphStyle('Dash', alignment=TA_CENTER))]]
            page_story.append(Table(dash_data, colWidths=[7.2*inch]))
            page_story.append(Spacer(1, 0.3*inch))
            
            # 3. Match Details Boxes
            def _make_team_box(team_name, role):
                is_bat_first = "First" in role
                if is_noray:
                    score = cd.get('bat_first_score_noray') if is_bat_first else cd.get('bat_second_score_noray')
                    reason = cd.get('bat_first_score_reason_noray') if is_bat_first else cd.get('bat_second_score_reason_noray')
                else:
                    score = cd.get('bat_first_score') if is_bat_first else cd.get('bat_second_score')
                    reason = cd.get('bat_first_score_reason') if is_bat_first else cd.get('bat_second_score_reason')
                
                return [
                    Paragraph(f"{team_name}", ParagraphStyle('TName', fontSize=14, textColor=colors.HexColor("#FFCC00"), fontName='Helvetica-Bold', spaceAfter=4)),
                    Paragraph(f"<font color='#8C52FF'>{role}</font>", ParagraphStyle('TRole', fontSize=10, textColor=colors.white, fontName='Helvetica-Bold', spaceAfter=12)),
                    Paragraph(f"<font color='#8C52FF'>Score Prediction:</font> {score} runs", box_style),
                    Paragraph("Astrological Logic:", ParagraphStyle('Sub', fontSize=9, textColor=colors.HexColor("#FFCC00"), fontName='Helvetica-Bold')),
                    Paragraph(f"{reason}", logic_style)
                ]
                
            bat_first_team = cd.get('bat_first', team_a)
            bat_second_team = team_b if bat_first_team == team_a else team_a
            
            teams_data = [
                [_make_team_box(bat_first_team, "Batting First"), _make_team_box(bat_second_team, "Batting Second")]
            ]
            t_teams = Table(teams_data, colWidths=[3.5*inch, 3.5*inch])
            t_teams.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1A1A1D")),
                ('BOX', (0,0), (0,0), 0.5, colors.HexColor("#444444")),
                ('BOX', (1,0), (1,0), 0.5, colors.HexColor("#444444")),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 15),
                ('RIGHTPADDING', (0,0), (-1,-1), 15),
                ('TOPPADDING', (0,0), (-1,-1), 15),
                ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ]))
            page_story.append(t_teams)
            page_story.append(Spacer(1, 0.4*inch))
            
            # 4. Detailed Questions Breakdown
            page_story.append(Paragraph("Astrological Match Analysis", ParagraphStyle('H2', fontSize=14, textColor=colors.HexColor("#8C52FF"), fontName='Helvetica-Bold', spaceAfter=10)))
            
            # Q1. Toss
            page_story.append(Paragraph("1. WHO WILL WIN THE TOSS?", box_q))
            page_story.append(Paragraph(f"{cd.get('toss_winner')}", box_style))
            page_story.append(Paragraph(f"<i>Logic:<br/>{cd.get('toss_reason')}</i>", logic_style))
            
            # Q2. Bat First
            page_story.append(Paragraph("2. WHO WILL BAT FIRST?", box_q))
            page_story.append(Paragraph(f"{cd.get('bat_first')}", box_style))
            page_story.append(Paragraph(f"<i>Logic:<br/>{cd.get('bat_first_reason')}</i>", logic_style))
            
            # Formulas for Q3/Q4 based on is_noray
            bf_score = cd.get('bat_first_score_noray') if is_noray else cd.get('bat_first_score')
            bf_reason = cd.get('bat_first_score_reason_noray') if is_noray else cd.get('bat_first_score_reason')
            bs_score = cd.get('bat_second_score_noray') if is_noray else cd.get('bat_second_score')
            bs_reason = cd.get('bat_second_score_reason_noray') if is_noray else cd.get('bat_second_score_reason')
            
            # Q3. Bat First Score
            page_story.append(Paragraph("3. BATTING FIRST, WHAT SCORE WILL THEY SCORE?", box_q))
            page_story.append(Paragraph(f"{cd.get('bat_first')} will score {bf_score} runs.", box_style))
            page_story.append(Paragraph(f"<i>Logic:<br/>{bf_reason}</i>", logic_style))

            # Q4. Bat Second Score
            page_story.append(Paragraph("4. BATTING SECOND, WHAT SCORE WILL THEY SCORE?", box_q))
            page_story.append(Paragraph(f"{bat_second_team} will score {bs_score} runs.", box_style))
            page_story.append(Paragraph(f"<i>Logic:<br/>{bs_reason}</i>", logic_style))
            
            # Q5. Match Outcome detail
            page_story.append(Paragraph("5. WHO WILL WIN THE MATCH?", box_q))
            page_story.append(Paragraph(f"{cd.get('predicted_winner')} ({cd.get('predicted_margin')})", box_style))
            page_story.append(Paragraph(f"<i>Logic:<br/>{cd.get('outcome_reason')}</i>", logic_style))
            
            # Footer Note
            page_story.append(Spacer(1, 0.4*inch))
            prasna_time = self.data.get('query_time_str', 'N/A')
            loc = self.data.get('location', 'N/A')
            page_story.append(Paragraph(f"Analysis drawn for {prasna_time} at {loc} using Jamakkal Prasna Engine.", ParagraphStyle('Foot', fontSize=8, textColor=colors.HexColor("#666666"), alignment=TA_CENTER)))
            
            return page_story

        story.extend(_build_page(is_noray=False))
        story.append(PageBreak())
        story.extend(_build_page(is_noray=True))
        
        def _bg_rect(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(colors.HexColor("#121214")) # Very dark background
            canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
            canvas.restoreState()
            
        doc.build(story, onFirstPage=_bg_rect, onLaterPages=_bg_rect)
        return self.filename

    def generate(self):
        # Override to single page premium report if strictly competition mode
        if self.data.get('is_strict_competition_mode'):
            return self.generate_competition_report()
            
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
        
        def _fmt_jg(p_data):
            if not isinstance(p_data, dict): return str(p_data)
            return f"{p_data.get('rasi', '')} ({p_data.get('degree', '')})"

        for i in range(0, len(jg), 2):
            p1_name, p1_val = jg[i]
            row = [p1_name, _fmt_jg(p1_val)]
            if i+1 < len(jg):
                p2_name, p2_val = jg[i+1]
                row.extend([p2_name, _fmt_jg(p2_val)])
            else:
                row.extend(["", ""])
            jama_data.append(row)
        story.append(self._make_table(jama_data, [1*inch, 1.8*inch, 1*inch, 1.8*inch]))

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
