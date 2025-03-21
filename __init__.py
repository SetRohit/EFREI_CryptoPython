from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Page d'accueil

# Génération de la clé (ATTENTION : à fixer en prod pour éviter de perdre les données)
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Chiffre la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token sous forme de chaîne

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        token_bytes = token.encode()  # Conversion str -> bytes
        valeur_decryptee = f.decrypt(token_bytes)  # Décryptage
        return f"Valeur décryptée : {valeur_decryptee.decode()}"  # Retourne la valeur déchiffrée
        
    except Exception as e:
        return f"Erreur lors du déchiffrement : {str(e)}"

    if not encrypted_text:
        return jsonify({"error": "Aucune donnée chiffrée fournie"}), 400

    try:
        decrypted_text = f.decrypt(encrypted_text.encode()).decode()  # Déchiffre la valeur
        return jsonify({"decrypted_text": decrypted_text})  # Retourne la valeur déchiffrée
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
