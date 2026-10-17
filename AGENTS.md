# Règles pour contribuer au dépôt ecole-pastorale

1. Ekole Core est un moteur neutre externe à ce dépôt. Ne pas copier/modifier `../ekole` lors d'un travail sur les cours.
2. Les Kristals Framework v11 sont les sources canoniques des unités; `pack.json`, `cours/`, `publications/eleve/` sont des dérivés. Reprojeter plutôt que modifier directement les JSON dérivés.
3. Les deux branches (Message / Miracles et mystères) sont distinctes dans les préalables; toute exception demande une décision explicite et revue doctrinale.
4. Toute assertion de fait, interprétation historique ou fait hagiographique doit posséder une provenance traçable; distinguer doctrine, lecture exégétique, pratique, tradition et miracle attribué.
5. Ne jamais présenter les cours comme approuvés/publieux : la revue théologique, la validation des sources et la protection pastorale restent nécessaires.
6. Après modification d'un canon, exécuter contrôle v11, contrôle général et rebuild v9 du Kristal ciblé, puis `python3 outils/projeter_ekole.py` et la suite de tests.
7. `extension-arketype/` demeure une contribution candidate à Arketype; elle n'est pas une dépendance runtime d'Ekole.
