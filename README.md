# Lintuhavainnot

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan lintuhavaintoja. Tämän lisäksi käyttäjä voi merkata sovellukseen paikan, jossa havainto on tehty, havaintopäivän ja havainnon varmuuden sekä lisäämään kuvia havainnostaan.
* Ylläpitäjä pystyy poistamaan ja muokkaamaan kenen tahansa käyttäjän sovellukseen lisäämiä havaintoja.
* Käyttäjä näkee sovellukseen lisätyt havainnot.
* Käyttäjä pystyy etsimään havaintoja hakusanalla lajin tai havaintopaikan perusteella.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät havainnot.
* Käyttäjä pystyy kommentoimaan havaintoja esimerkiksi tilanteessa, jossa havainto on epävarma ja toinen käyttäjä tarvitsee apua sen varmistamiseksi.

* ## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
