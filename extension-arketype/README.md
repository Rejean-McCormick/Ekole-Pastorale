# Deux extensions candidates à Arketype 1.5 — non normatives

- **ARK-20** (`unite-formation-federee`) : programme pédagogique réutilisable, branché à Ekole par une projection dérivée.
- **ARK-21** (`temoin-vertus-sources`) : dossier de saint ou de témoin, sources et statuts probatoires séparés.

Les répertoires `overlay/modeles/` sont **des templates v11 vides** et n'inventent aucune entité KQ, propriété KP ou doctrine officielle. Un exemple *rempli* de chaque type se trouve à la racine de la livraison.

Installer dans une **copie contrôlée** d'Arketype 1.5 :

```sh
python installer_deux_archetypes.py --arketype /CHEMIN/arketype --dry-run
python installer_deux_archetypes.py --arketype /CHEMIN/arketype
python /CHEMIN/arketype/arketype.py show temoin-vertus-sources
python /CHEMIN/arketype/arketype.py create --type temoin-vertus-sources --slug saint-pilote --title "Saint pilote" --parent /CHEMIN/DOSSIER_EXISTANT --authoring v11
```

Le dossier parent `--parent` doit déjà exister. L'ancien `installer_extension.py` a été conservé pour compatibilité avec le premier paquet ARK-20, mais **ne pose qu'ARK-20**. Pour installer les deux types, utiliser exclusivement `installer_deux_archetypes.py`.

L'installateur refuse les collisions et remet les inventaires à leur état d'origine en cas d'erreur. Il ne répare pas les défauts préexistants de l'archive Arketype fournie. Les nouveaux types demeurent candidats jusqu'à validation de la bibliothèque complète et admission formelle.
