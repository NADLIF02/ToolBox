# Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    nmap \
    sqlmap \
    hydra \
    wireshark \
    tcpdump \
    netcat-openbsd \
    telnet \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p /app/logs /app/reports /app/uploads /app/temp

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 toolbox

# Donner les droits à l'utilisateur toolbox
RUN chown -R toolbox:toolbox /app

# Changer vers l'utilisateur non-root
USER toolbox

# Exposer le port
EXPOSE 5000

# Commande par défaut
CMD ["python", "app.py"] 
