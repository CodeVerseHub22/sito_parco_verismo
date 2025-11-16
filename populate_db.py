#!/usr/bin/env python3
"""
Script per popolare il database con gli autori e le loro opere principali.
Esegui questo script con: python populate_db.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from parco_verismo.models import Autore, Opera

def populate():
    print("Popolamento del database in corso...")
    
    # Crea gli autori
    verga, created = Autore.objects.get_or_create(
        slug='giovanni-verga',
        defaults={'nome': 'Giovanni Verga'}
    )
    if created:
        print(f"✓ Creato autore: {verga.nome}")
    else:
        print(f"• Autore già esistente: {verga.nome}")
    
    capuana, created = Autore.objects.get_or_create(
        slug='luigi-capuana',
        defaults={'nome': 'Luigi Capuana'}
    )
    if created:
        print(f"✓ Creato autore: {capuana.nome}")
    else:
        print(f"• Autore già esistente: {capuana.nome}")
    
    print("\n" + "="*60)
    print("Aggiunta opere di Giovanni Verga")
    print("="*60)
    
    # Opere di Verga
    opere_verga = [
        {
            'titolo': 'I Malavoglia',
            'slug': 'i-malavoglia',
            'anno_pubblicazione': 1881,
            'trama': '''I Malavoglia è un romanzo corale che narra le vicende della famiglia Toscano, 
soprannominati "Malavoglia", poveri pescatori del paese di Aci Trezza. La storia si concentra sui 
tentativi di Padron 'Ntoni di mantenere unita la famiglia e di ripagare un debito contratto per 
l'acquisto di una partita di lupini destinata al commercio. Il naufragio della barca "Provvidenza", 
che trasportava i lupini, segna l'inizio di una serie di disgrazie che colpiranno la famiglia.''',
            'analisi': '''L'opera è considerata il capolavoro del Verismo italiano. Verga descrive 
con realismo la vita dei pescatori siciliani, le loro lotte contro la miseria e il destino. 
Il romanzo è caratterizzato dall'uso del discorso indiretto libero e da una lingua che riflette 
il parlato popolare siciliano. Tema centrale è il contrasto tra il mondo tradizionale, rappresentato 
da Padron 'Ntoni, e le aspirazioni di modernità dei giovani.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/I_Malavoglia'
        },
        {
            'titolo': 'Mastro-don Gesualdo',
            'slug': 'mastro-don-gesualdo',
            'anno_pubblicazione': 1889,
            'trama': '''Il romanzo racconta la storia di Gesualdo Motta, un muratore arricchito che 
cerca di elevarsi socialmente sposando una nobildonna decaduta, Bianca Trao. Nonostante la sua 
ricchezza, Gesualdo non viene mai accettato dalla nobiltà e viene disprezzato sia dai nobili che 
dal popolo. La sua vita è segnata dalla solitudine e dall'incomprensione, culminando in una morte 
solitaria e dolorosa, circondato dall'indifferenza di coloro che dovrebbero essergli vicini.''',
            'analisi': '''Secondo romanzo del ciclo dei "Vinti", Mastro-don Gesualdo rappresenta 
l'ascesa sociale impossibile e il tema dell'alienazione. Verga analizza la stratificazione sociale 
siciliana e l'impossibilità di superare le barriere di classe. Il protagonista è vittima delle 
sue stesse ambizioni e della società che lo respinge. L'opera è caratterizzata da una profonda 
analisi psicologica e da un pessimismo esistenziale.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Mastro-don_Gesualdo'
        },
        {
            'titolo': 'Vita dei campi',
            'slug': 'vita-dei-campi',
            'anno_pubblicazione': 1880,
            'trama': '''Raccolta di novelle che descrive la vita contadina siciliana con crudo 
realismo. Tra le novelle più famose vi sono "Rosso Malpelo", storia di un ragazzo dai capelli 
rossi maltrattato e sfruttato, "La Lupa", che narra l'ossessione amorosa di una donna, 
e "Cavalleria rusticana", dramma di gelosia e onore che ispirò la celebre opera lirica di Mascagni.''',
            'analisi': '''Vita dei campi segna l'inizio della stagione verista di Verga. Le novelle 
presentano personaggi umili schiacciati da un destino crudele, vittime delle leggi economiche e 
sociali. Lo stile è essenziale, privo di giudizi morali, con l'autore che si eclissa completamente 
dietro la narrazione. Emerge una visione pessimistica della vita, dove la lotta per la sopravvivenza 
è spietata.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1880)'
        },
        {
            'titolo': 'Novelle rusticane',
            'slug': 'novelle-rusticane',
            'anno_pubblicazione': 1883,
            'trama': '''Seconda raccolta di novelle veriste, che continua l'esplorazione del mondo 
contadino siciliano. Include storie come "La roba", che racconta l'ossessione per l'accumulo di 
ricchezze di Mazzarò, "Libertà", una cronaca della rivolta contadina di Bronte del 1860, 
e "Pane nero", storia di miseria e sfruttamento.''',
            'analisi': '''Le Novelle rusticane approfondiscono i temi di Vita dei campi, concentrandosi 
maggiormente sugli aspetti economici della vita rurale. Verga analizza l'ossessione per la proprietà, 
il conflitto tra ricchi e poveri, e le illusioni di riscatto sociale. Lo stile è ancora più 
asciutto e impersonale, con una rappresentazione cruda e oggettiva della realtà.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Novelle_rusticane'
        },
    ]
    
    for opera_data in opere_verga:
        opera, created = Opera.objects.get_or_create(
            slug=opera_data['slug'],
            defaults={
                'autore': verga,
                'anno_pubblicazione': opera_data['anno_pubblicazione'],
                'link_wikisource': opera_data['link_wikisource']
            }
        )
        if not created:
            opera.autore = verga
            opera.anno_pubblicazione = opera_data['anno_pubblicazione']
            opera.link_wikisource = opera_data['link_wikisource']
        opera.set_current_language('it')
        opera.titolo = opera_data['titolo']
        opera.trama = opera_data['trama']
        opera.analisi = opera_data['analisi']
        opera.save()
        if created:
            print(f"✓ Creata opera: {opera.titolo} ({opera.anno_pubblicazione})")
        else:
            print(f"• Opera aggiornata: {opera.titolo}")
    
    print("\n" + "="*60)
    print("Aggiunta opere di Luigi Capuana")
    print("="*60)
    
    # Opere di Capuana
    opere_capuana = [
        {
            'titolo': 'Il marchese di Roccaverdina',
            'slug': 'il-marchese-di-roccaverdina',
            'anno_pubblicazione': 1901,
            'trama': '''Il romanzo narra la storia del marchese di Roccaverdina, che dopo aver 
avuto una lunga relazione con la sua massaia Agrippina Solmo, decide di farla sposare con un 
suo servo, Rocco Criscione, per continuare a frequentarla senza scandalo. Tuttavia, tormentato 
dalla gelosia, il marchese uccide Rocco. Il senso di colpa lo perseguiterà fino alla follia, 
portandolo alla confessione e alla morte.''',
            'analisi': '''Capolavoro di Capuana, il romanzo rappresenta un'evoluzione del verismo 
verso l'analisi psicologica. L'autore esplora i tormenti della coscienza e il conflitto tra 
passione e ragione. La dimensione psicologica prevale su quella sociale, anticipando temi del 
decadentismo. Il marchese è un personaggio complesso, diviso tra il desiderio e il rimorso.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Il_marchese_di_Roccaverdina'
        },
        {
            'titolo': 'Giacinta',
            'slug': 'giacinta',
            'anno_pubblicazione': 1879,
            'trama': '''Giacinta è una giovane donna che, dopo essere stata violentata da bambina, 
sviluppa una personalità disturbata e cerca disperatamente l'amore e l'accettazione. Si sposa 
con Andrea, ma il matrimonio è tormentato dai suoi problemi psicologici. La storia esplora le 
conseguenze del trauma infantile sulla psiche e sulla vita adulta.''',
            'analisi': '''Giacinta è uno dei primi romanzi veristi italiani e uno dei primi a 
trattare apertamente temi come il trauma sessuale e le sue conseguenze psicologiche. Capuana 
utilizza il naturalismo per esplorare l'inconscio e le patologie mentali, anticipando gli 
sviluppi della psicologia moderna. L'opera fu considerata scandalosa per l'epoca.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Giacinta'
        },
        {
            'titolo': 'Profili di donne',
            'slug': 'profili-di-donne',
            'anno_pubblicazione': 1877,
            'trama': '''Raccolta di ritratti femminili che esplorano diversi tipi di donne e le 
loro vicende sentimentali. Capuana analizza con sensibilità psicologica i caratteri femminili, 
le loro passioni, i loro conflitti interiori e il loro rapporto con la società.''',
            'analisi': '''Quest'opera mostra l'interesse di Capuana per la psicologia femminile 
e il suo approccio analitico alla narrazione. I ritratti sono caratterizzati da un'attenzione 
particolare agli stati d'animo e alle motivazioni interiori, prefigurando l'evoluzione verso 
il romanzo psicologico.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Profili_di_donne'
        },
    ]
    
    for opera_data in opere_capuana:
        opera, created = Opera.objects.get_or_create(
            slug=opera_data['slug'],
            defaults={
                'autore': capuana,
                'anno_pubblicazione': opera_data['anno_pubblicazione'],
                'link_wikisource': opera_data['link_wikisource']
            }
        )
        if not created:
            opera.autore = capuana
            opera.anno_pubblicazione = opera_data['anno_pubblicazione']
            opera.link_wikisource = opera_data['link_wikisource']
        opera.set_current_language('it')
        opera.titolo = opera_data['titolo']
        opera.trama = opera_data['trama']
        opera.analisi = opera_data['analisi']
        opera.save()
        if created:
            print(f"✓ Creata opera: {opera.titolo} ({opera.anno_pubblicazione})")
        else:
            print(f"• Opera aggiornata: {opera.titolo}")
    
    print("\n" + "="*60)
    print("✓ Popolamento completato con successo!")
    print("="*60)
    print(f"\nTotale autori: {Autore.objects.count()}")
    print(f"Totale opere: {Opera.objects.count()}")
    print(f"  - Opere di Verga: {Opera.objects.filter(autore=verga).count()}")
    print(f"  - Opere di Capuana: {Opera.objects.filter(autore=capuana).count()}")
    print("\nPuoi ora avviare il server con:")
    print("  python manage.py runserver")
    print("\nE visitare:")
    print("  - Biblioteca: http://127.0.0.1:8000/biblioteca/")
    print("  - Opere di Verga: http://127.0.0.1:8000/opere/giovanni-verga/")
    print("  - Opere di Capuana: http://127.0.0.1:8000/opere/luigi-capuana/")

if __name__ == '__main__':
    populate()
