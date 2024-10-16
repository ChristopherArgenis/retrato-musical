import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

class Consulta:
    def __init__(self, df):
        self.df = df

    def ft_year(self, select=None, year1=None, year2=None):
        self.year1, self.year2 = year1, year2
        self.select = select
        match self.select:
            case "Igual":
                self.df = self.df[self.df["Year"] == year1]
            case "Desde":
                self.df = self.df[(self.df["Year"] >= year1) & (self.df["Year"] <= year2)]
            case "Apartir":
                self.df = self.df[self.df["Year"] >= year1]

    def ft_artist(self, artist):
        self.artist = artist
        self.df = self.df[self.df["Artist"] == self.artist]

    def ft_genre(self, genre):
        self.genre = genre
        self.df = self.df[self.df["Genre"] == self.genre]

class proba:
    def __init__(self, df_Mod):
        self.dfM = df_Mod

    def proba_total(self, df):
        self.df = df
        self.proba = 0
        if len(self.dfM.df) < 150:
            self.proba = ((len(self.dfM.df)/len(self.df))*100)
            return f"{self.proba:.2f}% de Probabilidad"
        else:
            self.proba = int((len(self.dfM.df)/len(self.df))*100)
            return f"{self.proba}% de Probabilidad"
        
@app.route('/', methods=["GET", "POST"])
def main():
    # Lectura del csv y guardado en un objeto dataframe
    df = pd.read_csv("ClassicHit.csv")

    # Dataframe a partir de las columnas del csv
    Music_db = df[["Track", "Artist", "Year", "Genre", "Popularity"]]

    # Valores unicos de los años y ordenamiento
    years = Music_db["Year"].unique()
    years = list(years)
    years.sort()

    # Instancia de la clase Consulta para hacer una.
    query = Consulta(Music_db)
    probab = 0

    if request.method == "POST":
        artist = request.form['artist']
        genre = request.form['genre']
        parameter = request.form['select']
        year1 = int(request.form['year1'])
        year2 = int(request.form['year2'])

        if artist != "Select":
            query.ft_artist(artist)
        if genre != "Select":
            query.ft_genre(genre)
        
        match parameter:
            case "Select":
                pass
            case "Igual":
                query.ft_year(select="Igual", year1=year1)
            case "Apartir":
                query.ft_year(select="Apartir", year1=year1)
            case "Desde":
                query.ft_year(select="Desde", year1=year1, year2=year2)

        probabilidad = proba(query)
        probab = probabilidad.proba_total(Music_db)
        query.df.sort_values(by="Popularity", ascending=False, inplace=True)

    return render_template("Sitio_web.html", consulta=query, years=years, proba=probab)

if __name__ == '__main__':
    app.run()