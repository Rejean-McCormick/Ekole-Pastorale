# Décisions techniques — ARK-20 / ARK-21 / Ekole

## D-01 : ni école monolithique, ni copie du vieux contenu Ekole-Québec

Ekole-Québec fournit un précédent de parcours et une interface, mais n'est pas traité comme norme Kristal v11. Le contenu est reconstruit en workspaces indépendants et signés par état logique v9.

## D-02 : séparation des responsabilités

La connaissance ne devient pas propriété d'une application. Chaque unité ARK-20 possède objectifs, activités, progression et évaluation; chaque dossier ARK-21 possède un schéma de témoignage et ses provenances; Catho conserve les corpus historiques; Ekole lit seulement la projection.

## D-03 : deux branches, une même identité catholique

Dans le canon, appartenance de branche = assertion KQ→KP→KQ. Le texte du libellé ne permet pas d'inférer la branche. Le projecteur vérifie assertion, namespace, profil, statut, et refuse les préalables franchissant les deux branches, sauf décision explicite future avec une nouvelle règle de curriculum. Les parcours facultatifs peuvent présenter les deux sans créer d'obligation transversale.

## D-04 : migration historique sans usurpation

A-Kristal-Catho fourni n'est pas encore v11. Le pont est **documentaire et adressé par hash** : empreintes SHA256 des 2 artefacts, noms et vrais identifiants historique des 38 docteurs et 138 références. Il n'en déduit ni KQ, ni Wikidata, ni relations de confiance, ni liens v9 résolus. Prochaine étape : nouveau Kristal Catho conforme v11, résolution source→source dans un registre d'équivalences revu.

## D-05 : les vues enseignants sont différentes des vues élèves

La projection élève ne contient pas les rubriques d'évaluation privées, les directives de sauvegarde internes ou les commentaires du formateur. Les démonstrations élève affichent une mise en garde « MAQUETTE NON APPROUVÉE » et ne sont pas une publication reconnue.

## D-06 : checks de build obligatoires

Projection = vérifier `check-v11`, `check`, identité locale, graphe, relation de branche, modules, durée, rubriques, garde-fous, dépendances, snapshot v9, engagements logiques et exactitude des payloads. Modifier `canon/domain/pedagogie/unite.json` exige révision, contrôle et nouveau build v9. Aucune correction implicite au canon.

## D-07 : les schémas éditoriaux sont candidats

`pastorale.unite-native/1.1-draft` et `pastorale.temoin-native/0.1-draft` ne sont ni la norme Framework v11 ni des standards universels pour toute école. ARK-20 est générique et sa déclinaison catholique n'impose pas son vocabulaire à d'autres écoles.
