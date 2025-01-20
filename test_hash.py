from passlib.context import CryptContext

# Initialisation du contexte de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mot de passe en clair
plain_password = "USER1"

# Générer un hachage
hashed_password = pwd_context.hash(plain_password)
print(f"Hachage généré : {hashed_password}")

# Vérifier le mot de passe
is_valid = pwd_context.verify(plain_password, hashed_password)
print(f"Vérification réussie : {is_valid}")
