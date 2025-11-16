#!/usr/bin/env python3
"""
Script per popolare il database con eventi e notizie di esempio.
Esegui questo script con: python populate_eventi_notizie.py
"""
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from parco_verismo.models import Evento, Notizia

def populate():
    print("Popolamento del database con eventi e notizie...")
    
    # Eventi di esempio
    eventi_data = [
        {
            'titolo': 'Presentazione del romanzo "I Malavoglia"',
            'slug': 'presentazione-i-malavoglia',
            'descrizione': '''Il Parco Letterario del Verismo organizza una serata speciale dedicata al capolavoro
di Giovanni Verga. L'evento prevede una lettura guidata dei passi più significativi del romanzo,
seguita da un dibattito con esperti letterari e studiosi del verismo siciliano.

Saranno presenti:
- Letture a cura di attori professionisti
- Analisi critica dell'opera
- Dibattito con il pubblico
- Degustazione di prodotti tipici siciliani

L'evento si terrà nella suggestiva cornice di Aci Trezza, luogo natale del romanzo.''',
            'data_inizio': datetime(2025, 12, 15, 18, 30),
            'data_fine': datetime(2025, 12, 15, 22, 00),
            'luogo': 'Aci Trezza - Teatro Comunale',
            'indirizzo': 'Via Teatro, 1 - 95021 Aci Trezza (CT)',
            'is_active': True
        },
        {
            'titolo': 'Visita guidata al Parco Letterario',
            'slug': 'visita-guidata-parco',
            'descrizione': '''Scopri i luoghi che hanno ispirato le opere di Verga e Capuana in una visita guidata
esclusiva organizzata dal Parco Letterario del Verismo.

Il percorso toccherà:
- I luoghi di "I Malavoglia" ad Aci Trezza
- La casa natale di Luigi Capuana a Mineo
- I paesaggi che hanno ispirato "Vita dei campi"
- Le chiese e i monumenti storici menzionati nelle opere

La visita è gratuita e dura circa 3 ore. Prenotazione obbligatoria.''',
            'data_inizio': datetime(2025, 11, 20, 9, 00),
            'data_fine': datetime(2025, 11, 20, 12, 00),
            'luogo': 'Punto di ritrovo: Municipio di Aci Trezza',
            'indirizzo': 'Piazza Municipio - 95021 Aci Trezza (CT)',
            'is_active': True
        },
        {
            'titolo': 'Convegno: Il Verismo oggi',
            'slug': 'convegno-verismo-oggi',
            'descrizione': '''Un convegno internazionale dedicato all'attualità del verismo nella letteratura
contemporanea. Interverranno critici letterari, scrittori e accademici da tutta Italia.

Temi trattati:
- L'eredità del verismo nella narrativa italiana contemporanea
- Verga e Capuana: maestri del realismo
- Il verismo siciliano e la letteratura europea
- Nuove prospettive critiche sul movimento verista

L'evento è accreditato per la formazione docenti.''',
            'data_inizio': datetime(2026, 1, 25, 9, 30),
            'data_fine': datetime(2026, 1, 25, 18, 00),
            'luogo': 'Università di Catania - Aula Magna',
            'indirizzo': 'Via Biblioteca, 4 - 95124 Catania',
            'is_active': True
        }
    ]
    
    print("\n" + "="*60)
    print("Aggiunta eventi")
    print("="*60)
    
    for evento_data in eventi_data:
        defaults = {k: evento_data[k] for k in ['data_inizio', 'data_fine', 'immagine'] if k in evento_data}
        defaults.update({'is_active': evento_data.get('is_active', True)})
        evento, created = Evento.objects.get_or_create(
            slug=evento_data['slug'],
            defaults=defaults
        )
        if not created:
            evento.data_inizio = evento_data['data_inizio']
            evento.data_fine = evento_data['data_fine']
            evento.is_active = evento_data.get('is_active', True)
        evento.set_current_language('it')
        evento.titolo = evento_data['titolo']
        evento.descrizione = evento_data['descrizione']
        evento.luogo = evento_data['luogo']
        evento.indirizzo = evento_data['indirizzo']
        evento.save()
        if created:
            print(f"✓ Creato evento: {evento.titolo} ({evento.data_inizio.date()})")
        else:
            print(f"• Evento aggiornato: {evento.titolo}")
    
    # Notizie di esempio
    notizie_data = [
        {
            'titolo': 'Il Parco Letterario del Verismo ottiene il riconoscimento UNESCO',
            'slug': 'riconoscimento-unesco',
            'contenuto': '''Siamo orgogliosi di annunciare che il Parco Letterario del Verismo è stato ufficialmente
riconosciuto come Patrimonio Culturale Immateriale dell'Umanità dall'UNESCO.

Questo importante riconoscimento premia il lavoro svolto negli ultimi anni per la valorizzazione
del patrimonio letterario verista e la promozione della cultura siciliana nel mondo.

Il riconoscimento UNESCO rappresenta un importante passo avanti per la tutela e la promozione
del nostro patrimonio culturale, e ci impegna a continuare il nostro lavoro con ancora maggiore
dedizione e professionalità.

Ringraziamo tutti i partner, le istituzioni e i cittadini che hanno sostenuto questo progetto.''',
            'riassunto': 'Il Parco Letterario del Verismo ottiene il prestigioso riconoscimento UNESCO come Patrimonio Culturale Immateriale.',
            'is_active': True
        },
        {
            'titolo': 'Nuova pubblicazione: Guida ai luoghi verghiani',
            'slug': 'guida-luoghi-verghiani',
            'contenuto': '''È disponibile la nuova guida "Alla scoperta dei luoghi verghiani", una pubblicazione
bilingue (italiano-inglese) che accompagna i visitatori alla scoperta dei luoghi che hanno ispirato
le opere di Giovanni Verga.

La guida, realizzata in collaborazione con l'Università di Catania, contiene:
- Mappe dettagliate dei percorsi letterari
- Descrizioni storiche e letterarie dei luoghi
- Fotografie d'epoca e moderne
- Citazioni dalle opere di Verga
- Informazioni pratiche per i visitatori

La pubblicazione è disponibile gratuitamente presso gli uffici del Parco e sul nostro sito web.''',
            'riassunto': 'Disponibile la nuova guida bilingue per scoprire i luoghi che hanno ispirato le opere di Giovanni Verga.',
            'is_active': True
        },
        {
            'titolo': 'Progetto educativo: Il verismo a scuola',
            'slug': 'progetto-educativo-verismo',
            'contenuto': '''Il Parco Letterario del Verismo ha avviato un nuovo progetto educativo rivolto
agli studenti delle scuole superiori siciliane.

Il progetto "Il verismo a scuola" prevede:
- Visite guidate gratuite per le classi
- Laboratori di scrittura creativa ispirati al verismo
- Incontri con scrittori e critici letterari
- Concorso letterario per studenti
- Materiali didattici digitali

L'iniziativa coinvolgerà oltre 50 istituti scolastici e mira a far conoscere il movimento
verista alle nuove generazioni, stimolando l'interesse per la letteratura e la cultura siciliana.

Le scuole interessate possono contattare gli uffici del Parco per informazioni e prenotazioni.''',
            'riassunto': 'Nuovo progetto educativo per portare il verismo nelle scuole siciliane con visite guidate e laboratori.',
            'is_active': True
        }
    ]
    
    print("\n" + "="*60)
    print("Aggiunta notizie")
    print("="*60)
    
    for notizia_data in notizie_data:
        notizia, created = Notizia.objects.get_or_create(
            slug=notizia_data['slug'],
            defaults={
                'is_active': notizia_data.get('is_active', True)
            }
        )
        if not created:
            notizia.is_active = notizia_data.get('is_active', True)
        notizia.set_current_language('it')
        notizia.titolo = notizia_data['titolo']
        notizia.contenuto = notizia_data['contenuto']
        notizia.riassunto = notizia_data['riassunto']
        notizia.save()
        if created:
            print(f"✓ Creata notizia: {notizia.titolo}")
        else:
            print(f"• Notizia aggiornata: {notizia.titolo}")
    
    print("\n" + "="*60)
    print("✓ Popolamento completato con successo!")
    print("="*60)
    print(f"\nTotale eventi: {Evento.objects.count()}")
    print(f"Totale notizie: {Notizia.objects.count()}")
    print("\nPuoi ora visitare:")
    print("  - Eventi: http://127.0.0.1:8000/eventi/")
    print("  - Calendario: http://127.0.0.1:8000/calendario/")
    print("  - Notizie: http://127.0.0.1:8000/notizie/")

if __name__ == '__main__':
    populate()