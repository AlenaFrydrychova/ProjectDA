#celkové hodnocení restaurací, vynechává nuly, což je trochu problém :(
rest_rating = []
poradi = 1 #pocita poradi radku, ale vynechava radky, ktere neobsahuji "td", {"class": "hbg1"}

value_rating = 0
for line in table.find_all("td", {"class": "hbg1"}): #hledá v tabulce tagy td s classou hbg1 (tam je definovaná délka obrázku, který představuje hodnocení)
    if line != 0: #nefunguje, ideálně by se mělo spustit jen když v line tag td opravdu je a vypsat nulu, když není. Je třeba posunout podmínku nad cyklus a nějak jí přeformulovat?
        for rating in line.find_all("img"): #najde všechny tagy img v td s classou hbg1
            width = int(rating.get('width')) #hodnota width
            if width == 11: # 11 je maximální délka jedné kostičky hodnocení (za předpokladu, že není na konci -> ta má z nějakého důvodu 12)
                value_rating += width #hodnota do které se počítá rating jedné restaurace (celkový width obrázků)
                if width == 12: #pokud má 12 jedná se o poslední kosticku hodnoceni
                    value_rating += width #hodnota width
                    print(poradi, value_rating) #poradí je jen císlo řádku, když jsme to hledaly v tabulce na webu
                    value_rating = 0 #vymazání value rating, protože 12 má jen poslední kostička
                    poradi += 1
            elif width > 0 and width < 11: # kostička, která je na konci a není kompletní tzn je mezi 1 až 10
                value_rating += width #hodnota width
                print(poradi, value_rating)
                value_rating = 0 #vymazani hodnoty
                poradi += 1
    else: #nefunguje
        value_rating = 0
        print(value_rating)
