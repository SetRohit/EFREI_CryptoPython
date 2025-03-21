from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Page d'accueil

# 🔐 Clé fixe (générée une seule fois avec Fernet.generate_key(), puis copiée ici)
FIXED_KEY = b'MARemplaceParUneVraieCleBase64=='  # Mets ici une vraie clé générée avec Fernet.generate_key()
f = Fernet(FIXED_KEY)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Chiffre la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token sous forme de chaîne

@app.route('/decrypt/', methods=['POST'])
def decryptage():
    data = request.json  # Récupère le JSON envoyé par l'utilisateur
    encrypted_text = data.get("encrypted_text")  # Récupère la valeur chiffrée

    if not encrypted_text:
        return jsonify({"error": "Aucune donnée chiffrée fournie"}), 400

    try:
        decrypted_text = f.decrypt(encrypted_text.encode()).decode()  # Déchiffre la valeur
        return jsonify({"decrypted_text": decrypted_text})  # Retourne la valeur déchiffrée
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
