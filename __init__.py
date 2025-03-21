from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Page d'accueil

# Clé fournie par l'utilisateur
key = b'A8oFDNA9XdjmkJ6xFP6HURxiZvjuYhVt--DdYQCovuw='
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        token_bytes = token.encode()  # Conversion str -> bytes
        valeur_decryptee = f.decrypt(token_bytes)  # Déchiffre la valeur
        return f"Valeur décryptée : {valeur_decryptee.decode()}"  # Retourne en str
        
    except Exception as e:
        return f"Erreur lors du déchiffrement : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
