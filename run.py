import argparse
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta

# Configurar argumentos de linha de comando
parser = argparse.ArgumentParser(description='Processar um arquivo GPX e corrigir pausas.')
parser.add_argument('gpx_file_path', type=str, help='Caminho para o arquivo GPX de entrada.')
parser.add_argument('momento_ida', type=str, help='Horário de início da ida no formato ISO 8601 (ex: 2025-02-22T10:05:15+00:00).')
parser.add_argument('momento_pausa', type=str, help='Horário de início da pausa no formato ISO 8601 (ex: 2025-02-22T10:56:30+00:00).')
parser.add_argument('momento_continuacao', type=str, help='Horário de continuação após a pausa no formato ISO 8601 (ex: 2025-02-22T11:27:42+00:00).')
parser.add_argument('output_path', type=str, help='Caminho para salvar o arquivo GPX corrigido.')

args = parser.parse_args()

# Carregar o arquivo GPX
gpx_file_path = args.gpx_file_path
tree = ET.parse(gpx_file_path)
root = tree.getroot()

# Namespace do GPX
namespace = {'default': 'http://www.topografix.com/GPX/1/1',
             'gpxtpx': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'}

# Remover o prefixo "ns0" ao salvar o arquivo
ET.register_namespace('', 'http://www.topografix.com/GPX/1/1')
ET.register_namespace('gpxtpx', 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1')

# Encontrar todos os pontos de track (trkpt)
trkpts = root.findall(".//default:trkpt", namespace)

# Converter horários para datetime e identificar os pontos relevantes
pontos_ida = []
ponto_pausa = None
ponto_continuacao = None

momento_ida = datetime.fromisoformat(args.momento_ida)
momento_pausa = datetime.fromisoformat(args.momento_pausa)
momento_continuacao = datetime.fromisoformat(args.momento_continuacao)

for trkpt in trkpts:
    ele = float(trkpt.find('default:ele', namespace).text)
    time = datetime.fromisoformat(trkpt.find('default:time', namespace).text.replace('Z', '+00:00'))

    # Identificar o ponto na ida, equivalente ao de continuação da pausa
    if time >= momento_ida and time < momento_pausa:
        pontos_ida.append(trkpt)

    # Identificar o ponto de pausa
    if time == momento_pausa:
        ponto_pausa = trkpt

    # Identificar o momento que continua o treino
    if time == momento_continuacao:
        ponto_continuacao = trkpt

# Calcular o tempo pausado
tempo_pausado = (momento_continuacao - momento_pausa).total_seconds()

# Duplicar os pontos da subida
tempo_por_ponto = tempo_pausado / len(pontos_ida)

# Criar novos pontos para o trecho pausado
novos_pontos = []
for i, trkpt in enumerate(pontos_ida):
    novo_ponto = ET.Element('trkpt', attrib=trkpt.attrib)  # Cria um novo elemento <trkpt> com os mesmos atributos
    for child in trkpt:
        novo_child = ET.Element(child.tag, attrib=child.attrib)  # Copia cada subelemento (elevação, tempo, etc.)
        novo_child.text = child.text
        novo_ponto.append(novo_child)

    # Ajustar o tempo
    novo_tempo = momento_pausa - timedelta(seconds=i * tempo_por_ponto)
    # Garantir que o elemento <time> exista no novo ponto
    time_element = novo_ponto.find('default:time', namespace)

    # Atualizar o valor do elemento <time> com o formato correto
    time_element.text = novo_tempo.strftime('%Y-%m-%dT%H:%M:%SZ')  # Formato correto           
            
    extensions = novo_ponto.find('default:extensions', namespace)
    tracpointExtension = ET.Element('gpxtpx:TrackPointExtension')
    cad = ET.Element('gpxtpx:cad')
    cad.text = '0'
    tracpointExtension.append(cad)
    extensions.append(tracpointExtension)

    novos_pontos.append(novo_ponto)

# Inserir os novos pontos no arquivo GPX
for novo_ponto in novos_pontos:
    root.find('.//default:trkseg', namespace).insert(trkpts.index(ponto_pausa) + 1, novo_ponto)

# Salvar o arquivo corrigido
output_path = args.output_path
tree.write(output_path, encoding='utf-8', xml_declaration=True)

print(f"Arquivo corrigido salvo em: {output_path}")