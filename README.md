# DSA Helper Scripts

Helper Scripts for the Pen&Paper game "Das Schwarze Auge".

The scripts are designed to work in concert with the [Helden Software](https://www.helden-software.de/)

## Update DSA Sheet

Add the current characteristic values to the talent table

e.g. the talent table row
```
Athletik	|   (GE/KO/KK)    |	BEx2    |	7
```
is converted to
```
Athletik	|   ( GE[14] / KO[16] / KK[15] )    |	BEx2    |	7
```

### Usage


```bash
python3 -m update_dsa_sheet {CHARACTER_SHEET}
```

# ToDo
- add table with meta-talents described in "Wege des Schwerts"
