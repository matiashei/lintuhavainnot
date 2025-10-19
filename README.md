# Lintuhavainnot

## Sovelluksen toiminnot (tähdellä merkatut ovat vielä toteuttamatta)

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan lintuhavaintoja. Tämän lisäksi käyttäjä voi merkata sovellukseen paikan, jossa havainto on tehty, havaintopäivän ja kommenttina esimerkiksi havainnon varmuuden sekä lisäämään kuvia havainnostaan.
* Käyttäjä näkee sovellukseen lisätyt havainnot.
* Käyttäjä pystyy etsimään havaintoja hakusanalla lajin tai havaintopaikan perusteella.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät havainnot.
* Käyttäjä pystyy kommentoimaan havaintoja esimerkiksi tilanteessa, jossa havainto on epävarma ja toinen käyttäjä tarvitsee apua sen varmistamiseksi. Kommentit näytetään viiden ryhmissä.
* Havainnot listataan etusivulle 20 ryhmiin sivutettuina ensisijaisesti päivämäärän ja toissijaisesti havainnon id-numeron perusteella.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
```

Käynnistä sovellus:

```
$ flask run
```
