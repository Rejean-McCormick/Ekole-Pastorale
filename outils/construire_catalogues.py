#!/usr/bin/env python3
"""Catalogue éditorial de saints : projets de recherche, jamais des biographies certifiées."""
from pathlib import Path
import json
BASE=Path(__file__).resolve().parent.parent

def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
# A "witness" is not equivalent to a "doctor"; record virtues and evidence separately.
data=[
 ('François d’Assise',['pauvreté volontaire','fraternité','sollicitude envers la création'],'Testament; Règles; Cantique des créatures','Textes attribués au saint à distinguer des biographies hagiographiques postérieures','Pauvreté vécue librement ≠ misère subie'),
 ('Vincent de Paul',['service des pauvres','organisation de la charité','prudence'],'Correspondance; conférences conservées','Distinguer parole transcrite, organisation historique et réinterprétations modernes','Aide sans condition de pratique religieuse'),
 ('Marie de l’Incarnation',['persévérance','vie intérieure','éducation'],'Correspondance; Relations','Lire avec sources autochtones et étude de la colonisation','Ne pas idéaliser la mission coloniale'),
 ('Kateri Tekakwitha',['fidélité de conscience','courage','vie de prière'],'Biographies anciennes et traditions ecclésiales','Étudier les récits coloniaux et la voix des communautés autochtones','Ne pas parler au nom des peuples autochtones'),
 ('Marguerite Bourgeoys',['éducation','solidarité','vie communautaire'],'Archives historiques de la Congrégation de Notre-Dame','Distinguer actes documentés et idéalisation postérieure','Éducation et rapports coloniaux au Québec'),
 ('Marguerite d’Youville',['service des personnes vulnérables','gestion responsable','résilience'],'Archives et biographies des Sœurs grises','Vérifier les actes institutionnels et leurs interprétations','Hébergement et dignité des personnes aidées'),
 ('André Bessette',['humilité','accueil','persévérance'],'Témoignages et archives liées à l’Oratoire Saint-Joseph','Distinguer témoignages de guérison, dévotion et reconnaissance ecclésiale','Ne jamais promettre de guérison aux malades'),
 ('Thérèse de Lisieux',['confiance','charité quotidienne','persévérance'],'Manuscrits autobiographiques, correspondance','Écrits directs et éditions postérieures à contextualiser','Ne pas instrumentaliser l’humilité pour obtenir du travail gratuit'),
 ('Thérèse d’Avila',['discernement','courage','vie intérieure'],'Livre de la vie; Château intérieur','Étudier le genre autobiographique mystique et sa réception','L’accompagnement spirituel n’est pas un diagnostic clinique'),
 ('Catherine de Sienne',['franchise','courage','souci de l’unité'],'Lettres; Dialogue','Lettres attribuées, éditions et hagiographies distinctes','Critiquer sans couvrir les dysfonctionnements'),
 ('Ignace de Loyola',['discernement','service','examen de conscience'],'Exercices spirituels; récit du pèlerin','Distinguer textes fondateurs et usages modernes des exercices','Pas de coercition dans les retraites'),
 ('Joséphine Bakhita',['espérance','dignité humaine','résilience'],'Témoignages et biographies à documenter','Ne jamais convertir les traumatismes en spectacle édifiant','Consentement et prudence dans les récits de violence'),
 ('Martin de Porrès',['soin des malades','service','humilité'],'Biographies historiques à documenter','Enquêter sur le contexte social colonial et les sources de miracle','Respect des pratiques médicales'),
 ('Oscar Romero',['courage public','justice','solidarité'],'Homélies, lettres pastorales, archives contemporaines','Distinguer actes documentés, prises de position politiques et récits ultérieurs','Charité et justice sans parti pris imposé'),
 ('Charles de Foucauld',['fraternité','présence','simplicité'],'Correspondance et écrits spirituels','Lire les rapports interculturels du contexte colonial','Écouter les communautés locales plutôt que projeter sur elles'),
 ('François de Sales',['douceur','patience','accompagnement'],'Introduction à la vie dévote; correspondance','Distinguer direction spirituelle ancienne et bonnes pratiques contemporaines','Bannir l’emprise spirituelle'),
]
entries=[]
for idx,(nom,vertus,ecrits,risque,enjeu) in enumerate(data,1):
 entries.append({'id':f'temoin-candidat-{idx:03d}','nom':nom,'statut_documentaire':'candidat_a_documenter_et_revoir','reconnaissance_ecclesiale':'a_verifier_sur_source_officielle_avant_publication',
 'vertus_attribuees_pour_etude':vertus,'corpus_pistes':ecrits,'gradation_sources':['ecrits_directs','documents_contemporains','biographies_ulterieures','traditions_de_devotion'],
 'point_de_vigilance':risque,'usage_pastoral':enjeu,'miracles_attribues':'hors_de_la_fiche_des_vertus; consulter séparément la branche miracles avec statut des sources',
 'regle':'Ce projet de fiche ne certifie ni un miracle ni un fait biographique non sourcé.'})
save(BASE/'federation/saints-et-vertus-candidats.json',{'format':'pastorale.temoins-candidats/1.0','statut':'non_canonique_non_certifie','destination_future':'Kristal autonome des témoins, éventuellement un archétype distinct de ARK-20','fiches':entries})
print(len(entries),'fiches de témoins candidates')
