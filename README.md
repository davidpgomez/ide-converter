# i-DE converter

A small Python script to transform the CSV that can be obtained from
i-DE customers area to the format accepted by [CNMC Facturaluz](https://comparador.cnmc.gob.es/facturaluz) 
simulator.

## Formats
The CSV for billed power consumption complies with the expected (and accepted)
format of CNMC Facturaluz, but current (and not billed) consumption generated
CSV has a different format:

```csv
CUPS;FECHA-HORA;INV / VER;CONSUMO Wh;GENERACION Wh;
ES0987543210987654ZF;2021/06/01 00:00;1;51;0;
ES0987543210987654ZF;2021/06/01 01:00;1;62;0;
ES0987543210987654ZF;2021/06/01 02:00;1;120;0;
ES0987543210987654ZF;2021/06/01 03:00;1;96;0;
...
```

the expected one must look like this

```csv
ES0987543210987654ZF;31/05/2021;24;0.051
ES0987543210987654ZF;01/06/2021;01;0.062
ES0987543210987654ZF;01/06/2021;02;0.120
ES0987543210987654ZF;01/06/2021;02;0.096

```

As you can see, date format and consumption (from Wh to kWh) changes. Also notice that consumed power from 00:00 of a certain day D should be treated
as consumed power from 24:00 h for D-1 day.

## Usage

Just execute it in your terminal:

```bash
python3 ide-converter --file download_from_ide.csv --output /data/result.csv
```

The resulting CSV can be directly upload to [CNMC Facturaluz](https://comparador.cnmc.gob.es/facturaluz).
