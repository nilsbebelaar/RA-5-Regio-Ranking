import cloudflare
from dotenv import load_dotenv
from environs import Env
from minify_html import minify as minify_html
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import openpyxl


file_loader = FileSystemLoader('excel_to_table/templates')
env = Environment(loader=file_loader)
template = env.get_template('ranking_table.html')


workbook = openpyxl.load_workbook(r"R:\Shared drives\Rotterdam Atletiek\2. Baanatletiek\Wedstrijdorganisatie\8. 5-Regio Rijnmond\5-Regio 2023\Organisatie 3 juni\Uitslagen\Uitslagentabel met punten 5-Regio Ontmoeting 2023.xlsm", data_only=True)
worksheet = workbook.worksheets[0]

ranking = {
    'Dordrecht': {
        'color': 'red',
        'punten': worksheet['E16'].value,
        'rank': worksheet['B17'].value,
        'details': [
            {'naam': 'U9', 'Mannen': worksheet['B4'].value, 'Vrouwen': worksheet['C4'].value, 'Estafette': worksheet['D4'].value, 'Totaal': worksheet['E4'].value},
            {'naam': 'U10', 'Mannen': worksheet['B5'].value, 'Vrouwen': worksheet['C5'].value, 'Estafette': worksheet['D5'].value, 'Totaal': worksheet['E5'].value},
            {'naam': 'U11', 'Mannen': worksheet['B6'].value, 'Vrouwen': worksheet['C6'].value, 'Estafette': worksheet['D6'].value, 'Totaal': worksheet['E6'].value},
            {'naam': 'U12', 'Mannen': worksheet['B7'].value, 'Vrouwen': worksheet['C7'].value, 'Estafette': worksheet['D7'].value, 'Totaal': worksheet['E7'].value},
            {'naam': 'U14-V', 'Vrouwen': worksheet['C9'].value, 'Estafette': worksheet['D9'].value, 'Totaal': worksheet['E9'].value},
            {'naam': 'U14-M', 'Mannen': worksheet['B10'].value, 'Estafette': worksheet['D10'].value, 'Totaal': worksheet['E10'].value},
            {'naam': 'U16-V', 'Vrouwen': worksheet['C11'].value, 'Estafette': worksheet['D11'].value, 'Totaal': worksheet['E11'].value},
            {'naam': 'U16-M', 'Mannen': worksheet['B12'].value, 'Estafette': worksheet['D12'].value, 'Totaal': worksheet['E12'].value},
            {'naam': 'Pendel', 'Totaal': worksheet['E14'].value},
        ]
    },
    'Haaglanden': {
        'color': 'orange',
        'punten': worksheet['I16'].value,
        'rank': worksheet['F17'].value,
        'details': [
            {'naam': 'U9', 'Mannen': worksheet['F4'].value, 'Vrouwen': worksheet['G4'].value, 'Estafette': worksheet['H4'].value, 'Totaal': worksheet['I4'].value},
            {'naam': 'U10', 'Mannen': worksheet['F5'].value, 'Vrouwen': worksheet['G5'].value, 'Estafette': worksheet['H5'].value, 'Totaal': worksheet['I5'].value},
            {'naam': 'U11', 'Mannen': worksheet['F6'].value, 'Vrouwen': worksheet['G6'].value, 'Estafette': worksheet['H6'].value, 'Totaal': worksheet['I6'].value},
            {'naam': 'U12', 'Mannen': worksheet['F7'].value, 'Vrouwen': worksheet['G7'].value, 'Estafette': worksheet['H7'].value, 'Totaal': worksheet['I7'].value},
            {'naam': 'U14-V', 'Vrouwen': worksheet['G9'].value, 'Estafette': worksheet['H9'].value, 'Totaal': worksheet['I9'].value},
            {'naam': 'U14-M', 'Mannen': worksheet['F10'].value, 'Estafette': worksheet['H10'].value, 'Totaal': worksheet['I10'].value},
            {'naam': 'U16-V', 'Vrouwen': worksheet['G11'].value, 'Estafette': worksheet['H11'].value, 'Totaal': worksheet['I11'].value},
            {'naam': 'U16-M', 'Mannen': worksheet['F12'].value, 'Estafette': worksheet['H12'].value, 'Totaal': worksheet['I12'].value},
            {'naam': 'Pendel', 'Totaal': worksheet['I14'].value},
        ]
    },
    'Rijnmond': {
        'color': 'green',
        'punten': worksheet['M16'].value,
        'rank': worksheet['J17'].value,
        'details': [
            {'naam': 'U9', 'Mannen': worksheet['J4'].value, 'Vrouwen': worksheet['K4'].value, 'Estafette': worksheet['L4'].value, 'Totaal': worksheet['M4'].value},
            {'naam': 'U10', 'Mannen': worksheet['J5'].value, 'Vrouwen': worksheet['K5'].value, 'Estafette': worksheet['L5'].value, 'Totaal': worksheet['M5'].value},
            {'naam': 'U11', 'Mannen': worksheet['J6'].value, 'Vrouwen': worksheet['K6'].value, 'Estafette': worksheet['L6'].value, 'Totaal': worksheet['M6'].value},
            {'naam': 'U12', 'Mannen': worksheet['J7'].value, 'Vrouwen': worksheet['K7'].value, 'Estafette': worksheet['L7'].value, 'Totaal': worksheet['M7'].value},
            {'naam': 'U14-V', 'Vrouwen': worksheet['K9'].value, 'Estafette': worksheet['L9'].value, 'Totaal': worksheet['M9'].value},
            {'naam': 'U14-M', 'Mannen': worksheet['J10'].value, 'Estafette': worksheet['L10'].value, 'Totaal': worksheet['M10'].value},
            {'naam': 'U16-V', 'Vrouwen': worksheet['K11'].value, 'Estafette': worksheet['L11'].value, 'Totaal': worksheet['M11'].value},
            {'naam': 'U16-M', 'Mannen': worksheet['J12'].value, 'Estafette': worksheet['L12'].value, 'Totaal': worksheet['M12'].value},
            {'naam': 'Pendel', 'Totaal': worksheet['M14'].value},
        ]
    },
    'West-Brabant': {
        'color': 'yellow',
        'punten': worksheet['Q16'].value,
        'rank': worksheet['N17'].value,
        'details': [
            {'naam': 'U9', 'Mannen': worksheet['N4'].value, 'Vrouwen': worksheet['O4'].value, 'Estafette': worksheet['P4'].value, 'Totaal': worksheet['Q4'].value},
            {'naam': 'U10', 'Mannen': worksheet['N5'].value, 'Vrouwen': worksheet['O5'].value, 'Estafette': worksheet['P5'].value, 'Totaal': worksheet['Q5'].value},
            {'naam': 'U11', 'Mannen': worksheet['N6'].value, 'Vrouwen': worksheet['O6'].value, 'Estafette': worksheet['P6'].value, 'Totaal': worksheet['Q6'].value},
            {'naam': 'U12', 'Mannen': worksheet['N7'].value, 'Vrouwen': worksheet['O7'].value, 'Estafette': worksheet['P7'].value, 'Totaal': worksheet['Q7'].value},
            {'naam': 'U14-V', 'Vrouwen': worksheet['O9'].value, 'Estafette': worksheet['P9'].value, 'Totaal': worksheet['Q9'].value},
            {'naam': 'U14-M', 'Mannen': worksheet['N10'].value, 'Estafette': worksheet['P10'].value, 'Totaal': worksheet['Q10'].value},
            {'naam': 'U16-V', 'Vrouwen': worksheet['O11'].value, 'Estafette': worksheet['P11'].value, 'Totaal': worksheet['Q11'].value},
            {'naam': 'U16-M', 'Mannen': worksheet['N12'].value, 'Estafette': worksheet['P12'].value, 'Totaal': worksheet['Q12'].value},
            {'naam': 'Pendel', 'Totaal': worksheet['Q14'].value},
        ]
    },
    'Zeeland': {
        'color': 'blue',
        'punten': worksheet['U16'].value,
        'rank': worksheet['R17'].value,
        'details': [
            {'naam': 'U9', 'Mannen': worksheet['R4'].value, 'Vrouwen': worksheet['S4'].value, 'Estafette': worksheet['T4'].value, 'Totaal': worksheet['U4'].value},
            {'naam': 'U10', 'Mannen': worksheet['R5'].value, 'Vrouwen': worksheet['S5'].value, 'Estafette': worksheet['T5'].value, 'Totaal': worksheet['U5'].value},
            {'naam': 'U11', 'Mannen': worksheet['R6'].value, 'Vrouwen': worksheet['S6'].value, 'Estafette': worksheet['T6'].value, 'Totaal': worksheet['U6'].value},
            {'naam': 'U12', 'Mannen': worksheet['R7'].value, 'Vrouwen': worksheet['S7'].value, 'Estafette': worksheet['T7'].value, 'Totaal': worksheet['U7'].value},
            {'naam': 'U14-V', 'Vrouwen': worksheet['S9'].value, 'Estafette': worksheet['T9'].value, 'Totaal': worksheet['U9'].value},
            {'naam': 'U14-M', 'Mannen': worksheet['R10'].value, 'Estafette': worksheet['T10'].value, 'Totaal': worksheet['U10'].value},
            {'naam': 'U16-V', 'Vrouwen': worksheet['S11'].value, 'Estafette': worksheet['T11'].value, 'Totaal': worksheet['U11'].value},
            {'naam': 'U16-M', 'Mannen': worksheet['R12'].value, 'Estafette': worksheet['T12'].value, 'Totaal': worksheet['U12'].value},
            {'naam': 'Pendel', 'Totaal': worksheet['U14'].value},
        ]
    },
}

ranking = dict(sorted(ranking.items(), key=lambda x: x[1]['rank']))

output = template.render(ranking=ranking, time=datetime.now().strftime("%d-%m-%Y %H:%M"))
output = minify_html(output, keep_closing_tags=True,)

load_dotenv()
env = Env()

print(cloudflare.set_kv(
    account_id=env('CF_ACCOUNT_ID'),
    api_key=env('CF_API_KEY'),
    namespace_id=env('CF_KV_NAMESPACE_ID'),
    key='main_ranking',
    value=minify_html(output)
))
