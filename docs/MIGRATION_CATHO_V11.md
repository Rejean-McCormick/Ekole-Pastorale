# Projet de migration contrôlée du patrimoine A-Kristal-Catho vers Framework v11

## Ce qui existe à ce stade

Les deux artefacts historiques suivants ont été identifiés et adressés **par empreintes exactes** dans `federation/catho-legacy-bridge.json` : `canon/domain/personnes-reconnaissances.json` et `knowledge-base/corpus/corpus-chretien.semantic.json`. Le premier contient 38 docteurs reconnus dans la taxonomie donnée. Le second contient 138 références documentaires. Les assertions bibliques, théologiques, et les titres d'auteurs font partie de ce corpus historique, qui n'est **pas** un graphe v11 natif. Les ressemblances textuelles ne valent pas approbation d'identité.

## Processus recommandé, sans migration destructive

**Phase 1 — Inventaire** : classer les artefacts existants, états, sources, licences et statuts historiques. Garder les octets d'origine et leurs SHA256 comme reçus immuables.

**Phase 2 — Définir les propriétaires** : séparer le patrimoine des textes, l'index des personnes et œuvres, les dossiers de saints et les séquences pédagogiques. Une école ne possède pas automatiquement toutes ces connaissances.

**Phase 3 — Nouveaux namespaces** : générer les KQ/KP/KA/KS v11 à partir des entités réellement relues. Les chaînes historiques telles que `urn:kristal:catho:personne:*` sont conservées comme références historiques, jamais renumérotées ni prises pour des KQ valables.

**Phase 4 — Table de correspondances révisée** : enregistrer l'ancienne référence, la nouvelle identité locale, le type de relation, sa preuve, le réviseur, la date et le statut. Autoriser les statuts *non résolu*, *candidat*, *confirmé*, *rejeté*; aucun texte de libellé ne déclenche une relation confirmée.

**Phase 5 — Test de cohérence** : check-v11, validation Framework, contrôle du catalogue linguistique, couverture des assertions et comparaison des engagements d'état. Pour les saints, distinguer l'écrit authentifié et le récit hagiographique.

**Phase 6 — Actualiser les liens pédagogiques** : seules des références vers des états connus (state_ref, logical State Commitment et identifiants namespacés) peuvent alimenter des cours par l'interface fédérée. La provenance doit être exportée avec le cours et une nouvelle décision est nécessaire lors de l'évolution d'une source.

L'audit actuel `auditer_catho.py` n'effectue **que la phase 1 pour deux artefacts** : il ne doit jamais être présenté comme une migration finale.
