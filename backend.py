import json
from googleapiclient.discovery import build
import sys

print('Conectando à API do YouTube...')

# Configuração
API_KEY = 'AIzaSyAz-l0gk1N3y_ta1dfWyBKRguX_6MSafH4'  # ⚠️ Coloque sua chave da API aqui

# Dicionário: { canal_id : nome_do_canal }
canal_ids = {
    'UCy9CXl0iFafrcBA953Iqd0Q': 'The Petersens',
    'UCiLqiXa5O85APUBQV7X5w9Q': 'Redeemed Zoomer',
    'UCUQbA9X4gxe7rgoSt2DJeSA': 'The Octagon Oracle',
    'UCRy4GsY-DHfm9jJ9xF9bQ4A': 'Pastor Rodrigo Mocellin',
    'UCAL3JXZSzSm8AlZyD3nQdBA': 'Pimitive Technology',
    'UCyoRZY8w04UPXMfefw848dQ': 'Ian Z Forge',
    'UChHpGHPbuzudE6hZ-zlPn6g': 'Armory Smith',
    'UCfCUZf65OhfNNGQF0VJ-8iA': 'Hoppero MMA',
    'UCQhV2aQ3HkAd_r9I0Qz_eGg': 'Gilbert Durinho Brasil',
    'UCNQClXZDN0QWliPqyHNfLWw': 'Horse Beef MMA',
    'UCeViI8suCM0yQRtAhLX0Hhw': 'God Logic 2.0',
    'UCfTJJ9hIy6Us3JVJV_4eKzg': 'God Logic',
    'UCH7UZOQyIpvZ7qZhn2xsaAQ': 'Rushdoony Brasil',
    'UC9YkugExilgMFh36lHrXZqA': 'Tiny Notes from Home',
    'UCKYcfq8_yAieQRZ81M_A7hw': 'Torch of Christ Ministries (Phillip Blair)',
    'UCgkoN5fod5z7lhFDdHrt30Q': 'Whoever Has The Son',
    'UCSaN7bio-LGA9FXyEvJlYVw': 'SO BE IT!',
    'UCKr-liguaGWMf3f94eQXsug': 'Give Me An Answer',
    'UCC_2rswH-WYMID1aKu8oNww': "Christ's Forgiveness Ministries",
    'UC6mq_hG1SqKSQ4oINXPoXxQ': 'A Messenger of Truth',
    'UC_7n21RGpsAo9i2N7hN_uAA': 'Our Self Reliant Life',
    'UCkD7Crjh-GmF8WXlKVy1d8Q': 'AG Farm Life',
    'UCapKWgim0Eq58laxlkCfQZg': 'Farm on 212th'
}


try:
    youtube = build('youtube', 'v3', developerKey=API_KEY)
except Exception as e:
    print(f"ERRO FATAL: Falha ao inicializar a API. Detalhes: {e}")
    sys.exit(1)

todos_os_canais = []
print('Buscando e processando vídeos de cada canal...\n')

for canal_id, nome_simples in canal_ids.items():
    print(f'→ Buscando vídeos do canal: {nome_simples} ({canal_id})')

    try:
        request = youtube.search().list(
            part='snippet',
            channelId=canal_id,
            maxResults=10,
            order='date',
            type='video'
        )
        resposta = request.execute()

        videos_do_canal = []

        for item in resposta.get('items', []):
            if item['id']['kind'] != 'youtube#video':
                continue

            snippet = item['snippet']
            video_id = item['id']['videoId']

            thumbnail_url = snippet['thumbnails'].get('medium', {}).get('url')
            if not thumbnail_url:
                thumbnail_url = snippet['thumbnails'].get('default', {}).get('url', '')

            videos_do_canal.append({
                'titulo': snippet['title'],
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'embed_url': f'https://www.youtube.com/embed/{video_id}?autoplay=1&modestbranding=1&rel=0&showinfo=0&controls=1&disablekb=0&fs=1&iv_load_policy=3',
                'video_id': video_id,
                'thumbnail': thumbnail_url,
                'data': snippet['publishedAt'][:10]
            })

        todos_os_canais.append({
            'id': canal_id,
            'nome': nome_simples,
            'videos': videos_do_canal
        })

    except Exception as e:
        print(f'⚠️ ERRO: Falha ao buscar {nome_simples}: {e}\n')
        continue

# Salvar dados
if todos_os_canais:
    with open('dados.json', 'w', encoding='utf-8') as f:
        json.dump(todos_os_canais, f, ensure_ascii=False, indent=4)
    print('\n✅ Processo concluído com sucesso. Arquivo "dados.json" foi atualizado.')
else:
    print('\n❌ Nenhum canal foi carregado com sucesso.')
