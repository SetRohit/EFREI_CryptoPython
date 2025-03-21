from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('hello.html')  # Page d'accueil

@app.route('/encrypt/', methods=['POST'])
def encryptage():
    data = request.json  # Récupère le JSON envoyé par l'utilisateur
    valeur = data.get("valeur")  # Message à chiffrer
    user_key = data.get("key")  # Clé fournie par l'utilisateur

    if not valeur or not user_key:
        return jsonify({"error": "Veuillez fournir une valeur et une clé"}), 400

    try:
        # Vérifie si la clé est bien une clé Fernet valide
        key = user_key.encode()
        f = Fernet(key)
        token = f.encrypt(valeur.encode())  # Chiffre la valeur
        return jsonify({"encrypted_text": token.decode()})  # Retourne le texte chiffré
    except Exception as e:
        return jsonify({"error": f"Clé invalide : {str(e)}"}), 400

@app.route('/decrypt/', methods=['POST'])
def decryptage():
    data = request.json  # Récupère le JSON envoyé
    encrypted_text = data.get("encrypted_text")  # Message chiffré
    user_key = data.get("key")  # Clé fournie par l'utilisateur

    if not encrypted_text or not user_key:
        return jsonify({"error": "Veuillez fournir le texte chiffré et la clé"}), 400

    try:
        key = user_key.encode()
        f = Fernet(key)
        decrypted_text = f.decrypt(encrypted_text.encode()).decode()  # Déchiffre le texte
        return jsonify({"decrypted_text": decrypted_text})  # Retourne le texte déchiffré
    except Exception as e:
        return jsonify({"error": f"Échec du déchiffrement : {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
