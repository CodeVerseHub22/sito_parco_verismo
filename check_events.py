from parco_verismo.models import Autore
autori = Autore.objects.all()
for a in autori:
    print(a.nome, a.slug)