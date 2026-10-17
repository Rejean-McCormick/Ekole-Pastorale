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

Windows : double-cliquer `LANCER.bat` ou exécuter `LANCER.bat --verifier` depuis un terminal.

## Quel dépôt ?

- `ekole` : moteur neutre, indépendant du programme catholique.
- `ecole-pastorale` : dépôt de contenu pastoral (ce ZIP), incluant les Kristals v11 et leur projection compatible Core.
- `ekole-quebec` : autre dépôt de contenu sans lien avec le programme catholique.

## Mise à jour

Pour régénérer le contenu Ekole : `python3 outils/projeter_ekole.py`. Si un Kristal a été modifié, validez/reconstruisez auparavant son engagement v9. La projection écrase seulement les JSON dérivés connus à la racine, sans changer Ekole Core.

## Point de vigilance

Les tests historiques de la *vieille version* d'Ekole Core, notamment `tests/test_pastorale.py`, supposent encore 12 cours et 3 parcours du prototype. Ils doivent être révisés dans un cycle de maintenance distinct de Core avant de les utiliser pour qualifier le nouveau corpus. Le chargement `--verifier` teste quant à lui le manifeste 32/7 actuel.
