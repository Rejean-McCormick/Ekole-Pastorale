# École pastorale catholique — Kristal Framework v11 → Ekole (v0.3)

**Statut : maquette d'ingénierie pédagogique et technique, locale, non publiée et non approuvée par l'autorité ecclésiastique.**

Cette refonte répond à une orientation précise : une **école authentiquement catholique**, ancrée dans Jésus et dans toute la Tradition (Écritures, Pères, docteurs, saints, doctrine sociale), qui enseigne **en deux branches pédagogiques indépendantes** :

1. **Message et tradition vivante** : amour, pardon, partage, pauvreté, justice, vie intérieure, docteurs, saints, vertus, pastorale active.
2. **Miracles et mystères de la foi** : signes évangéliques, guérisons, conception virginale, résurrection du Christ, phénomènes attribués aux saints, discernement et sacrements.

Les miracles **restent reçus et présentés comme tels dans la foi catholique**. La première branche **n'exige pas d'y adhérer préalablement** pour étudier les enseignements de Jésus ou des saints. La deuxième ne réduit pas les signes à des métaphores. Les deux relèvent d'une même tradition.

## Inventaire réalisé

| Brique | Réalisation | Statut |
|---|---|---|
| ARK-20 | **Unité de formation fédérée** : objectif, sources, séquence, cas, activité, preuve d'apprentissage, protection, projection Ekole | Archétype candidat Arketype 1.5, template vide et v11 |
| ARK-21 | **Témoin, vertus et attestations** : œuvres, gestes, vertus, tradition hagiographique, miracles attribués séparément | Deuxième archétype candidat, template vide et v11 |
| Kristals pédagogiques | **32 Kristals autonomes** Framework 11.0.0-draft.3, lexique fr-CA et états v9 | 20 message + 12 miracles, unités développées mais non homologuées |
| Exemple de saint | **1 Kristal témoin** v11 : François d'Assise, distinct du cours Ekole | Prototype documentaire, sources primaires à collationner |
| Saints supplémentaires | **16 fiches candidates** (vertus, corpus, risques de lecture) | Catalogue d'authoring non canonique |
| Pont Catho | **38 docteurs et 138 sources** relevés dans A-Kristal-Catho historique, avec SHA256 des artefacts réels | Pont documentaire vérifiable, **pas migration v11** |
| Projection Ekole | **32 cours et 7 parcours**, vues enseignants/élèves distinctes et blocage de publication | Compatible Ekole `ekole.content-pack/0.1` sans changer Core |
| Qualité | Contrat JSON Schema 2020-12, contrôles de graphes/états v9, préalables, rubriques et tests | Validation technique uniquement |

**Volume de formation indicatif : 99 heures**, si toutes les unités sont réalisées (62 h branche message, 37 h branche miracles). Les parcours sont des itinéraires sélectifs : il n'est pas nécessaire de suivre toutes les unités. Il s'agit d'une estimation de conception, non d'un programme crédité.

## Architecture : propriété et projection

```text
  A-Kristal-Catho historique (NE PAS REBASTIR PAR REMAPPAGE DE NOMS)
    ├─ Corpus doctrinal / Écritures / auteurs / sources
    ├─ 38 docteurs dans personnes-reconnaissances.json
    └─ Source refs et assertions documentées
            |      références documentaires + SHA256 exacts
            v      (pas d'équivalence automatique KQ/KP)
  federation/catho-legacy-bridge.json
            |
            |    corpus des témoins et vertus (propriété distincte)
            +--------- Kristal ARK-21 François d'Assise
            |             ├─ écrits / attestations / vertus
            |             └─ récits extraordinaires séparés
            |
  kristals/* : 32 unités ARK-20 conformes au profil v11
    ├─ canon/domain/v11/{graph,registry,crosswalk,dictionaries}
    ├─ canon/domain/pedagogie/unite.json  ← SEULE SOURCE DE VÉRITÉ DU COURS
    ├─ build/v9 : engagements logiques de l'état exact
    └─ design : liens externes CANDIDATS (non résolus)
            |
            v
  outils/projeter_ekole.py (lecture stricte, aucun write dans les Kristals)
            |
            v
  export-ekole/{pack.json,cours/,publications/eleve/,provenance-derivation.json}
            |
            v
  Ekole Core inchangé, démarrage local avec --contenu
```

### Pourquoi deux archétypes ?

- `ARK-20` **possède le cours** : progression, méthode, exercices, critères et préalables. Un cours ne devient pas propriétaire des écrits d'Augustin ni de l'histoire de François d'Assise.
- `ARK-21` **possède le dossier structuré sur un témoin** : inventaire d'écrits, vertus et actes attribués, nature et qualité des sources; il ne décerne ni titres ecclésiastiques ni authentifications de miracles.
- **Catho** demeure le propriétaire du corpus historique qu'on a déjà. Les relations vers ses données seront homologuées au moment d'une future migration v11, avec identités *namespacées* et états logiques épinglés.

**Important :** des identifiants comme `KQ1001` ne valent *qu'à l'intérieur de leur namespace v11*. Une égalité de libellé ne prouve jamais deux identités équivalentes.

## Arborescence à connaître

- `extension-arketype/overlay/` : les 2 types et leurs 2 templates **vides**, conçus pour Arketype 1.5.
- `extension-arketype/installer_deux_archetypes.py` : installation transactionnelle des 2 archétypes.
- `kristals/<unité>` : 32 Kristals de cours, leurs données canoniques, identités v11 et engagements d'état v9.
- `kristals-temoins/francois-assise` : exemple de nouveau propriétaire d'un dossier de saint.
- `curriculum/cours-index.json` : **index dérivé** et vérifié du curriculum; ce n'est pas l'autorité sur les cours.
- `federation/saints-et-vertus-candidats.json` : 16 pistes d'authoring, non intégrées automatiquement au canon.
- `federation/catho-legacy-bridge.json` : empreintes exactes, 38 docteurs et 138 refs; sans prétention de résolution v11.
- `outils/auditer_catho.py` : vérification en lecture seule de ce pont contre le dossier Catho fourni.
- `outils/projeter_ekole.py` : projection avec contrôles et provenance; refuse les états modifiés sans rebuild.
- `export-ekole` : cours enseignants, vues apprenants de démonstration et 7 parcours.
- `contracts/` : contrat éditorial 1.1 expérimental; **non** normatif pour Framework v11.
- `docs/` : note d'architecture, curriculum, règles de gouvernance et vérifications.

## Pour regarder immédiatement dans Ekole

Pré-requis : Python 3.10+ et le **Core Ekole** que vous avez fourni (ou une version compatible avec `ekole.content-pack/0.1`).

```sh
python /CHEMIN/ekole/launcher.py --contenu /CHEMIN/Pastorale_Kristal_v11_Ekole_v03/export-ekole --verifier
python /CHEMIN/ekole/launcher.py --contenu /CHEMIN/Pastorale_Kristal_v11_Ekole_v03/export-ekole
```

La projection dans `export-ekole` est déjà incluse. Par défaut **elle reste locale, non publiée, non certifiée**; la vue apprenant affiche un avertissement de maquette. Les rubriques d'évaluation et les contrôles de sauvegarde sont conservés dans les fichiers enseignants, pas dans les fichiers apprenants.

## Reconstruire la projection après une correction

Quand un cours est édité dans `canon/domain/pedagogie/unite.json`, le projecteur **refusera** son nouveau contenu tant que son état v9 n'aura pas été reconstruit. Vérifier préalablement la cohérence doctrinale, pédagogique et les sources :

```sh
python kristals/lire-bible/tools/kristal.py check-v11 kristals/lire-bible
python kristals/lire-bible/tools/kristal.py check kristals/lire-bible
python kristals/lire-bible/tools/kristal.py build-v9 kristals/lire-bible
python outils/projeter_ekole.py --sortie export-ekole
python /CHEMIN/ekole/launcher.py --contenu export-ekole --verifier
```

Le script `projeter_ekole.py` lance `check-v11` et `check` dans chaque Kristal, vérifie l'état logique v9 et compare chaque fichier canonique au payload de build avant d'exporter. L'option `--sans-preflight` n'est réservée qu'aux tests rapides et **ne supprime pas la comparaison exacte avec les artefacts de build**.

## Ajouter les deux archétypes à une copie d'Arketype 1.5

```sh
python extension-arketype/installer_deux_archetypes.py --arketype /CHEMIN/arketype --dry-run
python extension-arketype/installer_deux_archetypes.py --arketype /CHEMIN/arketype
python /CHEMIN/arketype/arketype.py show unite-formation-federee
python /CHEMIN/arketype/arketype.py show temoin-vertus-sources
python /CHEMIN/arketype/arketype.py create --type temoin-vertus-sources --slug exemple-nouveau-saint --title "Témoin" --parent /CHEMIN/kristals --authoring v11
```

L'installateur n'écrase aucun type existant et restaure les fichiers d'inventaire si une étape échoue. Les types ajoutés sont des **candidats**. L'Arketype 1.5 fourni présentait déjà des anomalies de validation globale (reçus v9 de certains modèles, logo manquant, fichier de modèle), ce que l'extension **ne répare pas silencieusement**. Une validation de l'hôte complet devra être effectuée après sa propre remise en état. Le Kit intégré à Arketype est draft.1; les instances livrées ont été construites avec le Kit draft.2.

## Audit des références historiques

En ayant accès au dossier extrait de `A-Kristal-Catho (5).zip` :

```sh
python outils/auditer_catho.py --catho /CHEMIN/A-Kristal-Catho
```

Cet audit doit retrouver les deux empreintes SHA256 exactes des artefacts, 38 identifiants de docteurs et 138 identifiants de sources. **Il ne télécharge rien** et ne confond jamais une correspondance textuelle avec une relation inter-Kristal autorisée. Si le Kristal Catho change, le pont devra être renégocié; il ne faut pas contourner le contrôle.

## Tester

```sh
python -m unittest discover -s tests -v
# Vérification facultative des contrats expérimentaux :
python -m pip install jsonschema
python /CHEMIN/ekole/launcher.py --contenu export-ekole --verifier
```

Le groupe de tests vérifie les 32 namespaces locaux et les branches, la validité des payloads selon le schéma, les préalables acycliques sans obligation entre branches, la somme des rubriques, les protections, les vues élèves, les engagements v9 et le Kristal de saint pilote.

## Limites obligatoires avant tout déploiement public

1. **La fidélité doctrinale n'a pas été approuvée** : consulter une autorité catholique compétente, des personnes formées en exégèse et, selon le type de formation, des responsables diocésains.
2. **Les sources restent des cibles éditoriales** : 138 références réelles existent dans Catho, mais aucune bibliothèque complète de textes sous licence n'a été transférée. Les notices bibliographiques et les traductions doivent être vérifiées avant publication.
3. **Le Kristal des saints est pilote** : la fiche François distingue vertus, écrits, traditions et miracles; ses éditions, documents et déclarations officielles restent à corroborer. Les 16 autres fiches sont des *candidates*, pas des biographies attestées.
4. **La protection des personnes est prioritaire** : aucune promesse de guérison, aucune coercition religieuse, aucune pression sur les victimes, respect des soins, procédures de signalement du Québec à confirmer pour le terrain.
5. **L'intégration est au niveau du paquet Ekole 0.1** : elle n'inclut pas encore les anciennes interfaces visuelles complexes, la synchronisation temps réel, un LMS ou une interface apprenant moderne générée séparément.
6. **Aucune migration de Catho vers v11 n'a été simulée**. Le pont de hash documentaire permet une mise en relation prudente, sans invention d'identités ou d'approbation de crosswalk.

En bref : **Catho fournit le patrimoine; ARK-21 qualifie les témoins; ARK-20 transforme ce savoir en cours; Ekole rend les parcours accessibles.** Chaque couche conserve sa propre responsabilité.
