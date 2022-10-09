from tabnanny import check
import unittest
import questions


class TestTExams(unittest.TestCase):
    def test_normal(self):
        exam = questions.Exam.create_new(
            "https://newsroom.nvon.nl/files/default/skv132vb.pdf", "vwo", 2013, 2)
        exam.find_questions()

        check_questions = [
            'Geef de evenwichtsvoorwaar de voor dit evenwicht.',
            'Leg uit of in rivierwater de [CH3HgCl]  ook 1,5 ·105 keer zo groot is als de \n[CH3Hg+] of dat dit kleiner is of nog groter.',
            'Bereken hoeveel mg Hg per liter aanwezig was in het zeewater waarin de \nvissen hebben geleefd. Ga ervan uit dat BCF = 8,4·103. Gebruik een \ngegeven uit Binas-tabel 11.',
            'Geef met behulp van structuurformu les de vergelijking van de reactie \ntussen een molecuul methylkwikchloride en het eiwitfragment  \n~ Leu – Cys ~.',
            'Leg uit waarom het enzym na deze reac tie zijn werking niet meer kan \nuitvoeren.',
            'Geef de reactievergelijking voor de vorming van \nkalksteen, zoals die tijdens het ui tharden van een fresco plaatsvindt.',
            'Laat door middel van een berekening zien dat het volume van het gips \ngroter is dan het volume van het  kalksteen waaruit het is ontstaan. \nGebruik Binas-tabel 10. Neem aan dat  calciet voor kalksteen staat.',
            'Geef van deze redoxreactie de ver gelijkingen van de beide halfreacties en \nleid daarmee de totale reactieverge lijking af. In de vergelijking van de \nhalfreactie van de omzetting van hem atiet tot magnetiet komen ook H2O \nen H+ voor.',
            'Verklaar aan de hand van deze reac tievergelijking dat de vorming van \nmagnetiet het afbrokkelen v an een fresco nog verergert.',
            'Teken de structuurformule van een deel uit het midden van de keten van \nhet copolymeer acryloid B72. Verwerk in deze structuurformule van beide \nmonomeren twee eenheden.',
            'Geef, aan de hand van een reactieverge lijking, een mogelijke verklaring \nvoor het feit dat bariumhydroxide de hoeveelheid gips kan doen \nverminderen en verklaar aan de hand van deze reactievergelijking dat de \nhoeveelheid kalksteen kan toenemen. Gebruik in je verklaring ook \ngegevens uit Binas.',
            'Geef een reactievergelijking voor dit evenwicht.',
            'Leg uit waarom de twee beschreven methoden de ligging van het \nevenwicht in de richting van de ammoniak verschuiven.',
            'Leg uit waarom extra CO2 inbreng tot meer scaling leidt.',
            'Bereken de pH van een ammoniumsulfaatoplossing met 80 g N per liter. \nLaat de invloed van de sulfaationen op de pH buiten beschouwing.',
            'Geef de naam van een eigenschap van de oplossing die men kan meten \nen geef aan hoe men met behulp van die eigenschap nagaat of de \nammoniumsulfaatoplossing die ui t reactor 3 komt inderdaad 80 g N per \nliter bevat.',
            'Completeer het blokschema op de uitwerkbijlage door de ontbrekende \nstofstromen zo in het blokschema te  tekenen dat het schema het proces \nna de opstartfase weergeeft. Vermeld bij die zelfgetekende stofstromen \nde naam (namen) van de stof(fen) die daarbij hoort (horen) of een \nomschrijving van de stofstroom. \nLaat in het schema ook zien of de st of(fen) onderin of bovenin de reactor \nwordt (worden) ingevoerd.',
            'Geef de volledige re actievergelijking.',
            'Bereken hoeveel m3 15 M zwavelzuur minstens nodig is om alle \nammoniak, die kan ontstaan uit de 120 m3 te behandelen mest, om te \nzetten tot opgelost ammoniumsulf aat. Ga ervan uit dat van de \nstandaardoplossingen en van oplo ssing P de dichtheid 1,0 g mL–1 is.',
            'Geef de naam van een aminozuur waarmee een C12H25SO4– ion een \nionbinding kan vormen. Li cht je antwoord toe.',
            'Bereken hoeveel gram SDS nodig is om  1,0 gram eiwit te denatureren. Ga \nervan uit dat de gemiddelde massa van een aminozuureenheid in een \neiwitmolecuul 112 u is.',
            'Geef de structuurformule van stof A.',
            'Leg uit of DTT de secundaire of de tertiaire structuur van het eiwit \nverbreekt.',
            'Laat met behulp van een berekening zien of  zo’n overlap ook voorkomt bij \nhet HIV-virus. Ga ervan uit dat de gemiddelde massa van een \naminozuureenheid in een eiwitmolecuul 112 u is.',
            'Geef de vergelijkingen van de beide halfreacties en de totale \nreactievergelijking voor de omzetting van TMB tot het blauwe \nreactieproduct. Gebruik molecuulformu les. In de vergelijking van de \nhalfreactie van TMB komt onder andere ook H+ voor.',
            'Geef een reden waarom deze twee c ontrolemonsters worden getest.'
        ]

        for number in range(len(exam.questions)):
            question = exam.questions[number]
            self.assertEqual(number + 1, question.number)
            self.assertEqual(check_questions[number], question.question)


if __name__ == '__main__':
    unittest.main()
