#!/usr/bin/env python3
"""Builds an RV Park underwriting workbook (live Excel formulas)."""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ---- styles ----------------------------------------------------------------
TITLE   = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
SECTION = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
BOLD    = Font(name="Calibri", size=11, bold=True)
LABEL   = Font(name="Calibri", size=11)
INPUTF  = Font(name="Calibri", size=11, bold=True, color="1F4E78")
NOTE    = Font(name="Calibri", size=9, italic=True, color="808080")

TITLE_FILL   = PatternFill("solid", fgColor="1F4E78")
SECTION_FILL = PatternFill("solid", fgColor="2E75B6")
INPUT_FILL   = PatternFill("solid", fgColor="FFF2CC")   # yellow = type here
TOTAL_FILL   = PatternFill("solid", fgColor="D9E1F2")
KEY_FILL     = PatternFill("solid", fgColor="E2EFDA")

thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

CUR   = '#,##0'
CUR2  = '$#,##0'
PCT   = '0.0%'
PCT2  = '0.00%'
MULT  = '0.00"x"'

wb = Workbook()

# =============================================================================
# SHEET 1 — UNDERWRITING
# =============================================================================
ws = wb.active
ws.title = "Underwriting"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 38
ws.column_dimensions["B"].width = 18
ws.column_dimensions["C"].width = 30

R = {}  # name -> cell address like "B17"

def title(text):
    ws.merge_cells("A1:C1")
    c = ws["A1"]; c.value = text; c.font = TITLE; c.fill = TITLE_FILL
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 26

def section(row, text):
    ws.merge_cells(f"A{row}:C{row}")
    c = ws[f"A{row}"]; c.value = text; c.font = SECTION; c.fill = SECTION_FILL
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 20

def row_input(row, label, value, fmt=CUR2, note="", key=None):
    ws[f"A{row}"] = label; ws[f"A{row}"].font = LABEL
    c = ws[f"B{row}"]; c.value = value; c.font = INPUTF; c.fill = INPUT_FILL
    c.number_format = fmt; c.border = BORDER
    c.alignment = Alignment(horizontal="right")
    if note:
        ws[f"C{row}"] = note; ws[f"C{row}"].font = NOTE
    if key: R[key] = f"B{row}"

def row_calc(row, label, formula, fmt=CUR2, note="", bold=False, fill=None, key=None):
    ws[f"A{row}"] = label; ws[f"A{row}"].font = BOLD if bold else LABEL
    c = ws[f"B{row}"]; c.value = formula
    c.font = BOLD if bold else LABEL
    c.number_format = fmt; c.alignment = Alignment(horizontal="right")
    if fill: c.fill = fill
    if note:
        ws[f"C{row}"] = note; ws[f"C{row}"].font = NOTE
    if key: R[key] = f"B{row}"

title("RV PARK UNDERWRITING ANALYSIS")

ws["A3"] = "Property Name"; ws["A3"].font = LABEL
ws["B3"] = "Enter property name"; ws["B3"].font = INPUTF; ws["B3"].fill = INPUT_FILL; ws["B3"].border = BORDER
ws["A4"] = "Location (City, ST)"; ws["A4"].font = LABEL
ws["B4"] = "City, ST"; ws["B4"].font = INPUTF; ws["B4"].fill = INPUT_FILL; ws["B4"].border = BORDER
ws["A5"] = "Analysis Date"; ws["A5"].font = LABEL
ws["B5"] = "2026-06-26"; ws["B5"].font = INPUTF; ws["B5"].fill = INPUT_FILL; ws["B5"].border = BORDER
ws["C3"] = "Yellow cells = your inputs. Everything else calculates."; ws["C3"].font = NOTE

# ----- Deal assumptions ------------------------------------------------------
section(7, "DEAL ASSUMPTIONS")
row_input(8,  "Number of RV Sites (pads)", 50, '#,##0', "total rentable pads", key="sites")
row_input(9,  "Purchase Price", 1500000, CUR2, key="price")
row_calc (10, "  Price per Site", f"={R['price']}/{R['sites']}", CUR2, "purchase price / sites")
row_input(11, "Avg. Monthly Rent per Site", 450, CUR2, "blended lot rent / month", key="rent")
row_input(12, "Vacancy & Credit Loss %", 0.15, PCT, "economic vacancy", key="vac")
row_input(13, "Other Income (monthly)", 1500, CUR2, "store, laundry, propane, fees", key="other_m")
row_input(14, "Management Fee (% of EGI)", 0.08, PCT, "3rd-party or self-mgmt", key="mgmt_pct")
row_input(15, "Replacement Reserves / site / yr", 100, CUR2, "capital reserve", key="res_site")
row_input(16, "Annual Rent Growth %", 0.03, PCT, "for multi-year projection", key="rent_g")
row_input(17, "Annual Expense Growth %", 0.025, PCT, "for multi-year projection", key="exp_g")

# ----- Income ----------------------------------------------------------------
section(19, "INCOME  (Year 1 Stabilized Pro Forma)")
row_calc(20, "Gross Potential Rent (GPR)", f"={R['sites']}*{R['rent']}*12", CUR2, "annual", key="gpr")
row_calc(21, "Less: Vacancy & Credit Loss", f"=-{R['gpr']}*{R['vac']}", CUR2)
R["vacloss"] = "B21"
row_calc(22, "Plus: Other Income", f"={R['other_m']}*12", CUR2, key="other_a")
row_calc(23, "Effective Gross Income (EGI)", f"={R['gpr']}+{R['vacloss']}+{R['other_a']}",
         CUR2, bold=True, fill=TOTAL_FILL, key="egi")

# ----- Operating expenses ----------------------------------------------------
section(25, "OPERATING EXPENSES  (Year 1)")
row_input(26, "Property Taxes", 18000, CUR2, key="tax")
row_input(27, "Insurance", 9000, CUR2, key="ins")
row_input(28, "Utilities (water/sewer/trash/elec)", 36000, CUR2, "owner-paid portion", key="util")
row_input(29, "Repairs & Maintenance", 15000, CUR2, key="rm")
row_input(30, "Payroll / Onsite Manager", 24000, CUR2, key="pay")
row_input(31, "Marketing, Admin, Office", 8000, CUR2, key="admin")
row_calc (32, "Management Fee", f"={R['mgmt_pct']}*{R['egi']}", CUR2, "= mgmt % x EGI", key="mgmt")
row_calc (33, "Replacement Reserves", f"={R['res_site']}*{R['sites']}", CUR2, key="reserves")
row_calc (34, "Total Operating Expenses",
         f"=SUM({R['tax']}:{R['reserves'].replace('B','B')})", CUR2, bold=True, fill=TOTAL_FILL, key="opex")
# fix the sum range explicitly
ws[R["opex"]].value = f"=SUM(B26:B33)"
row_calc (35, "Operating Expense Ratio", f"={R['opex']}/{R['egi']}", PCT, "OpEx / EGI", key="oer")
row_calc (36, "Expenses per Site", f"={R['opex']}/{R['sites']}", CUR2)

# ----- NOI -------------------------------------------------------------------
section(38, "NET OPERATING INCOME")
row_calc(39, "Net Operating Income (NOI)", f"={R['egi']}-{R['opex']}", CUR2,
         bold=True, fill=KEY_FILL, key="noi")
row_calc(40, "NOI per Site", f"={R['noi']}/{R['sites']}", CUR2)

# ----- Financing & exit assumptions -----------------------------------------
section(42, "FINANCING & EXIT ASSUMPTIONS")
row_input(43, "Loan-to-Value (LTV) %", 0.70, PCT, key="ltv")
row_input(44, "Interest Rate %", 0.07, PCT2, "annual", key="intr")
row_input(45, "Amortization (years)", 25, '#,##0', key="amort")
row_input(46, "Closing Costs %", 0.03, PCT, "of purchase price", key="close_pct")
row_input(47, "Initial CapEx / Rehab", 50000, CUR2, "day-one improvements", key="capex")
row_input(48, "Hold Period (years)", 5, '#,##0', "1-10", key="hold")
row_input(49, "Exit Cap Rate %", 0.085, PCT2, "for sale value", key="exitcap")
row_input(50, "Selling Costs %", 0.05, PCT, "of sale price", key="sellcost")

# ----- Debt & equity ---------------------------------------------------------
section(52, "DEBT & EQUITY")
row_calc(53, "Loan Amount", f"={R['price']}*{R['ltv']}", CUR2, key="loan")
row_calc(54, "Down Payment (Equity)", f"={R['price']}-{R['loan']}", CUR2, key="down")
row_calc(55, "Closing Costs", f"={R['price']}*{R['close_pct']}", CUR2, key="close")
row_calc(56, "Total Cash Required",
         f"={R['down']}+{R['close']}+{R['capex']}", CUR2, bold=True, fill=TOTAL_FILL, key="cash")
row_calc(57, "Monthly Debt Payment",
         f"=PMT({R['intr']}/12,{R['amort']}*12,-{R['loan']})", CUR2, key="pmt_m")
row_calc(58, "Annual Debt Service", f"={R['pmt_m']}*12", CUR2, bold=True, key="ads")

# ----- Returns ---------------------------------------------------------------
section(60, "KEY RETURN METRICS  (Year 1)")
row_calc(61, "Going-in Cap Rate", f"={R['noi']}/{R['price']}", PCT, "NOI / Price",
         bold=True, fill=KEY_FILL, key="caprate")
row_calc(62, "Cash Flow Before Tax (CFBT)", f"={R['noi']}-{R['ads']}", CUR2,
         bold=True, fill=KEY_FILL, key="cfbt")
row_calc(63, "Cash-on-Cash Return", f"={R['cfbt']}/{R['cash']}", PCT, "CFBT / cash invested",
         bold=True, fill=KEY_FILL, key="coc")
row_calc(64, "Debt Service Coverage (DSCR)", f"={R['noi']}/{R['ads']}", MULT,
         "lenders want >= 1.25x", bold=True, fill=KEY_FILL, key="dscr")
row_calc(65, "Gross Rent Multiplier (GRM)", f"={R['price']}/{R['gpr']}", '0.00"x"')
row_calc(66, "Break-even Occupancy",
         f"=({R['opex']}+{R['ads']})/({R['gpr']}+{R['other_a']})", PCT,
         "occupancy needed to cover costs", key="breakeven")
row_calc(67, "Debt Yield", f"={R['noi']}/{R['loan']}", PCT, "NOI / loan (lender metric)")

for r in range(3, 68):
    ws.row_dimensions[r].height = max(ws.row_dimensions[r].height or 15, 15)

# =============================================================================
# SHEET 2 — 10-YEAR PRO FORMA & IRR
# =============================================================================
pf = wb.create_sheet("Pro Forma & Returns")
pf.sheet_view.showGridLines = False
pf.column_dimensions["A"].width = 34
for i in range(11):  # B..L for year 0..10
    pf.column_dimensions[get_column_letter(2 + i)].width = 13

pf.merge_cells("A1:L1")
c = pf["A1"]; c.value = "10-YEAR PRO FORMA & RETURNS"; c.font = TITLE; c.fill = TITLE_FILL
c.alignment = Alignment(horizontal="center", vertical="center")
pf.row_dimensions[1].height = 26

U = "Underwriting!"
def uref(key): return U + R[key]

# header row 3: Year 0..10
pf["A3"] = "Year"; pf["A3"].font = BOLD; pf["A3"].fill = SECTION_FILL; pf["A3"].font = SECTION
for y in range(0, 11):
    col = get_column_letter(2 + y)
    cc = pf[f"{col}3"]; cc.value = y; cc.font = SECTION; cc.fill = SECTION_FILL
    cc.alignment = Alignment(horizontal="center")

def pf_row(row, label, fn, fmt=CUR2, bold=False, fill=None):
    pf[f"A{row}"] = label
    pf[f"A{row}"].font = BOLD if bold else LABEL
    for y in range(0, 11):
        col = get_column_letter(2 + y)
        cell = pf[f"{col}{row}"]
        v = fn(y, col)
        if v is None:
            continue
        cell.value = v
        cell.number_format = fmt
        cell.font = BOLD if bold else LABEL
        cell.alignment = Alignment(horizontal="right")
        if fill: cell.fill = fill

# growth factor helper for year y (operating year y, y>=1)
def gpr_y(y, col):
    if y == 0: return None
    return f"={uref('gpr')}*(1+{uref('rent_g')})^{y-1}"
pf_row(5, "Gross Potential Rent", gpr_y)

def vac_y(y, col):
    if y == 0: return None
    return f"=-{col}5*{uref('vac')}"
pf_row(6, "Less: Vacancy & Credit Loss", vac_y)

def other_y(y, col):
    if y == 0: return None
    return f"={uref('other_a')}*(1+{uref('rent_g')})^{y-1}"
pf_row(7, "Other Income", other_y)

def egi_y(y, col):
    if y == 0: return None
    return f"={col}5+{col}6+{col}7"
pf_row(8, "Effective Gross Income", egi_y, bold=True, fill=TOTAL_FILL)

# operating expenses: base opex grows, but management fee tracks EGI; keep simple: total opex grows w/ expense growth
def opex_y(y, col):
    if y == 0: return None
    return f"={uref('opex')}*(1+{uref('exp_g')})^{y-1}"
pf_row(9, "Operating Expenses", opex_y)

def noi_y(y, col):
    if y == 0: return None
    return f"={col}8-{col}9"
pf_row(10, "Net Operating Income", noi_y, bold=True, fill=KEY_FILL)

def ads_y(y, col):
    if y == 0: return None
    return f"=IF({y}<={uref('hold')},{uref('ads')},0)"
pf_row(11, "Annual Debt Service", ads_y)

# loan balance at end of year y (algebraic): L*(1+i)^k - PMT*((1+i)^k-1)/i
def bal_y(y, col):
    i = f"({uref('intr')}/12)"
    pmt = f"(-{uref('pmt_m')})"  # PMT returns negative; flip to positive payment
    # Underwriting PMT was computed with -loan so result positive; pmt_m is positive already
    pmt = uref('pmt_m')
    k = f"MIN({y},{uref('amort')})*12"
    L = uref('loan')
    if y == 0:
        return f"={L}"
    return (f"={L}*(1+{i})^({k})-{pmt}*(((1+{i})^({k})-1)/{i})")
pf_row(12, "Loan Balance (end of yr)", bal_y, fmt=CUR2)

# operating cash flow before tax, only during hold
def cfo_y(y, col):
    if y == 0: return None
    return f"=IF({y}<={uref('hold')},{col}10-{col}11,0)"
pf_row(13, "Operating Cash Flow", cfo_y, bold=True)

# reversion (sale) in the hold year: sale price = next-year NOI / exit cap
def sale_y(y, col):
    if y == 0: return None
    nextcol = get_column_letter(2 + y + 1) if y < 10 else None
    # forward NOI = this year's NOI grown one more year
    fwd = f"{col}10*(1+{uref('exp_g')})"  # approx forward NOI growth
    saleprice = f"({col}10*(1+{uref('rent_g')}))/{uref('exitcap')}"
    net = f"({saleprice})*(1-{uref('sellcost')})-{col}12"
    return f"=IF({y}={uref('hold')},{net},0)"
pf_row(14, "Net Sale Proceeds (reversion)", sale_y, fill=TOTAL_FILL)

# total cash flow for IRR: year 0 = -total cash; years = operating CF + reversion
def cft_y(y, col):
    if y == 0:
        return f"=-{uref('cash')}"
    return f"={col}13+{col}14"
pf_row(15, "Total Cash Flow (for IRR)", cft_y, bold=True, fill=KEY_FILL)

pf.row_dimensions[3].height = 18

# ----- returns summary block -------------------------------------------------
pf["A17"] = "RETURN SUMMARY (over hold period)";
pf.merge_cells("A17:D17")
pf["A17"].font = SECTION; pf["A17"].fill = SECTION_FILL
pf["A17"].alignment = Alignment(horizontal="left", indent=1)

def summ(row, label, formula, fmt, note=""):
    pf[f"A{row}"] = label; pf[f"A{row}"].font = BOLD
    cc = pf[f"B{row}"]; cc.value = formula; cc.number_format = fmt
    cc.font = BOLD; cc.fill = KEY_FILL; cc.alignment = Alignment(horizontal="right")
    if note:
        pf[f"C{row}"] = note; pf[f"C{row}"].font = NOTE

# IRR over B15:L15 (years 0..10); trailing zeros after sale are fine
summ(18, "Levered IRR", "=IRR(B15:L15)", PCT, "internal rate of return on equity")
summ(19, "Equity Multiple", "=SUM(C13:L13)/-B15 + (SUMIF... )", MULT)
# proper equity multiple: (sum operating CF + reversion) / initial equity
pf["B19"].value = "=(SUM(C13:L13)+SUM(C14:L14))/-B15"
summ(20, "Avg. Cash-on-Cash", f"=AVERAGEIF(C11:L11,\">0\",C13:L13)/{U+R['cash']}", PCT,
     "avg operating CF / equity during hold")
summ(21, "Year-1 Cash-on-Cash", f"={U+R['coc']}", PCT)
summ(22, "Going-in Cap Rate", f"={U+R['caprate']}", PCT)
summ(23, "Total Profit", "=SUM(C13:L13)+SUM(C14:L14)+B15", CUR2, "all cash flows incl. equity out")

# =============================================================================
# SHEET 3 — INSTRUCTIONS
# =============================================================================
ins = wb.create_sheet("Read Me", 0)
ins.sheet_view.showGridLines = False
ins.column_dimensions["A"].width = 100
ins.merge_cells("A1:A1")
ins["A1"] = "RV PARK UNDERWRITING — HOW TO USE"
ins["A1"].font = TITLE; ins["A1"].fill = TITLE_FILL
ins["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ins.row_dimensions[1].height = 26

lines = [
    "",
    "WHAT THIS IS",
    "A deal screening model for buying RV parks. Plug in a property's numbers and it tells you the cap rate,",
    "cash flow, cash-on-cash return, DSCR, and a 5-10 year IRR so you can decide if a deal works.",
    "",
    "HOW TO USE IT",
    "1. Go to the 'Underwriting' tab.",
    "2. Fill in every YELLOW cell with the property's real numbers (from the seller's P&L / rent roll).",
    "3. Everything that isn't yellow calculates automatically — do not type over formulas.",
    "4. Check the green 'KEY RETURN METRICS' box for the headline numbers.",
    "5. Open the 'Pro Forma & Returns' tab for the multi-year projection and IRR.",
    "",
    "THE INPUTS THAT MATTER MOST",
    "  • Number of sites, purchase price, and average monthly lot rent drive the income.",
    "  • Vacancy & Credit Loss — be honest; verify against the actual rent roll, not the pro forma.",
    "  • Operating expenses — get the seller's trailing-12 P&L. Watch for understated taxes (they reset",
    "    on sale) and missing management/payroll/reserves.",
    "  • Financing — LTV, interest rate, amortization. Update to your actual lender quote.",
    "  • Exit Cap Rate — usually set 0.5%-1.0% HIGHER than the going-in cap to be conservative.",
    "",
    "RULES OF THUMB (screening, not gospel)",
    "  • Cap rate: 8%+ is typical for RV parks; lower means you're paying up.",
    "  • DSCR: lenders want 1.25x or better. Below 1.20x is a financing risk.",
    "  • Cash-on-Cash: 8-12%+ year one is a healthy target.",
    "  • Expense ratio: 35-50% of EGI is normal; under 30% usually means expenses are understated.",
    "  • Always underwrite to ACTUALS first, then to your stabilized pro forma separately.",
    "",
    "WATCH-OUTS SPECIFIC TO RV PARKS",
    "  • Transient vs. annual/monthly mix — transient income is seasonal and far less stable.",
    "  • Utility metering — are sites individually metered or is the owner eating utilities?",
    "  • Infrastructure age — septic/sewer, electric pedestals (30/50 amp), and water lines are big CapEx.",
    "  • Flood zone, seasonal closures, and percentage of park-owned rentals vs. tenant-owned rigs.",
    "",
    "This is a screening tool, not investment advice. Verify every number and consult professionals.",
]
r = 2
for ln in lines:
    ins[f"A{r}"] = ln
    if ln.isupper() and ln.strip() and not ln.startswith(" "):
        ins[f"A{r}"].font = Font(bold=True, size=12, color="1F4E78")
    else:
        ins[f"A{r}"].font = Font(size=11)
    r += 1

wb.save("RV_Park_Underwriting.xlsx")
print("Saved RV_Park_Underwriting.xlsx")
