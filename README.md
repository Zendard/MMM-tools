# Markov
## Gebruik
```bash
python markov.py <trace_file.txt> [--length] [-n] [--specific n]
```

## Opties
- `trace_file.txt` Tracebestand om uit te lezen
- `--length` Maak een markovtabel van de pakketlengtes i.p.v. de pakketaantallen
- `-n` Normaliseer de rijen **niet**
- `--specific n` Beschouw `n` als 1 geval en alle andere waarden als een 2de geval

## Output
Markovtabel in `stdout`

# Graph
## Gebruik
```bash
python graph2.py [configuratie.xml]
```

## Opties
- `configuratie.xml` Configuratiebestand om uit te lezen. Bij afwezigheid van dit argument vraagt het programma om een bestandsnaam

## Output
Routerdiagram in `router_diagram.png`
