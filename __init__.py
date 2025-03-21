from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Bienvenue sur l'application de chiffrement/déchiffrement"

@app.route('/encrypt/<string:key>/<string:valeur>')
def encryptage(key, valeur):
    try:
        f = Fernet(key.encode())  # Création d'un objet Fernet avec la clé fournie
        valeur_bytes = valeur.encode()  # Conversion str -> bytes
        token = f.encrypt(valeur_bytes)  # Chiffre la valeur
        return jsonify({"encrypted_text": token.decode()})  # Retourne la valeur chiffrée
    except Exception as e:
        return jsonify({"error": f"Clé invalide : {str(e)}"}), 400

@app.route('/decrypt/<string:key>/<string:token>')
def decryptage(key, token):
    try:
        f = Fernet(key.encode())  # Création d'un objet Fernet avec la clé fournie
        token_bytes = token.encode()  # Conversion str -> bytes
        valeur_decryptee = f.decrypt(token_bytes)  # Décryptage
        return jsonify({"decrypted_text": valeur_decryptee.decode()})  # Retourne la valeur déchiffrée
    except InvalidToken:
        return jsonify({"error": "Échec du déchiffrement, clé ou token invalide"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur : {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
