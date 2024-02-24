from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Automata:
    def __init__(self, grammar, predict_table):
        self.grammar = grammar
        self.predict_table = predict_table

    def iniciar(self, cadena):
        pila = ['$']
        pila.append('S')
        counter = 0
        registros = []

        while True:
            X = pila[-1]
            if counter < len(cadena):
                a = cadena[counter]
            else:
                a = '$'

            if a == '$':
                if X == '$':
                    pila.pop()
                    return True
                else:
                    return False

            if X in self.grammar.terminals:
                if X == a:
                    pila.pop()
                    counter += 1
                else:
                    return False
            else:
                if X == 'RA' and a == ';':
                    pila.pop()
                    continue
                if a.isalpha() and a not in ['automata', 'alfabeto', 'aceptacion', 'fin', ':', ',', ';', 'epsilon']:
                    if a in self.predict_table.table['SM'].get('a-z'):
                        pila.pop()
                        counter += 1
                        continue
                    else:
                        return False
                elif a.isdigit():
                    if a in self.predict_table.table['SM'].get('0-9'):
                        pila.pop()
                        counter += 1
                        continue
                    else:
                        return False

                produccion = self.predict_table.table[X].get(a)
                if produccion is None:
                    return False
                else:
                    pila.pop()
                    for symbol in reversed(produccion):
                        pila.append(symbol)
        return False

    def resultado(self, cadena):
        return self.iniciar(cadena)

class Gramatica:
    def __init__(self):
        self.terminals = {'automata', 'alfabeto', 'aceptacion', 'fin', ':', ',', ';', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'epsilon'}
        self.non_terminals = {'S', 'A', 'B', 'V', 'AL', 'G', 'SM', 'RA', 'F', 'C', 'D'}

class AnalysisTable:
    def __init__(self):
        self.table = {
            'S': {
                'automata': ['A', 'B', 'V'],
                'alfabeto': None,
                'aceptacion': None,
                'fin': None,
                ':': None,
                ',': None,
                ';': None,
                'a-z': None,
                '0-9': None
            },
            'A': {
                'automata': ['automata'],
                'alfabeto': None,
                'aceptacion': None,
                'fin': None,
                ':': None,
                ',': None,
                ';': None,
                'a-z': None,
                '0-9': None
            },
            'V': {
                'automata': None,
                'alfabeto': None,
                'aceptacion': None,
                'fin': ['fin'],
                ':': None,
                ',': None,
                ';': None,
                'a-z': None,
                '0-9': None
            },
            'B': {
                'automata': None,
                'alfabeto': ['AL', 'F'],
                'aceptacion': None,
                'fin': ['F'],
                ':': None,
                ',': None,
                ';': None,
                'a-z': None,
                '0-9': None
            },
            'AL': {
                'automata': None,
                'alfabeto': ['G', ':', 'SM', 'RA', ';'],
                'aceptacion': None,
                'fin': None,
                ':': None,
                ',': None,
                ';': None,
                'a-z': None,
                '0-9': None
            },
            'G': {
                'automata': None,
                'alfabeto': ['alfabeto'],
                'aceptacion': None,
                'fin': None,
                ':': None,
                ',': None,
                ';': None,
                'a-z': None,
                '0-9': None
            },
            'SM': {
                'automata': None,
                'alfabeto': None,
                'aceptacion': None,
                'fin': None,
                ':': None,
                ',': None,
                ';': None,
                'a-z': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
                '0-9': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            },
            'RA': {
                'automata': None,
                'alfabeto': None,
                'aceptacion': None,
                'fin': None,
                ':': None,
                ',': [',', 'SM', 'RA'],
                'a-z': None,
                '0-9': None
            },
            'F': {
                'automata': None,
                'alfabeto': None,
                'aceptacion': ['C', ':', 'D', ';'],
                'fin': None,
                ':': None,
                ',': None,
                ';': None,
                'a-z': None,
                '0-9': None
            },
            'C': {
                'automata': None,
                'alfabeto': None,
                'aceptacion': ['aceptacion'],
                'fin': None,
                ':': None,
                ',': None,
                ';': None,
                'a-z': None,
                '0-9': None
            },
            'D': {
                'automata': None,
                'alfabeto': None,
                'aceptacion': ['aceptacion'],
                'fin': None,
                ':': None,
                ',': None,
                ';': None,
                'a-z': None,
                '0-9': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            }
        }

@app.route('/verificar', methods=['POST'])
def verificar_cadena():
    data = request.json
    cadena = data.get('cadena').split()
    print(cadena)
    
    grammar = Gramatica()
    predict_table = AnalysisTable()
    automata = Automata(grammar, predict_table)
    
    resultado = automata.resultado(cadena)
    cadena_enviar_front = 'invalido'
    if resultado:
        cadena_enviar_front = 'valido'
    
    print(cadena_enviar_front)

    return jsonify({'resultado': cadena_enviar_front})

if __name__ == '__main__':
    app.run(debug=True)
