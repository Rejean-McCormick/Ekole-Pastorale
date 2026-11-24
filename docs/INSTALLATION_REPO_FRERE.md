# Installation du dépôt frère

## Structure attendue

Placez `ekole/` et `ecole-pastorale/` sous le même dossier parent. Ekole Core fourni découvre automatiquement `ecole-pastorale` si aucune autre école n'est présente; si `ekole-quebec/` est aussi présent, **choisissez le contenu explicitement**.

## Commandes sûres

```bash
cd ecole-pastorale
python3 ../ekole/launcher.py --contenu . --verifier
./lancer.sh --verifier
./lancer.sh
```

Windows : double-cliquer `LANCER_PASTORALE.bat` ou exécuter `LANCER_PASTORALE.bat --verifier` depuis un terminal. `LANCER.bat` n'est pas présent dans ce dépôt.

## Quel dépôt ?

- `ekole` : moteur neutre, indépendant du programme catholique.
- `ecole-pastorale` : dépôt de contenu pastoral (ce ZIP), incluant les Kristals v11 et leur projection compatible Core.
- `ekole-quebec` : autre dépôt de contenu sans lien avec le programme catholique.

## Mise à jour

Pour régénérer le contenu Ekole, reconstruire et vérifier d'abord les engagements v9 locaux, puis exécuter le projecteur :

```bash
python outils/rebuild_local_candidates.py --build
python outils/rebuild_local_candidates.py
python outils/projeter_ekole.py
python -m unittest discover -s tests -v
```

La reconstruction v9 est nécessaire lorsqu'on part d'un snapshot qui exclut les sorties `build/v9/`. Ces commandes ne publient pas les contenus. Le projecteur lit les thèmes visuels depuis `curriculum/visuels-themes.json`, préserve les 12 styles dans `pack.json` et écrit uniquement les JSON dérivés, sans modifier Ekole Core ni les sources canoniques. Sur Windows, utiliser `python` ou `py -3` selon l'installation.

## Point de vigilance

Le test `tests/test_pastorale.py` est une **compatibilité permissive** avec le vrai dépôt frère Ekole Core (au moins 12 cours et 3 parcours) ; il n'établit pas à lui seul la conformité stricte du corpus 32/7. `tests/test_depot_frere.py` vérifie précisément les 32 cours, les 7 parcours et la reproductibilité de la projection. Sans le vrai dépôt frère, le test d'intégration est ignoré, et non validé. Le chargement `demarrer_pastorale.py --verifier` est un contrôle distinct de compatibilité avec le Core local. Voir [Tests et validation](TESTING_AND_VALIDATION.md).
