from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

# Simple colour palette
HEADER_FILL = PatternFill(fill_type="solid", fgColor="D9EAD3")

THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)

TITLE_FONT = Font(name="Calibri", size=18, bold=True)
HEADER_FONT = Font(name="Calibri", size=11, bold=True)
NORMAL_FONT = Font(name="Calibri", size=11)


def title(cell):
    """Format a worksheet title."""
    cell.font = TITLE_FONT


def header(cell):
    """Format a table heading."""
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.border = THIN_BORDER
    cell.alignment = Alignment(horizontal="center")


def value(cell):
    """Format a normal value cell."""
    cell.font = NORMAL_FONT
    cell.border = THIN_BORDER


def setup_sheet(ws):
    """Apply standard formatting to every worksheet."""
    ws.freeze_panes = "A4"

    ws.column_dimensions["A"].width = 35
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 18